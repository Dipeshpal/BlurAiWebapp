from django.db import models
# from django.core.validators import FileExtensionValidator


class File(models.Model):
    file = models.ImageField()
    def __str__(self):
        return self.file