# Generated by Django 3.1.7 on 2021-04-02 04:58

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('inventory', '0008_auto_20210402_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='inventory.GenericStringTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
