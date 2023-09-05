# Generated by Django 4.2.3 on 2023-07-16 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsl_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lslscript',
            name='email',
            field=models.EmailField(default='kessel@informatik.uni-mannheim.de', max_length=254),
        ),
        migrations.AddField(
            model_name='lslscript',
            name='share',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lslscript',
            name='type',
            field=models.CharField(default='string', max_length=255),
        ),
    ]
