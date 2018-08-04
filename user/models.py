from django.db import models
from django.contrib.auth.models import AbstractUser
from repeated.base_model import BaseModel

# class User(models.Model):
#     uname=models.CharField(max_length=100,unique=True)
#     upasswd = models.CharField(max_length=100)
#     umail = models.CharField(max_length=100)
#     is_activity = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.uname

class User(AbstractUser,BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'df_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name