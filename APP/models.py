from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=80, verbose_name='用户名', null=False, blank=False, unique=True)
    password = models.CharField(max_length=80, verbose_name='密码', null=False, blank=False)

    class Meta:
        db_table = u'user'
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Tianyancha_User(models.Model):
    phone = models.CharField(max_length=80, verbose_name='手机号', null=False, blank=False, unique=True)
    password = models.CharField(max_length=80, verbose_name='密码', null=False, blank=False)

    class Meta:
        db_table = u'tianyancha_user'
        verbose_name = u'天眼查用户'
        verbose_name_plural = u'天眼查用户'

    def __str__(self):
        return self.phone


class Main_person(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='企业名称', null=False, blank=False)
    pname = models.CharField(max_length=80, verbose_name='姓名', null=False, blank=False)
    position = models.CharField(max_length=80, verbose_name='职位', null=False, blank=False)

    class Meta:
        db_table = u'main_person'
        verbose_name = u'主要人员'
        verbose_name_plural = u'主要人员'

    def __str__(self):
        return self.pname


class Shareholder_information(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='企业名称', null=False, blank=False,
                                    default='default_value')
    shareholder_name = models.CharField(max_length=80, verbose_name='股东（发起人）', null=False, blank=False)
    shareholding_ratio = models.CharField(max_length=80, verbose_name='持股比例', null=False, blank=False)
    ultimate_beneficial_shares = models.CharField(max_length=80, verbose_name='最终受益股份', null=False, blank=False)
    contribution_amount = models.CharField(max_length=80, verbose_name='认缴出资额', null=False, blank=False)
    contribution_time = models.CharField(max_length=80, verbose_name='认缴出资日期', null=False, blank=False)

    class Meta:
        db_table = u'shareholder_information'
        verbose_name = u'股东信息'
        verbose_name_plural = u'股东信息'

    def __str__(self):
        return self.shareholder_name


class Qualification_person(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='企业名称', null=False, blank=False,
                                    default='default_value')
    qualification_name = models.CharField(max_length=80, verbose_name='资质名称', null=False, blank=False)
    qualification_number = models.CharField(max_length=80, verbose_name='资质证书号', null=False, blank=False)
    qualification_type = models.CharField(max_length=80, verbose_name='资质类别', null=False, blank=False)
    qualification_date = models.CharField(max_length=80, verbose_name='发证日期', null=False, blank=False)
    qualification_validity = models.CharField(max_length=80, verbose_name='证书有效期', null=False, blank=False)
    qualification_authority = models.CharField(max_length=80, verbose_name='发证机关', null=False, blank=False)

    class Meta:
        db_table = u'qualification'
        verbose_name = u'资质'
        verbose_name_plural = u'资质'

    def __str__(self):
        return self.qualification_name


class Register_person(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='企业名称', null=False, blank=False,
                                    default='default_value')
    register_person_name = models.CharField(max_length=80, verbose_name='姓名', null=False, blank=False)
    register_person_type = models.CharField(max_length=80, verbose_name='注册类别', null=False, blank=False)
    register_person_number = models.CharField(max_length=80, verbose_name='注册号', null=False, blank=False)
    register_person_profession = models.CharField(max_length=80, verbose_name='注册专业', null=False, blank=False)

    class Meta:
        db_table = u'register_person'
        verbose_name = u'注册人员'
        verbose_name_plural = u'注册人员'

    def __str__(self):
        return self.register_person_name


class Project(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='企业名称', null=False, blank=False,
                                    default='default_value')
    project_id = models.CharField(max_length=80, verbose_name='项目编号', null=False, blank=False)
    project_name = models.CharField(max_length=80, verbose_name='项目名称', null=False, blank=False)
    project_place = models.CharField(max_length=80, verbose_name='项目属地', null=False, blank=False)
    project_type = models.CharField(max_length=80, verbose_name='项目类型', null=False, blank=False)
    construct_company = models.CharField(max_length=80, verbose_name='建设单位', null=False, blank=False)

    class Meta:
        db_table = u'project'
        verbose_name = u'项目'
        verbose_name_plural = u'项目'

    def __str__(self):
        return self.project_name


class UploadProjectFile(models.Model):
    type = models.CharField(max_length=100, verbose_name='文件类型')
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    title = models.CharField(max_length=100, verbose_name='文件名')
    path = models.FileField(upload_to='file/project_file', verbose_name='文件路径')

    class Meta:
        db_table = u'upload_project_file'
        verbose_name = u'上传文件'
        verbose_name_plural = u'上传文件'

    def __str__(self):
        return self.title


class UploadTestFile(models.Model):
    type = models.CharField(max_length=100, verbose_name='文件类型')
    title = models.CharField(max_length=100, verbose_name='文件名')
    path = models.FileField(upload_to='file/test_file', verbose_name='文件路径')

    class Meta:
        db_table = u'upload_test_file'
        verbose_name = u'上传检查文件'
        verbose_name_plural = u'上传检查文件'

    def __str__(self):
        return self.title


class Seal(models.Model):
    file_title = models.CharField(max_length=100, verbose_name='文件名')
    seal_page = models.CharField(max_length=100, verbose_name='印章位置')
    path = models.FileField(upload_to='Seal_Picture', verbose_name='印章路径')

    class Meta:
        db_table = u'seal'
        verbose_name = u'印章'
        verbose_name_plural = u'印章'

    def __str__(self):
        return self.file_title


# 文书网用户
class Wenshuwang_User(models.Model):
    phoneW = models.CharField(max_length=80, verbose_name='手机号', null=False, blank=False, unique=True)
    password = models.CharField(max_length=80, verbose_name='密码', null=False, blank=False)

    class Meta:
        db_table = u'wenshuwang_user_info'
        verbose_name = u'文书网用户'
        verbose_name_plural = u'文书网用户'

    def __str__(self):
        return self.phoneW


# 文书网爬虫结果的数据表
class Wenshuwang(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='公司名称', null=False, blank=False, unique=True)
    screen_shot = models.ImageField(upload_to='wenshuwang_pic', verbose_name='截图', null=True, blank=True)

    class Meta:
        db_table = u'wenshuwang_info'
        verbose_name = u'文书网'
        verbose_name_plural = u'文书网'

    def __str__(self):
        return self.company_name


# 采购网
class CGW_inquire(models.Model):
    company_name = models.CharField(max_length=80, verbose_name='公司名称', null=False, blank=False, unique=True)
    penalty = models.CharField(max_length=200, verbose_name='处罚结果', null=False, blank=False)

    class Meta:
        db_table = u'CGW_inquire'
        verbose_name = u'采购网'
        verbose_name_plural = u'采购网'

    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name

