from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import AdminProfile, EmployeeProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name','first_name','username', 'password', 'email', 'is_staff')
    def create(self, validated_data):
        user = User.objects.create(
            last_name=validated_data['last_name'],
            first_name = validated_data['first_name'],
            email= validated_data['email'],
            username= validated_data['username'],
            password=make_password(self.validated_data['password']),
            is_staff= validated_data['is_staff']
        )
        user.save()
        return user
class RegistrationSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=128)
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=512)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField(default=False)
    id = serializers.IntegerField()

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ('user', 'admin_id')


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ('user', 'employee_id', 'Bigbrothers')


class IdCheckSerializer(serializers.Serializer):
    reg_username = serializers.CharField(max_length=128)

class IdNumberCheckSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()

class InfoCheckSerializer(serializers.Serializer):
    login_username = serializers.CharField(max_length=128)

class DeleteAlertSerializer(serializers.Serializer):
    id = serializers.CharField()

class IdRequestSerializer(serializers.Serializer):
    id = serializers.CharField()

class PostAlertMessageLogtSerializer(serializers.Serializer):
    keyword = serializers.CharField(max_length=72)
    drop_on_flag = serializers.BooleanField(default=False)
    pictureBase64 = serializers.CharField(max_length=1024000, default='')

class BigbrotherRuleManager(serializers.Serializer):
    filter = serializers.CharField(max_length=36)
    drop_on_flag = serializers.IntegerField()
    explain = serializers.CharField(max_length=32)
    val = serializers.IntegerField()
    pk = serializers.IntegerField()
    range = serializers.IntegerField()

class DateListenerSerializer(serializers.Serializer):
    date = serializers.CharField(max_length=11)

class RequestFilterWithUuidSerializer(serializers.Serializer):
    BeaconInfoList = serializers.ListField(
        child = serializers.ListField(
            child = serializers.CharField()
        )
    )
