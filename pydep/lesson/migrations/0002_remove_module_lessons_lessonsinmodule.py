# Generated by Django 4.2.4 on 2023-08-31 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='lessons',
        ),
        migrations.CreateModel(
            name='LessonsInModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson', unique=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.module', unique=True)),
            ],
        ),
    ]