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