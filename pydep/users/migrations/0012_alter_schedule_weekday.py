# Generated by Django 4.2.5 on 2024-05-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_schedule_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='weekday',
            field=models.CharField(choices=[('Monday', 'Понедельник'), ('Tuesday', 'Вторник'), ('Wednesday', 'Среда'), ('Thursday', 'Четверг'), ('Friday', 'Пятница'), ('Saturday', 'Суббота'), ('Sunday', 'Воскресенье')], max_length=19, verbose_name='День недели'),
        ),
    ]