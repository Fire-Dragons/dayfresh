from django.db import models

class User(models.Model):
    uname=models.CharField(max_length=100,unique=True)
    upasswd = models.CharField(max_length=100)
    umail = models.CharField(max_length=100)
    is_activity = models.BooleanField(default=0)

    def __str__(self):
        return self.uname