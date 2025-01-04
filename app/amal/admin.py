import os
import tempfile

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
import sqlite3

from .models import AyahGroup, Ayah, LocalDatabase
from .forms import SQLiteUploadForm


# Register your models here.

@admin.register(AyahGroup)
class AyahGroupAdmin(admin.ModelAdmin):
    resource_class = AyahGroup
    list_display = [
        "id",
        "title",
        "subtitle",
    ]
    ordering = ["id"]


@admin.register(Ayah)
class AyahAdmin(admin.ModelAdmin):
    resource_class = Ayah
    list_display = [
        "id",
        "group",
        "title",
        "position",
    ]
    ordering = ["id"]
    list_editable = [
        "position",
    ]
    list_filter = ['group', ]


@admin.register(LocalDatabase)
class LocalDatabaseAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "schema_version",
        "data_version",
        "url",
    ]

    readonly_fields = ("url",)

    change_list_template = 'admin/db_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-sqlite/', self.upload_sqlite_view, name='upload-sqlite'),
        ]
        return custom_urls + urls

    def upload_sqlite_view(self, request):
        self.request = request  # Store request
        if request.method == 'POST':
            form = SQLiteUploadForm(request.POST, request.FILES)
            if form.is_valid():
                return self.process_sqlite_upload(request, request.FILES['sqlite_file'])
        else:
            form = SQLiteUploadForm()

        context = {
            'form': form,
            'title': 'Upload SQLite Database',
            'opts': self.model._meta,
        }
        return render(request, 'admin/upload_sqlite.html', context)

    def process_sqlite_upload(self, request, sqlite_file):
        temp_file_path = None
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in sqlite_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # Connect to uploaded database
            conn = sqlite3.connect(temp_file_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Clear existing data
            Ayah.objects.all().delete()
            AyahGroup.objects.all().delete()

            # Import AyahGroup data with IDs
            cursor.execute('SELECT id, title, subtitle FROM ayah_group')
            for row in cursor.fetchall():
                AyahGroup.objects.create(
                    id=row["id"],
                    title=row["title"],
                    subtitle=row["subtitle"]
                )

            # Get column names from ayah table

            query = f'SELECT * FROM ayah'
            print(query)
            cursor.execute(query)

            for row in cursor.fetchall():
                row_dict = dict(row)
                if 'visible' not in row_dict:
                    row_dict['visible'] = True
                else:
                    row_dict['visible'] = bool(row_dict['visible'])
                Ayah.objects.create(**row_dict)

            conn.close()
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            self.message_user(self.request, 'Database successfully imported')

            return HttpResponseRedirect(reverse('admin:index'))

        except Exception as e:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            self.message_user(self.request, f'Error importing database: {str(e)}', level='ERROR')
            return HttpResponseRedirect(reverse('admin:index'))
