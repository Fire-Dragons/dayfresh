from django.shortcuts import redirect
import hashlib
import uuid
import os

#md5加密方法
def mymd5(pwd):
    my_md5 = hashlib.md5()
    my_md5.update(pwd.encode('utf-8'))
    return my_md5.hexdigest()
