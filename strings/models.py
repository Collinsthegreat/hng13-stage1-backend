from django.db import models

# Create your models here.
class StoredString(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  # sha256
    value = models.TextField(unique=True)
    properties_json = models.JSONField()  # requires Django 3.1+
    created_at = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "properties": self.properties_json,
            "created_at": self.created_at.isoformat()
        }

    def __str__(self):
        return f"{self.value[:50]} ({self.id[:8]})"
