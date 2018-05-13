from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


class AdminProfile(models.Model):
    user = models.OneToOneField(User)
    admin_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.admin_id)

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User)
    employee_id = models.IntegerField(unique=True)


    def __str__(self):
        return str(self.employee_id)

class LocationList(models.Model):
    uuid = models.UUIDField()
    location = models.CharField(max_length=32)
    def __str__(self):
        return (self.location+" "+str(self.uuid))


class TextGuardList(models.Model):
    text_value = models.CharField(max_length=32, default='')
    drop_on_flag = models.BooleanField(default=False)
    explain = models.CharField(max_length=32, null=True)
    def __str__(self):
        return str(self.text_value)


class LabelGuardList(models.Model):
    label_value = models.CharField(max_length=32, default='')
    drop_on_flag = models.BooleanField(default=False)
    explain = models.CharField(max_length=32, default='', null=True)
    uuid = models.ForeignKey(LocationList)

    def __str__(self):
        return str(self.label_value)


class DateRecord(models.Model):
    date = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return str(self.date)


class PostAlertMessageLog(models.Model):
    username = models.CharField(max_length=6, default='')
    drop_on_flag = models.BooleanField(default=False)
    keyword = models.CharField(max_length=72, default='')
    pictureBase64 = models.CharField(max_length=1024000, default='')
    recordTime = models.DateTimeField(editable=True, null=True)
    user = models.ForeignKey(User, default='')
    cause = models.CharField(max_length=300, default='')
    date = models.ForeignKey(DateRecord, default='', null=True)
    alertView = models.BooleanField(default=True)

    def __str__(self):
        return str(self.recordTime)

class GuardOrUtilImageSavezone(models.Model):
    pictureBase64 = models.CharField(max_length=1024000, default='')
    pictureName = models.CharField(max_length=64, default='')

    def __str__(self):
        return str(self.pictureName)
