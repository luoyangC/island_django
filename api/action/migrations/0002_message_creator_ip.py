# Generated by Django 3.0.1 on 2020-05-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='creator_ip',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='留言者IP'),
        ),
    ]