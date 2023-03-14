from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=80,verbose_name='用户名',null=False,blank=False,unique=True)
    password = models.CharField(max_length=80,verbose_name='密码',null=False,blank=False)

    class Meta:
        db_table = u'user'
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Tianyancha_User(models.Model):
    phone = models.CharField(max_length=80,verbose_name='手机号',null=False,blank=False,unique=True)
    password = models.CharField(max_length=80,verbose_name='密码',null=False,blank=False)

    class Meta:
        db_table = u'tianyancha_user'
        verbose_name = u'天眼查用户'
        verbose_name_plural = u'天眼查用户'

    def __str__(self):
        return self.phone

class Main_person(models.Model):
    pname = models.CharField(max_length=80,verbose_name='姓名',null=False,blank=False)
    position = models.CharField(max_length=80,verbose_name='职位',null=False,blank=False)

    class Meta:
        db_table = u'main_person'
        verbose_name = u'主要人员'
        verbose_name_plural = u'主要人员'

    def __str__(self):
        return self.pname

class Project(models.Model):
    project_id = models.CharField(max_length=80,verbose_name='项目编号',null=False,blank=False)
    project_name = models.CharField(max_length=80,verbose_name='项目名称',null=False,blank=False)
    project_place = models.CharField(max_length=80,verbose_name='项目属地',null=False,blank=False)
    project_type = models.CharField(max_length=80,verbose_name='项目类型',null=False,blank=False)
    construct_company = models.CharField(max_length=80,verbose_name='建设单位',null=False,blank=False)

    class Meta:
        db_table = u'project'
        verbose_name = u'项目'
        verbose_name_plural = u'项目'

    def __str__(self):
        return self.project_name

