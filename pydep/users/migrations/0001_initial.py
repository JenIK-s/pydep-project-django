# Generated by Django 4.2.5 on 2023-09-26 10:58

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Логин')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Почта')),
                ('image', models.ImageField(blank=True, null=True, upload_to='avatar', verbose_name='Аватар')),
                ('first_name', models.CharField(max_length=50, verbose_name='Ваше имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Ваша фамилия')),
                ('birthday', models.DateTimeField(auto_now_add=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('payment', models.IntegerField(blank=True, null=True)),
                ('courses_learn', models.ManyToManyField(blank=True, related_name='user_course', to='lesson.course', verbose_name='Прохожу курсы')),
                ('courses_teach', models.ManyToManyField(blank=True, to='lesson.course', verbose_name='Преподаю курсы')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RegisterCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Запись на курс',
                'verbose_name_plural': 'Записи на курсы',
                'unique_together': {('user', 'course')},
            },
        ),
    ]
