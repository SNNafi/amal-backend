import os
from datetime import datetime

from django.conf import settings
from django.db.models import Max
from django.utils import timezone

from django.db import models
from django.utils.safestring import mark_safe

from app.amal.db_generator import DatabaseGenerator


# Create your models here.

def current_timestamp():
    return float(timezone.now().timestamp())


class TimestampedModel(models.Model):
    created_at = models.FloatField(default=current_timestamp, editable=False)
    updated_at = models.FloatField(default=current_timestamp, editable=False)

    @classmethod
    def last_updated_timestamp(cls):
        last_updated_at = cls.objects.aggregate(max=Max("updated_at"))["max"]
        return last_updated_at if last_updated_at else 0

    @property
    def created_at_in_date_time_format(self):
        return timezone.make_aware(datetime.fromtimestamp(int(self.created_at)))

    @property
    def updated_at_in_date_time_format(self):
        return timezone.make_aware(datetime.fromtimestamp(int(self.updated_at)))

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = current_timestamp()
        self.updated_at = current_timestamp()
        return super(TimestampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class AyahGroup(TimestampedModel):
    title = models.TextField(max_length=100)
    subtitle = models.TextField(max_length=500)

    def __str__(self):
        return self.title


class Ayah(TimestampedModel):
    group = models.ForeignKey(AyahGroup, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    title = models.TextField(max_length=500)
    arabic = models.TextField(blank=True, null=True)
    indopak = models.TextField(blank=True, null=True)
    bangla = models.TextField(blank=True, null=True)
    ref = models.TextField(max_length=200, blank=True, null=True)
    audiopath = models.TextField(blank=True, null=True, max_length=100)
    visible = models.BooleanField(default=True)


class LocalDatabase(models.Model):
    schema_version = models.PositiveSmallIntegerField()
    data_version = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"MEDIA_URL: {settings.MEDIA_URL}")
        print(f"Full path: {os.path.join(settings.MEDIA_ROOT, self.path())}")
        return f"Local Database v{self.schema_version}.{self.data_version}"

    def path(self):
        return f"databases/amal_{self.schema_version}.{self.data_version}.db"

    def absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.path())

    def url(self) -> str:
        return mark_safe(
            f"<a href='{settings.MEDIA_URL}{self.path()}'>{self.path()}</a>"
        )

    def save(self, *args, **kwargs) -> None:
        os.makedirs(os.path.dirname(self.absolute_path()), exist_ok=True)

        with DatabaseGenerator(path=self.absolute_path()) as generator:
            generator.create_database()
            generator.insert_data()

        return super().save(args, kwargs)

    class Meta:
        unique_together = ("schema_version", "data_version")
