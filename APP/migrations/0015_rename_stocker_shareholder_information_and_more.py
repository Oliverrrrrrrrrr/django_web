# Generated by Django 4.1.7 on 2023-03-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0014_rename_shareholder_information_stocker'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stocker',
            new_name='Shareholder_information',
        ),
        migrations.AlterField(
            model_name='main_person',
            name='company_name',
            field=models.CharField(max_length=80, verbose_name='企业名称'),
        ),
    ]