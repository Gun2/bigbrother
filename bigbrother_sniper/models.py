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
    range = models.IntegerField()
    def __str__(self):
        return ((self.location)+" "+str(self.uuid))


class TextGuardList(models.Model):
    text_value = models.CharField(max_length=32, default='')
    drop_on_flag = models.BooleanField(default=False)
    explain = models.CharField(max_length=32, null=True)
    range = models.IntegerField()
    uuid = models.ForeignKey(LocationList, default='', on_delete=models.CASCADE)
    picRequest = models.BooleanField()

    def __str__(self):
        return str(self.text_value)


class LabelGuardList(models.Model):
    label_value = models.CharField(max_length=32, default='')
    drop_on_flag = models.BooleanField(default=False)
    explain = models.CharField(max_length=32, null=True)
    range = models.IntegerField()
    uuid = models.ForeignKey(LocationList, null=True, on_delete=models.CASCADE)
    picRequest = models.BooleanField()

    def __str__(self):
        return str(self.label_value)


class DateRecord(models.Model):
    date = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return str(self.date)

class UserActiveDateRecord(models.Model):
    date = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return str(self.date)


class UserActiveLog(models.Model):
    user = models.ForeignKey(User)
    finalConnectionDate = models.DateTimeField()
    connectionEndFlag = models.BooleanField(default=False)
    startConnectionDate = models.DateTimeField(default=False)
    date = models.ForeignKey(UserActiveDateRecord)
    def __str__(self):
        return (str(self.user.username)+" "+str(self.user.last_name)+str(self.user.first_name)+" "+str(self.finalConnectionDate))


class PostAlertMessageLog(models.Model):
    drop_on_flag = models.BooleanField(default=False)
    keyword = models.CharField(max_length=72, default='')
    pictureBase64 = models.CharField(max_length=1024000, default='')
    recordTime = models.DateTimeField(editable=True, null=True)
    user = models.ForeignKey(User, default='')
    cause = models.CharField(max_length=300, default='')
    date = models.ForeignKey(DateRecord, default='', null=True)
    alertView = models.BooleanField(default=True)
    userActiveLog = models.ForeignKey(UserActiveLog, default='', null=True)
    userView = models.BooleanField(default=True)
    newFlag = models.BooleanField(default=True)
    location = models.CharField(max_length=64, default='')


    def __str__(self):
        return str(self.recordTime)

class GuardOrUtilImageSavezone(models.Model):
    pictureBase64 = models.CharField(max_length=1024000, default='')
    pictureName = models.CharField(max_length=64, default='')

    def __str__(self):
        return str(self.pictureName)

