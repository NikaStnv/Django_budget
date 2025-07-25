# Generated by Django 5.2.4 on 2025-07-24 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Початок періоду')),
                ('end_date', models.DateField(verbose_name='Кінець періоду')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Ким створено')),
            ],
            options={
                'verbose_name': 'Фінансовий звіт',
                'verbose_name_plural': 'Фінансові звіти',
                'ordering': ['-created_at'],
                'permissions': [('can_watch_reports', 'User can watch the reports'), ('can_export_reports', 'User can export the reports')],
            },
        ),
    ]
