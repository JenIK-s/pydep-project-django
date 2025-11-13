# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='content_blocks',
            field=models.JSONField(blank=True, default=list, help_text='Структурированный контент урока в формате блоков', verbose_name='Блоки контента'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
    ]

