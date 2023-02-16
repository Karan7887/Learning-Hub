from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    class Meta:
        verbose_name_plural = 'Notes'
    def __str__(self):
        return self.title

class Todos(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=50)
    finish = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Todos'
    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE,null=True, blank=True)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    homework_date = models.DateField(auto_now_add=False,auto_now=False,blank=True,default=datetime.now().date())
    finish = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Homework'
    def __str__(self):
        return self.title