from django import forms


class SQLiteUploadForm(forms.Form):
    sqlite_file = forms.FileField(
        label='Select SQLite Database',
        help_text='Upload a SQLite database file to populate the Ayah tables'
    )
