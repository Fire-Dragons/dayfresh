from django.db import models
from repeated.base_model import BaseModel
from user.models import User

class Address(BaseModel):
    user= models.ForeignKey(User,verbose_name='所属帐号')
    receiver=models.CharField(max_length=20,verbose_name='收件人',default=user)
    addr=models.CharField(max_length=256,verbose_name='收件地址')
    zip_code=models.CharField(max_length=6,null=True,verbose_name='邮件编码')
    phone=models.CharField(max_length=11,verbose_name='联系电话')
    is_default=models.BooleanField(default=True,verbose_name='是否默认')

    class Meta:
        db_table='df_address'
        verbose_name='地址'
        verbose_name_plural=verbose_name