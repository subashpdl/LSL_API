# Generated by Django 4.2.3 on 2023-09-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsl_api', '0007_lassoresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_id', models.CharField(max_length=100)),
                ('abstraction_id', models.CharField(max_length=100)),
                ('action_id', models.CharField(max_length=100)),
                ('arena_id', models.CharField(max_length=100)),
                ('sheetid', models.CharField(max_length=100)),
                ('systemid', models.CharField(max_length=100)),
                ('variantid', models.CharField(max_length=100)),
                ('adapterid', models.CharField(max_length=100)),
                ('x', models.CharField(max_length=100)),
                ('y', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('rawvalue', models.CharField(max_length=100)),
                ('valuetype', models.CharField(max_length=100)),
                ('lastmodified', models.CharField(max_length=100)),
                ('executiontime', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='LassoResult',
        ),
    ]
