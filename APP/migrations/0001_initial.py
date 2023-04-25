# Generated by Django 4.1.7 on 2023-04-25 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CGW_inquire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(max_length=80, unique=True, verbose_name="公司名称"),
                ),
                ("penalty", models.CharField(max_length=200, verbose_name="处罚结果")),
            ],
            options={
                "verbose_name": "采购网",
                "verbose_name_plural": "采购网",
                "db_table": "cgw_inquire",
            },
        ),
        migrations.CreateModel(
            name="CreditChina",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entityName",
                    models.CharField(
                        default="default_value", max_length=80, verbose_name="企业名称"
                    ),
                ),
                (
                    "administration_management",
                    models.CharField(max_length=80, verbose_name="行政管理"),
                ),
                (
                    "honesty_trustworthiness",
                    models.CharField(max_length=80, verbose_name="诚信守信"),
                ),
                (
                    "Serious_untrustworthy",
                    models.CharField(max_length=80, verbose_name="严重失信主体名单"),
                ),
                (
                    "Abnormal_operation",
                    models.CharField(max_length=80, verbose_name="经营异常"),
                ),
                (
                    "Credit_commitment",
                    models.CharField(max_length=80, verbose_name="信用承诺"),
                ),
                ("Credit_rating", models.CharField(max_length=80, verbose_name="信用评价")),
                (
                    "Judicial_judgment",
                    models.CharField(max_length=80, verbose_name="司法判决"),
                ),
                ("others", models.CharField(max_length=80, verbose_name="其他")),
            ],
            options={
                "verbose_name": "信用中国",
                "verbose_name_plural": "信用中国",
                "db_table": "credit_china",
            },
        ),
        migrations.CreateModel(
            name="Duplicate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_pair", models.CharField(max_length=100, verbose_name="文件对")),
                ("dup_page", models.CharField(max_length=100, verbose_name="重复页位置")),
                ("dup_content", models.CharField(max_length=500, verbose_name="重复段内容")),
                (
                    "standard_lib",
                    models.FileField(upload_to="file/Standard_Lib", verbose_name="标准库"),
                ),
                ("lib_name", models.CharField(max_length=100, verbose_name="标准库名")),
                (
                    "still_dup_content",
                    models.CharField(max_length=500, verbose_name="仍重复内容"),
                ),
            ],
            options={
                "verbose_name": "重复段",
                "verbose_name_plural": "重复段",
                "db_table": "duplicate",
            },
        ),
        migrations.CreateModel(
            name="Main_person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=80, verbose_name="企业名称")),
                ("pname", models.CharField(max_length=80, verbose_name="姓名")),
                ("position", models.CharField(max_length=80, verbose_name="职位")),
            ],
            options={
                "verbose_name": "主要人员",
                "verbose_name_plural": "主要人员",
                "db_table": "main_person",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        default="default_value", max_length=80, verbose_name="企业名称"
                    ),
                ),
                ("project_id", models.CharField(max_length=80, verbose_name="项目编号")),
                ("project_name", models.CharField(max_length=80, verbose_name="项目名称")),
                ("project_place", models.CharField(max_length=80, verbose_name="项目属地")),
                ("project_type", models.CharField(max_length=80, verbose_name="项目类型")),
                (
                    "construct_company",
                    models.CharField(max_length=80, verbose_name="建设单位"),
                ),
            ],
            options={
                "verbose_name": "项目",
                "verbose_name_plural": "项目",
                "db_table": "project",
            },
        ),
        migrations.CreateModel(
            name="Qualification_person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        default="default_value", max_length=80, verbose_name="企业名称"
                    ),
                ),
                (
                    "qualification_name",
                    models.CharField(max_length=80, verbose_name="资质名称"),
                ),
                (
                    "qualification_number",
                    models.CharField(max_length=80, verbose_name="资质证书号"),
                ),
                (
                    "qualification_type",
                    models.CharField(max_length=80, verbose_name="资质类别"),
                ),
                (
                    "qualification_date",
                    models.CharField(max_length=80, verbose_name="发证日期"),
                ),
                (
                    "qualification_validity",
                    models.CharField(max_length=80, verbose_name="证书有效期"),
                ),
                (
                    "qualification_authority",
                    models.CharField(max_length=80, verbose_name="发证机关"),
                ),
            ],
            options={
                "verbose_name": "资质",
                "verbose_name_plural": "资质",
                "db_table": "qualification",
            },
        ),
        migrations.CreateModel(
            name="Register_person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        default="default_value", max_length=80, verbose_name="企业名称"
                    ),
                ),
                (
                    "register_person_name",
                    models.CharField(max_length=80, verbose_name="姓名"),
                ),
                (
                    "register_person_type",
                    models.CharField(max_length=80, verbose_name="注册类别"),
                ),
                (
                    "register_person_number",
                    models.CharField(max_length=80, verbose_name="注册号"),
                ),
                (
                    "register_person_profession",
                    models.CharField(max_length=80, verbose_name="注册专业"),
                ),
            ],
            options={
                "verbose_name": "注册人员",
                "verbose_name_plural": "注册人员",
                "db_table": "register_person",
            },
        ),
        migrations.CreateModel(
            name="Seal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_title", models.CharField(max_length=100, verbose_name="文件名")),
                ("seal_page", models.CharField(max_length=100, verbose_name="印章位置")),
                (
                    "path",
                    models.FileField(upload_to="Seal_Picture", verbose_name="印章路径"),
                ),
            ],
            options={
                "verbose_name": "印章",
                "verbose_name_plural": "印章",
                "db_table": "seal",
            },
        ),
        migrations.CreateModel(
            name="Shareholder_information",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        default="default_value", max_length=80, verbose_name="企业名称"
                    ),
                ),
                (
                    "shareholder_name",
                    models.CharField(max_length=80, verbose_name="股东（发起人）"),
                ),
                (
                    "shareholding_ratio",
                    models.CharField(max_length=80, verbose_name="持股比例"),
                ),
                (
                    "ultimate_beneficial_shares",
                    models.CharField(max_length=80, verbose_name="最终受益股份"),
                ),
                (
                    "contribution_amount",
                    models.CharField(max_length=80, verbose_name="认缴出资额"),
                ),
                (
                    "contribution_time",
                    models.CharField(max_length=80, verbose_name="认缴出资日期"),
                ),
            ],
            options={
                "verbose_name": "股东信息",
                "verbose_name_plural": "股东信息",
                "db_table": "shareholder_information",
            },
        ),
        migrations.CreateModel(
            name="UploadProjectFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=100, verbose_name="文件类型")),
                ("project_name", models.CharField(max_length=100, verbose_name="项目名称")),
                ("title", models.CharField(max_length=100, verbose_name="文件名")),
                (
                    "path",
                    models.FileField(
                        upload_to="file/project_file", verbose_name="文件路径"
                    ),
                ),
            ],
            options={
                "verbose_name": "上传文件",
                "verbose_name_plural": "上传文件",
                "db_table": "upload_project_file",
            },
        ),
        migrations.CreateModel(
            name="UploadTestFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=100, verbose_name="文件类型")),
                ("title", models.CharField(max_length=100, verbose_name="文件名")),
                (
                    "path",
                    models.FileField(upload_to="file/test_file", verbose_name="文件路径"),
                ),
            ],
            options={
                "verbose_name": "上传检查文件",
                "verbose_name_plural": "上传检查文件",
                "db_table": "upload_test_file",
            },
        ),
        migrations.CreateModel(
            name="Wenshuwang",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(max_length=80, unique=True, verbose_name="公司名称"),
                ),
                (
                    "screen_shot",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="wenshuwang_pic",
                        verbose_name="截图",
                    ),
                ),
            ],
            options={
                "verbose_name": "文书网",
                "verbose_name_plural": "文书网",
                "db_table": "wenshuwang_info",
            },
        ),
        migrations.CreateModel(
            name="Wenshuwang_User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phoneW",
                    models.CharField(max_length=80, unique=True, verbose_name="手机号"),
                ),
                ("password", models.CharField(max_length=80, verbose_name="密码")),
            ],
            options={
                "verbose_name": "文书网用户",
                "verbose_name_plural": "文书网用户",
                "db_table": "wenshuwang_user_info",
            },
        ),
        migrations.CreateModel(
            name="Tianyancha_User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone",
                    models.CharField(max_length=80, unique=True, verbose_name="手机号"),
                ),
                ("password", models.CharField(max_length=80, verbose_name="密码")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "天眼查用户",
                "verbose_name_plural": "天眼查用户",
                "db_table": "tianyancha_user",
            },
        ),
        migrations.CreateModel(
            name="MyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=80, unique=True, verbose_name="用户名"),
                ),
                ("password", models.CharField(max_length=80, verbose_name="密码")),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户",
                "verbose_name_plural": "用户",
                "db_table": "user",
            },
        ),
    ]
