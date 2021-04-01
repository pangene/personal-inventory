# Generated by Django 3.1.7 on 2021-04-01 01:28

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('inventory', '0006_auto_20210329_0440'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericStringTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=50, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_genericstringtaggeditem_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_genericstringtaggeditem_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='inventory.GenericStringTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
