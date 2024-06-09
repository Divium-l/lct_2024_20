from django.db import models

class DatabaseConnection(models.Model):
    DATABASE_TYPES = [
        ('postgreSQL', 'PostgreSQL'),
        ('Oracle', 'Oracle'),
        # Добавьте другие типы баз данных, если нужно
    ]

    database_type = models.CharField(max_length=50, choices=DATABASE_TYPES)
    url = models.CharField(max_length=255)
    port = models.CharField(max_length=10)
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    copy = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.database_type} - {self.url}"