# Generated by Django 5.1.7 on 2025-03-27 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varvitabel', '0002_projektid'),
    ]

    operations = [
        migrations.CreateModel(
            name='mainvarvitabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projekt', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='varvitabel.projektid')),
                ('tootekood', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='varvitabel.toode')),
            ],
        ),
    ]
