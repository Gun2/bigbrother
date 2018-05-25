#-*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response

from bigbrother_sniper.serializers import (RegistrationSerializer,
                                           IdNumberCheckSerializer,
                                           IdCheckSerializer,
                                           InfoCheckSerializer,
                                           AdminProfileSerializer,
                                           EmployeeProfileSerializer,
                                           DeleteAlertSerializer,
                                           IdRequestSerializer,
                                           PostAlertMessageLogtSerializer,
                                           BigbrotherRuleManager,
                                           DateListenerSerializer,
                                           RequestFilterWithUuidSerializer,
                                           BigbrotherLocationManager)



from django.utils import timezone
from .models import ( AdminProfile,
                      EmployeeProfile,
                      TextGuardList,
                      LabelGuardList,
                      PostAlertMessageLog,
                      DateRecord,
                      GuardOrUtilImageSavezone,
                      LocationList,
                      UserActiveLog,
                      UserActiveDateRecord

                      )

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

#uuid 포맷
import uuid
#스레드
import threading

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

    return render(request, 'bigbrother_sniper/alert_page.html')


#정의
class defineWord():
    #모든 규칙 설정 uuid값
    def BROADCASTLOCATION(self):
        return "ffffffff-ffff-ffff-ffff-ffffffffffff"


#스레드 호출 클레스
class ThreadClass:
    #사용자 기록 갱신 스레드
    def userActiveLogRenewal(self):
        connectingUserActiveList = UserActiveLog.objects.filter(connectionEndFlag = False)
        for connectingUserActive in connectingUserActiveList:

            #15초 이상이면 연결 해제
            if ((timezone.now() - connectingUserActive.finalConnectionDate).seconds > 15):
                connectingUserActive.connectionEndFlag=True
                connectingUserActive.save()

        #migrations시 주석처리 지점
        #threading.Timer(5, self.userActiveLogRenewal).start()

#용자 기록 갱신스래드 시작
ThreadClass = threading.Thread(target=ThreadClass().userActiveLogRenewal, args=())
ThreadClass.start()

#메소드 모음 클레스
class BigBroUtils:

    #사용자 활동 기록 생성
    def createUserActiveLog(slef, user):
        print (user)
        activeLog = UserActiveLog.objects.create(
            user=user,
            finalConnectionDate=timezone.now(),
            connectionEndFlag=False,
            startConnectionDate=timezone.now(),
            date=BigBroUtils().searchUserActivityDateTable()
        )
        activeLog.save()

    #날짜 연결할 Date가져오기 //없으면 생성하기 //Date반환
    def searchDateTable(self):

        # 날짜 기록
        dateRecord = DateRecord.objects.filter(date=(str)(timezone.now())[0:10])
        if dateRecord:
            DateNow = dateRecord.first()
        else:
            createDate = DateRecord.objects.create(
                date=(str)(timezone.now())[0:10]
            )
            createDate.save()
            DateNow = DateRecord.objects.get(date=(str)(timezone.now())[0:10])
        return DateNow

   #사용자 기록 날짜 연결할 Date가져오기 //없으면 생성하기 //Date반환
    def searchUserActivityDateTable(self):
        # 날짜 기록
        dateRecord = UserActiveDateRecord.objects.filter(date=(str)(timezone.now())[0:10])
        if dateRecord:
            DateNow = dateRecord.first()
        else:
            createDate = UserActiveDateRecord.objects.create(
                date=(str)(timezone.now())[0:10]
            )
            createDate.save()
            DateNow = dateRecord.objects.get(date=(str)(timezone.now())[0:10])
        return DateNow




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
                newProf = AdminProfile.objects.create(
                    user=newUser,
                    admin_id=serializer.validated_data['id'],
                )
                newProf.save()




            else :
                newEmployeeProfile = EmployeeProfile.objects.create(
                    user=newUser,
                    employee_id=serializer.validated_data['id'],
                )
                newEmployeeProfile.save()


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
            admin_user = AdminProfile.objects.filter(admin_id=organization_id)
            employee_user = EmployeeProfile.objects.filter(employee_id=organization_id)

            if admin_user.exists():
                result = {
                    "result": 1
                }
                return Response(result)
            if employee_user.exists():
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




class EmployeeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        std = EmployeeProfile.objects.get(user=request.user)

        return Response({"EmployeePK": std.pk})

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
            return Response("not found text list", status=status.HTTP_403_FORBIDDEN)

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

            return Response("not found label list", status=status.HTTP_403_FORBIDDEN)
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
                label_value = serializer.validated_data['label_value']
                pkList =  list(set(serializer.validated_data['pk']))


                locationNow=""
                explainText=""

            #받아야 할 것
                #사진 설명 넣기
                explainLabel = "사물 : "
                for index in label_value:
                    explainLabel += " "+index

                #위치 넣기
                for pk in pkList:
                    location = LocationList.objects.get(pk=pk)
                    locationNow += " "+(location.location)



                if serializer.validated_data['drop_on_flag']==True:
                    tmpFlag = True
                    explain = explainLabel + "\n"+explainText + "\n위와 같은 이유로 사진을 차단하였습니다."
                else:
                    tmpFlag = False
                    explain = explainLabel + "\n"+explainText + "\n위와 같은 이유로 사진에 문제점이 발견되었습니다."


                if UserActiveLog.objects.filter(user = request.user, connectionEndFlag = False):
                    userActiveLog = UserActiveLog.objects.filter(user = request.user, connectionEndFlag = False).last()
                else:
                    userActiveLog = None


                postLog = PostAlertMessageLog.objects.create(
                    drop_on_flag=tmpFlag,
                    keyword=serializer.validated_data['label_value'],
                    pictureBase64=serializer.validated_data['pictureBase64'],
                    recordTime=timezone.now(),
                    user = request.user,
                    date=BigBroUtils().searchDateTable(),
                    cause = explain,
                    userActiveLog = userActiveLog,
                    location = locationNow


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
            AlertLogs = PostAlertMessageLog.objects.filter(alertView = True)
            #print (str)(timezone.now())[0:10]
            alerts = []

            for Alert in AlertLogs:
                if Alert.drop_on_flag==True:
                    drop_on_flag = "Drop"
                    color = "red"
                else:
                    drop_on_flag = "Alert"
                    color = "yellow"

                alerts.append({
                    "id": Alert.pk,
                    "username": Alert.user.last_name+Alert.user.first_name,
                    "drop_on_flag": drop_on_flag,
                    "keyword": Alert.keyword,
                    "recordTime": Alert.recordTime,
                    "color": color,
                    "newFlag": Alert.newFlag
                })
            result = {"alerts": alerts}
            return Response(result)
        else:

            alert = { "alerts" : PostAlertMessageLog.objects.values()}

            return Response(alert)

# 위치및 규칙 목록
class FilterListViewLocation(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user.is_staff:
            LocationFilters = LocationList.objects.all()

            locationFilters = []





            for LocationFilter in LocationFilters:

                if (str)(LocationFilter.uuid) == defineWord().BROADCASTLOCATION():
                    location = '모든지역'
                else:
                    location = LocationFilter.location

                TextFilters = TextGuardList.objects.filter(uuid=LocationFilter)
                LabelFilters = LabelGuardList.objects.filter(uuid=LocationFilter)

                textFilters = []
                labelFilters = []



                for TextFilter in TextFilters:

                    if TextFilter.drop_on_flag == True:
                        drop_on_flag = "Drop"
                    else:
                        drop_on_flag = "Alert"

                    textFilters.append({
                        "id": TextFilter.pk,
                        "text_value": TextFilter.text_value,
                        "drop_on_flag": drop_on_flag,
                        "explain": TextFilter.explain,
                        "location": location,
                        "range": TextFilter.range,
                        "picRequest":TextFilter.picRequest
                    })

                for LabelFilter in LabelFilters:

                    if LabelFilter.drop_on_flag == True:
                        drop_on_flag = "Drop"
                    else:
                        drop_on_flag = "Alert"

                    labelFilters.append({
                        "id": LabelFilter.pk,
                        "label_value": LabelFilter.label_value,
                        "drop_on_flag": drop_on_flag,
                        "explain": LabelFilter.explain,
                        "location": location,
                        "range": LabelFilter.range,
                        "picRequest": LabelFilter.picRequest

                    })

                locationFilters.append({
                "uuid": LocationFilter.uuid,
                "location": location,
                "range": LocationFilter.range,
                "pk": LocationFilter.pk,
                "textFilters": textFilters,
                "labelFilters": labelFilters
                })

            result = {"locationFilters": locationFilters}
            return Response(result)
        else:

            return Response("not admin", status=status.HTTP_403_FORBIDDEN)



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


class Deletelocation(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        serializer = DeleteAlertSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data['id']

            if request.user.is_staff:
                alertDelete = LocationList.objects.get(pk=id)
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

                beaconUuid = LocationList.objects.get(pk=serializer.validated_data['pk'])

                if (beaconUuid.range < serializer.validated_data['range']):
                    result = "failure"
                    return Response(result, status=status.HTTP_403_BAD_REQUEST)

                #규칙 옵션 //alert, drop
                if serializer.validated_data['drop_on_flag'] == 1:
                    tmpOptionFlag = True
                else:
                    tmpOptionFlag = False

                #사진 요청
                if serializer.validated_data['picRequest']:
                    tmpPicFlag = True
                else:
                    tmpPicFlag = False

                if (serializer.validated_data['val']==0):
                    text = TextGuardList.objects.create(
                        text_value=serializer.validated_data['filter'],
                        drop_on_flag=tmpOptionFlag,
                        explain=serializer.validated_data['explain'],
                        uuid=beaconUuid,
                        range=serializer.validated_data['range'],
                        picRequest=tmpPicFlag
                    )
                    text.save()

                elif (serializer.validated_data['val']==1):
                    label = LabelGuardList.objects.create(
                        label_value=serializer.validated_data['filter'],
                        drop_on_flag=tmpOptionFlag,
                        explain=serializer.validated_data['explain'],
                        uuid=beaconUuid,
                        range=serializer.validated_data['range'],
                        picRequest=tmpPicFlag
                    )
                    label.save()

                result = "success"
                return Response(result, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("err", status=status.HTTP_403_FORBIDDEN)



class CreateLocationMaker(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        if request.user.is_staff:
            serializer = BigbrotherLocationManager(data=request.data)

            if serializer.is_valid():
                #모든지역 브로드캐스트
                if (defineWord().BROADCASTLOCATION() == (str)(serializer.validated_data['uuid'])):
                    locationList = LocationList.objects.create(
                        uuid=serializer.validated_data['uuid'],
                        range=0,
                        location=serializer.validated_data['location'],

                    )
                else:
                    locationList = LocationList.objects.create(
                        uuid=serializer.validated_data['uuid'],
                        range=serializer.validated_data['maxRange'],
                        location = serializer.validated_data['location']
                    )
                locationList.save()

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
                selectAlert = PostAlertMessageLog.objects.get(pk=id)
                results = {
                    "pictureBase64" : selectAlert.pictureBase64,
                    "keyword" : selectAlert.keyword,
                    "explain" : selectAlert.cause
                }
            return Response(results)
        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)



class DeleteAlertLogAll(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        if request.user.is_staff:
            serializer = DateListenerSerializer(data=request.data)
            if serializer.is_valid():
                DateResult = DateRecord.objects.get(date = serializer.validated_data['date'])
                alertDeleteList = PostAlertMessageLog.objects.filter(date = DateResult)
                for alertDelete in alertDeleteList:
                    alertDelete.delete()

            return Response("success All Delete", status=status.HTTP_200_OK)

        else:
            return Response("Error.", status=status.HTTP_403_FORBIDDEN)




#사용자에게 알림 리스트 제공
class LoadAlertList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user:
            AlertLists = PostAlertMessageLog.objects.filter(user = request.user)

            listAlerts = []

            for AlertList in AlertLists:
                if AlertList.userView:
                    if AlertList.drop_on_flag==True:
                        tmpFlag ="위험 판정"
                    else:
                        tmpFlag="경고 판정"

                    listAlerts.append({
                        "id": AlertList.pk,
                        "keyword": AlertList.keyword,
                        "recordTime": AlertList.recordTime,
                        "drop_on_flag" :tmpFlag
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






class AlertLogDateSearch(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        if request.user.is_staff:
            alertDataLists = DateRecord.objects.all()

            results = []

            for alertDataList in alertDataLists:
                results.append({
                    "date": alertDataList.date,
                })


            return Response(results)

        else:
            return Response("no permission", status=status.HTTP_403_FORBIDDEN)

class AlertLogDateSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        if request.user.is_staff:
            serializer = DateListenerSerializer(data=request.data)
            if serializer.is_valid():
                SearchDate = DateRecord.objects.get(date = serializer.validated_data['date'])

                SearchAlertLists = PostAlertMessageLog.objects.filter(date = SearchDate)
                results = []

                for SearchAlertList in SearchAlertLists:
                    if SearchAlertList.drop_on_flag == True:
                        tmpFlag = "위험 판정"
                    else:
                        tmpFlag = "경고 판정"

                    results.append({
                        "id": SearchAlertList.pk,
                        "keyword": SearchAlertList.keyword,
                        "recordTime": SearchAlertList.recordTime,
                        "drop_on_flag": tmpFlag,
                        "username" : SearchAlertList.user.last_name+SearchAlertList.user.first_name
                    })
                return Response(results)
        else:
            return Response("no permission", status=status.HTTP_403_FORBIDDEN)




class HidnAlertLog(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        serializer = DeleteAlertSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data['id']

            if request.user.is_staff:
                alertDelete = PostAlertMessageLog.objects.get(pk=id)
                alertDelete.alertView = False
                alertDelete.save()
                result = {
                    "result": 1
                }
            return Response(result)

        else:
            return Response(" Error.", status=status.HTTP_403_FORBIDDEN)



class HidnAlertLogAll(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):

        if request.user.is_staff:
            alertDelete = PostAlertMessageLog.objects.all()
            for index in alertDelete:
                index.alertView = False
                index.save()

            return Response("success All Hidn", status=status.HTTP_200_OK)

        else:
            return Response("Error.", status=status.HTTP_403_FORBIDDEN)


class TextGuardListPostBeacon(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
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
            return Response("not found text list", status=status.HTTP_403_FORBIDDEN)

        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)



#지역별 사물 필터값 반환
class LabelGuardListPostBeacon(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        if request.user:
            serializer = RequestFilterWithUuidSerializer(data=request.data)


            if serializer.is_valid():

                labelGuard_infos = []
                BroadcastUuid = LocationList.objects.filter(uuid=defineWord().BROADCASTLOCATION())
                # 전체지역 필터값 넣기
                labelGuardList = LabelGuardList.objects.filter(uuid=BroadcastUuid)
                for labelGuard in labelGuardList:
                    labelGuard_infos.append({
                        "label_value": labelGuard.label_value,
                        "drop_on_flag": labelGuard.drop_on_flag,
                        "location": "모든지역",
                        "picRequest": labelGuard.picRequest,
                        "pk": BroadcastUuid.last().pk
                    })

                Beaconlist = serializer.validated_data['BeaconInfoList']
                for Beacon in Beaconlist:

                    #DB에 등록된 uuid인지 확인
                    if LocationList.objects.filter(uuid = Beacon[0]):

                        # 지역별 범위 확인 후 필터값 삽입
                        location = LocationList.objects.get(uuid = Beacon[0])
                        labelGuardList = LabelGuardList.objects.filter(uuid = location)
                        for labelGuard in labelGuardList:

                            if (labelGuard.range > ((int)(Beacon[1]))):
                                changeFlag = False

                                #중복 검사
                                for labelGuard_info in labelGuard_infos:
                                    if labelGuard_info["label_value"] == labelGuard.label_value:
                                        if (labelGuard_info["drop_on_flag"] == False) and (labelGuard.drop_on_flag == True):
                                            labelGuard_info["drop_on_flag"] = labelGuard.drop_on_flag
                                            labelGuard_info["location"] = labelGuard.uuid.location
                                        if labelGuard_info["picRequest"] == True and labelGuard.picRequest == False:
                                            labelGuard_info["picRequest"] = labelGuard.picRequest
                                            labelGuard_info["location"] = labelGuard.uuid.location
                                            #print (labelGuard_info.index(labelGuard.label_value))
                                        changeFlag=True
                                if changeFlag==False:
                                    labelGuard_infos.append({
                                        "label_value": labelGuard.label_value,
                                        "drop_on_flag": labelGuard.drop_on_flag,
                                        "location": labelGuard.uuid.location,
                                        "picRequest": labelGuard.picRequest,
                                        "pk": location.pk
                                    })



                print (labelGuard_infos)

                # 결과값
                return Response(labelGuard_infos)

                #return Response("not found label list", status=status.HTTP_403_FORBIDDEN)
            return Response("request error", status=status.HTTP_403_FORBIDDEN)

        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)



#비콘 목록 출력
class BeaconListSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        if request.user.is_staff:
            beaconLists = LocationList.objects.all()

            results = []

            for beaconList in beaconLists:

                results.append({
                    "pk": beaconList.pk,
                    "location": beaconList.location,

                })


            return Response(results)

        else:
            return Response("permission error", status=status.HTTP_403_FORBIDDEN)



#규칙 설정 최대거리 반환
class BeaconListRange(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        if request.user:
            serializer = IdRequestSerializer(data=request.data)

            if serializer.is_valid():

                location = LocationList.objects.get(pk=serializer.validated_data['id'])


                return Response(location.range)
            return Response("request error", status=status.HTTP_403_FORBIDDEN)

        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)






#규칙 설정 최대거리 반환
class AlertActiveLog(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


    def get(self, request):
        if request.user:
            activeLogList = UserActiveLog.objects.filter(user=request.user)
            #로그 없으면 처음 있으면 플레그 검사
            if activeLogList:
                activeLog = activeLogList.last()
                #플레그 활성화시 플레그 검사
                if activeLog.connectionEndFlag:
                    BigBroUtils().createUserActiveLog(request.user)

                    return Response("User Active Log is Created", status=status.HTTP_200_OK)

                else:
                    activeLog.finalConnectionDate = timezone.now()
                    activeLog.save()

                return Response("User Active Log is Renewaled", status=status.HTTP_200_OK)

            #없으면
            else:
                #사용자 로그 생성
                BigBroUtils().createUserActiveLog(request.user)
            return Response("User Active Log is Created", status=status.HTTP_200_OK)

        else:
            return Response("Unknown User request", status=status.HTTP_403_FORBIDDEN)



class NewAlertWasRead(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):

        serializer = IdRequestSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data['id']

            if request.user.is_staff:
                alertRead = PostAlertMessageLog.objects.get(pk=id)
                alertRead.newFlag = False
                alertRead.save()
                result = {
                    "result": 1
                }
            return Response(result)

        else:
            return Response(" Error.", status=status.HTTP_403_FORBIDDEN)

