# Generated by Django 4.1.7 on 2023-03-24 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0012_alter_seal_path_alter_uploadprojectfile_path_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shareholder_Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='default_value', max_length=80, verbose_name='企业名称')),
                ('shareholder_name', models.CharField(max_length=80, verbose_name='股东（发起人）')),
                ('shareholding_ratio', models.CharField(max_length=80, verbose_name='持股比例')),
                ('ultimate_beneficial_shares', models.CharField(max_length=80, verbose_name='最终受益股份')),
                ('contribution_amount', models.CharField(max_length=80, verbose_name='认缴出资额')),
                ('contribution_time', models.CharField(max_length=80, verbose_name='认缴出资日期')),
            ],
            options={
                'verbose_name': '股东信息',
                'verbose_name_plural': '股东信息',
                'db_table': 'shareholder_information',
            },
        ),
        migrations.AddField(
            model_name='main_person',
            name='company_name',
            field=models.CharField(default='default_value', max_length=80, verbose_name='企业名称'),
        ),
        migrations.AddField(
            model_name='project',
            name='company_name',
            field=models.CharField(default='default_value', max_length=80, verbose_name='企业名称'),
        ),
    ]
