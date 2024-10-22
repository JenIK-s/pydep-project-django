# Generated by Django 4.2.5 on 2023-09-26 10:58

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(default=1000, verbose_name='Цена')),
                ('programming_language', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('lessons', models.ManyToManyField(to='lesson.lesson')),
            ],
            options={
                'verbose_name': 'Модуль',
                'verbose_name_plural': 'Модули',
            },
        ),
        migrations.CreateModel(
            name='ModulesInCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.course', verbose_name='Курс')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.module', verbose_name='Модуль')),
            ],
            options={
                'verbose_name': 'Модули в курсе',
                'verbose_name_plural': 'Модули в курсах',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='modules',
            field=models.ManyToManyField(through='lesson.ModulesInCourse', to='lesson.module', verbose_name='Модули'),
        ),
    ]
