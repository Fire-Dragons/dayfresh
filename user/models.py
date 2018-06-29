from django.db import models

class User(models.Model):
    uname=models.CharField(max_length=100)
    upasswd = models.CharField(max_length=100)
    umail = models.CharField(max_length=100)

    def __str__(self):
        return self.uname