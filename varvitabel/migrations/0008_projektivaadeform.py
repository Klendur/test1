# Generated by Django 5.1.7 on 2025-04-15 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varvitabel', '0007_alter_toode_tootekood'),
    ]

    operations = [
        migrations.CreateModel(
            name='projektivaadeform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkbox', models.IntegerField(blank=True, null=True)),
                ('projekt1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projektid1', to='varvitabel.projektid')),
                ('toode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='varvitabel.toode')),
            ],
        ),
    ]
