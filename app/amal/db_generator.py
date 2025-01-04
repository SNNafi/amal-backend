import os
import sqlite3
from datetime import datetime

from . import models


class DatabaseGenerator:
    def __init__(self, path=None) -> None:
        self.connection = None
        self.db_file_path = path or f"/tmp/amal-{datetime.now()}.db"
        if os.path.exists(self.db_file_path):
            os.remove(self.db_file_path)

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file_path)
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.connection.close()

    def create_database(self):
        self.connection.execute(
            """
            CREATE TABLE "ayah_group" (
	            "id"	INTEGER NOT NULL,
	            "title"	TEXT,
	            "subtitle"	TEXT,
	            PRIMARY KEY("id" AUTOINCREMENT)
);
            """
        )
        self.connection.execute(
            """
            CREATE TABLE "ayah" (
	            "id"	INTEGER NOT NULL,
	            "group_id"	INTEGER NOT NULL,
	            "position"	INTEGER NOT NULL,
	            "title"	TEXT,
	            "arabic"	TEXT,
	            "indopak"	TEXT,
	            "bangla"	TEXT,
	            "ref"	TEXT,
	            "audiopath"	TEXT DEFAULT 0,
	            "visible" INTEGER,
	            PRIMARY KEY("id" AUTOINCREMENT)
)
            """
        )

    def insert_data(self):
        ayah_groups = [
            (
                item.id,
                item.title,
                item.subtitle,
            )
            for item in models.AyahGroup.objects.all()
        ]

        ayahs = [
            (
                item.id,
                item.group_id,
                item.position,
                item.title,
                item.arabic,
                item.indopak,
                item.bangla,
                item.ref,
                item.audiopath,
                int(item.visible),
            )
            for item in models.Ayah.objects.all()
        ]

        self.connection.executemany(
            """
                INSERT INTO ayah_group values (?, ?, ?)
            """,
            ayah_groups,
        )
        self.connection.executemany(
            """
                INSERT INTO ayah values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ayahs,
        )

        self.connection.commit()
        self.connection.execute("VACUUM")
