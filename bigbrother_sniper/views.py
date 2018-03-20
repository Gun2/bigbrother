#-*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response

from bigbrother_sniper.serializers import ( RegistrationSerializer,
                                           IdNumberCheckSerializer,
                                           IdCheckSerializer,
                                           InfoCheckSerializer,
                                           ProfessorProfileSerializer,
                                           StudentProfileSerializer,
                                           DeleteAlertSerializer,
                                           IdRequestSerializer,
                                           PostAlertMessageLogtSerializer,
                                           BigbrotherRuleManager)



from django.utils import timezone
from .models import ( ProfessorProfile,
                      Department,
                      StudentProfile,
                      ProfileImage,
                      TextGuardList,
                      LabelGuardList,
                      PostAlertMessageLog,
                      GuardOrUtilImageSavezone
                      )

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



import random
from django.utils import timezone
import datetime

from django.core.files import File
# Create your views here.

def mainView(request):

    return render(request, 'bigbrother_sniper/main.html')

def mainView(request):

    return render(request, 'bigbrother_sniper/main.html')

def loginView(request):

    return render(request, 'bigbrother_sniper/login.html')

def virtualClassView(request):

    return render(request, 'bigbrother_sniper/virtual_class.html')

class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            newUser = User.objects.create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=make_password(serializer.validated_data['password']),
                is_staff=serializer.validated_data['is_staff'],
            )
            newUser.save()
            if serializer.validated_data['is_staff']:
                newProf = ProfessorProfile.objects.create(
                    user=newUser,
                    employee_id=serializer.validated_data['id'],
                    department=Department.objects.get(pk=serializer.validated_data['department']),
                )
                newProf.save()

                profile_img = ProfileImage.objects.get(pk=serializer.validated_data['profile_image_id'])
                profile_img.user = newUser
                profile_img.save()


            else :
                newStudentProfile = StudentProfile.objects.create(
                    user=newUser,
                    student_id=serializer.validated_data['id'],
                    department=Department.objects.get(pk=serializer.validated_data['department']),
                )
                newStudentProfile.save()

                profile_img = ProfileImage.objects.get(pk=serializer.validated_data['profile_image_id'])
                profile_img.user = newUser
                profile_img.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdCheckView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):

        serializer = IdCheckSerializer(data=request.data)

        if serializer.is_valid():
            reg_username = serializer.validated_data['reg_username']
            user = User.objects.filter(username=reg_username)

            if user.exists():
                result = {
                    "result": 1
                }
                return Response(result)
            return Response(user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdNumberCheckView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):

        serializer = IdNumberCheckSerializer(data=request.data)

        if serializer.is_valid():
            organization_id = serializer.validated_data['organization_id']
            employee_user = ProfessorProfile.objects.filter(employee_id=organization_id)
            student_user = StudentProfile.objects.filter(student_id=organization_id)

            if employee_user.exists():
                result = {
                    "result": 1
                }
                return Response(result)
            if student_user.exists():
                result = {
                    "result": 1
                }
                return Response(result)
            return Response(employee_user)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InfoCheckView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):

        serializer = InfoCheckSerializer(data=request.data)

        if serializer.is_valid():
            login_username = serializer.validated_data['login_username']
            user = User.objects.filter(username=login_username).last()

            if user:
                if user.is_staff:
                    result = {
                        "result": 1
                    }
                    return Response(result)
                else:
                    result = {
                        "result": 2
                    }
                    return Response(result)

            else:
                return Response({'error': 'user not exist'}, status=status.HTTP_404_NOT_FOUND)




class StudentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        std = StudentProfile.objects.get(user=request.user)

        return Response({"StudentPK": std.pk})

class TextGuardListPost(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        if request.user:

            textGuardList = TextGuardList.objects.all()

            if textGuardList:
                textGuard_infos = []
                for list in textGuardList:
                    textGuard_infos.append({
                        "text_value": list.text_value,
                        "drop_on_flag": list.drop_on_flag,
                    })

            # 결과값
            return Response(textGuard_infos)
        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)


class LabelGuardListPost(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        if request.user:

            labelGuardList = LabelGuardList.objects.all()

            if labelGuardList:
                labelGuard_infos = []
                for list in labelGuardList:
                    labelGuard_infos.append({
                        "label_value": list.label_value,
                        "drop_on_flag": list.drop_on_flag,
                    })

            # 결과값
            return Response(labelGuard_infos)
        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)




#필터로그생산
class PostAlertMessage(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        if request.user:
            serializer = PostAlertMessageLogtSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.validated_data['drop_on_flag']==True:
                    tmpFlag = True
                else:
                    tmpFlag = False
                username = request.user.first_name+request.user.last_name
                postLog = PostAlertMessageLog.objects.create(
                    username=username,
                    drop_on_flag=tmpFlag,
                    keyword=serializer.validated_data['keyword'],
                    pictureBase64=serializer.validated_data['pictureBase64'],
                    recordTime=timezone.now(),
                    user = request.user
                )
                postLog.save()
                return Response(serializer.data)
            return Response("serializer is not valid", status=status.HTTP_403_FORBIDDEN)
        else:

            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)

#알림 기록 띄우기
class PostAlertMessageListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user.is_staff:
            AlertLogs = PostAlertMessageLog.objects.all()

            alerts = []

            for Alert in AlertLogs:
                if Alert.drop_on_flag==True:
                    drop_on_flag = "Drop"
                else:
                    drop_on_flag = "Alert"
                alerts.append({
                    "id": Alert.pk,
                    "username": Alert.username,
                    "drop_on_flag": drop_on_flag,
                    "keyword": Alert.keyword,
                    "recordTime": Alert.recordTime
                })
            result = {"alerts": alerts}
            return Response(result)
        else:

            alert = { "alerts" : PostAlertMessageLog.objects.values()}

            return Response(alert)


#텍스트 필터링 목록
class FilterListViewText(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user.is_staff:
            TextFilters = TextGuardList.objects.all()

            textFilters = []

            for TextFilter in TextFilters:

                if TextFilter.drop_on_flag==True:
                    drop_on_flag = "Drop"
                else:
                    drop_on_flag = "Alert"

                textFilters.append({
                    "id": TextFilter.pk,
                    "text_value": TextFilter.text_value,
                    "drop_on_flag": drop_on_flag,
                    "explain": TextFilter.explain

                })
            result = {"textFilters": textFilters}
            return Response(result)
        else:

            textFilters = { "textFilters" : TextGuardList.objects.values()}

            return Response(textFilters)

#라벻 필터링 목록
class FilterListViewLabel(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user.is_staff:
            LabelFilters = LabelGuardList.objects.all()

            labelFilters = []

            for LabelFilter in LabelFilters:

                if LabelFilter.drop_on_flag==True:
                    drop_on_flag = "Drop"
                else:
                    drop_on_flag = "Alert"


                labelFilters.append({
                    "id": LabelFilter.pk,
                    "label_value": LabelFilter.label_value,
                    "drop_on_flag": drop_on_flag,
                    "explain": LabelFilter.explain

                })
            result = {"labelFilters": labelFilters}
            return Response(result)
        else:

            LabelFilter = { "LabelFilters" : LabelGuardList.objects.values()}

            return Response(LabelFilter)


class DeleteAlertLog(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        serializer = DeleteAlertSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data['id']

            if request.user.is_staff:
                alertDelete = PostAlertMessageLog.objects.get(pk=id)
                alertDelete.delete()
                result = {
                    "result": 1
                }
            return Response(result)

        else:
            return Response(" Error.", status=status.HTTP_403_FORBIDDEN)



class DeleteAlertText(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        serializer = DeleteAlertSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data['id']

            if request.user.is_staff:
                alertDelete = TextGuardList.objects.get(pk=id)
                alertDelete.delete()
                result = {
                    "result": 1
                }
            return Response(result)

        else:
            return Response(" Error.", status=status.HTTP_403_FORBIDDEN)

class DeleteAlertLabel(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        serializer = DeleteAlertSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data['id']

            if request.user.is_staff:
                alertDelete = LabelGuardList.objects.get(pk=id)
                alertDelete.delete()
                result = {
                    "result": 1
                }
            return Response(result)

        else:
            return Response(" Error.", status=status.HTTP_403_FORBIDDEN)



class CreateRuleMaker(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        if request.user.is_staff:
            serializer = BigbrotherRuleManager(data=request.data)

            if serializer.is_valid():
                if serializer.validated_data['drop_on_flag'] == 1:
                    tmpFlag = 'True'
                else:
                    tmpFlag = 'False'
                if (serializer.validated_data['val']==0):
                    text = TextGuardList.objects.create(
                        text_value=serializer.validated_data['filter'],
                        drop_on_flag=tmpFlag,
                        explain=serializer.validated_data['explain']
                    )
                    text.save()

                elif (serializer.validated_data['val']==1):
                    label = LabelGuardList.objects.create(
                        label_value=serializer.validated_data['filter'],
                        drop_on_flag=tmpFlag,
                        explain=serializer.validated_data['explain']
                    )
                    label.save()

                result = "success"
                return Response(result, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("err", status=status.HTTP_403_FORBIDDEN)






class PostAlertMessageListPreview(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        if request.user.is_staff:

            serializer = DeleteAlertSerializer(data=request.data)
            if serializer.is_valid():
                id = serializer.validated_data['id']
                pictureBase64 = PostAlertMessageLog.objects.get(pk=id)

            return Response(pictureBase64.pictureBase64)
        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)



class DeleteAlertLogAll(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user.is_staff:
            alertDelete = PostAlertMessageLog.objects.all()
            alertDelete.delete()

            return Response("success All Delete", status=status.HTTP_200_OK)

        else:
            return Response("Error.", status=status.HTTP_403_FORBIDDEN)





class LoadAlertList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user:
            AlertLists = PostAlertMessageLog.objects.filter(user = request.user)

            listAlerts = []

            for AlertList in AlertLists:
                if AlertList.drop_on_flag==True:
                    tmpFlag ="위험 판정"
                else:
                    tmpFlag="경고 판"

                listAlerts.append({
                    "id": AlertList.pk,
                    "keyword": AlertList.keyword,
                    "recordTime": AlertList.recordTime,
                    "drop_on_flag" :tmpFlag.decode('utf-8')
                })
            return Response(listAlerts)

        else:

            return Response("Error.", status=status.HTTP_403_FORBIDDEN)



class LoadAlertImage(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        if request.user:
            serializer = IdRequestSerializer(data=request.data)

            if serializer.is_valid():
                AlertList = PostAlertMessageLog.objects.get(pk = serializer.validated_data['id'])

                listAlerts = []

                #drop이면 이미지 숨기기
                if AlertList.drop_on_flag == True:
                    guardImage = GuardOrUtilImageSavezone.objects.get(pictureName="guardPic")

                    listAlerts.append({
                        "pictureBase64": guardImage.pictureBase64,
                        "cause": AlertList.cause
                    })
                else:
                    listAlerts.append({
                        "pictureBase64": AlertList.pictureBase64,
                        "cause": AlertList.cause
                    })
                return Response(listAlerts)

        else:

            return Response("Error", status=status.HTTP_403_FORBIDDEN)