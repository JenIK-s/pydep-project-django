from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=255)


class Lesson(models.Model):
    messenger = [
        ('Tg', 'Telegram'),
        ('Wt', 'WhatsApp')
    ]
    name = models.CharField(max_length=255)
    communication_method = models.CharField(
        max_length=255,
        choices=messenger
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
    )
    price = models.IntegerField(default=1000)
    pub_date = models.DateTimeField()
