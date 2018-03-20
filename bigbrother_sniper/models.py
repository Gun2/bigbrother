from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

class Department(models.Model):
    name = models.TextField(max_length=64, unique=True)

    def __str__(self):
        return str(self.pk)

def ImageUploadNameBind(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        return 'profile_image/{}.{}'.format(instance.pk, ext)
    else:
        pass
     # do something if pk is not there yet


class ProfileImage(models.Model):
    user = models.OneToOneField(User, null=True)
    image = models.ImageField(upload_to=ImageUploadNameBind)

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User)
    employee_id = models.IntegerField(unique=True)
    department =  models.ForeignKey(Department)
    absence_time_set = models.CharField(max_length=2, default=30)
    def __str__(self):
        return str(self.employee_id)

class StudentProfile(models.Model):
    user = models.OneToOneField(User)
    student_id = models.IntegerField(unique=True)
    department = models.ForeignKey(Department)
    Crypt_rand_N = models.CharField(max_length=6, default='')


    def __str__(self):
        return str(self.student_id)

class TextGuardList(models.Model):
    text_value = models.CharField(max_length=32, default='')
    drop_on_flag = models.BooleanField(default=False)
    explain = models.CharField(max_length=32, null=True)

class LabelGuardList(models.Model):
    label_value = models.CharField(max_length=32, default='')
    drop_on_flag = models.BooleanField(default=False)
    explain = models.CharField(max_length=32, default='', null=True)

class PostAlertMessageLog(models.Model):
    username = models.CharField(max_length=6, default='')
    drop_on_flag = models.BooleanField(default=False)
    keyword = models.CharField(max_length=72, default='')
    pictureBase64 = models.CharField(max_length=1024000, default='')
    recordTime = models.DateTimeField(editable=True, null=True)
    user = models.ForeignKey(User, default='')
    cause = models.CharField(max_length=300, default='')

class GuardOrUtilImageSavezone(models.Model):
    pictureBase64 = models.CharField(max_length=1024000, default='')
    pictureName = models.CharField(max_length=64, default='')