from django.db import models
from datetime import datetime
# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    class Meta:
        verbose_name_plural = 'Notes'
    def __str__(self):
        return self.title

class Homework(models.Model):
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    homework_date = models.DateField(auto_now_add=False,auto_now=False,blank=True,default=datetime.now().date())
    finish = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Homework'
    def __str__(self):
        return self.title