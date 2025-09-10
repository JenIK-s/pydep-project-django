from django.db import models

class FilesProject(models.Model):
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name
