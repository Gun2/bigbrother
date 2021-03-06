"""bigbrother URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from .views import (
                    mainView,
                    loginView,
                    virtualClassView,
                    RegistrationView,
                    InfoCheckView,
                    IdCheckView,
                    IdNumberCheckView,





                    TextGuardListPost,
                    LabelGuardListPost,
                    PostAlertMessage,
                    PostAlertMessageListView,
                    DeleteAlertLog,
                    DeleteAlertText,
                    DeleteAlertLabel,
                    CreateRuleMaker,
                    CreateLocationMaker,
                    PostAlertMessageListPreview,
                    DeleteAlertLogAll,
                    LoadAlertList,
                    LoadAlertImage,
                    AlertLogDateSearch,
                    AlertLogDateSearchView,
                    HidnAlertLog,
                    HidnAlertLogAll,
                    TextGuardListPostBeacon,
                    LabelGuardListPostBeacon,
                    BeaconListSearchView,
                    BeaconListRange,
                    AlertActiveLog,
                    FilterListViewLocation,
                    NewAlertWasRead,
                    UserLogDateSearchView,
                    UserLogDateSearch,
                    Deletelocation)


from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^main/$', mainView, name='main'),
    url(r'^login/$', loginView, name='login'),
    # url(r'^main/$', login_view, name='main'),
    url(r'^alert_page/$', virtualClassView, name='alert_page'),
    url(r'^$', RedirectView.as_view(url='bigbrother_sniper/main/')),


    url(r'^api/user_register/$', RegistrationView.as_view()),
    url(r'^api/user_register/info/check/$', InfoCheckView.as_view()),
    url(r'^api/user_register/id/check/$', IdCheckView.as_view()),
    url(r'^api/user_register/id/NumberCheck/$', IdNumberCheckView.as_view()),
    url(r'^api/user_auth/$', obtain_jwt_token),
    url(r'^api/user_auth/refresh/$', refresh_jwt_token),
    url(r'^api/user_auth/verify/$', verify_jwt_token),





    url(r'^api/bigbrother/guard/list/text/$', TextGuardListPost.as_view()),
    url(r'^api/bigbrother/guard/list/label/$', LabelGuardListPost.as_view()),
    url(r'^api/bigbrother/guard/list/text/beacon/$', TextGuardListPostBeacon.as_view()),
    url(r'^api/bigbrother/guard/list/label/beacon/$', LabelGuardListPostBeacon.as_view()),

    url(r'^api/bigbrother/post/alert/message/$', PostAlertMessage.as_view()),
    url(r'^api/bigbrother/post/alert/message/list/view/$', PostAlertMessageListView.as_view()),
    url(r'^api/bigbrother/post/alert/message/list/preview/$', PostAlertMessageListPreview.as_view()),

    url(r'^api/bigbrother/filter/list/view/location/$', FilterListViewLocation.as_view()),

    url(r'^api/read/new/alert/$', NewAlertWasRead.as_view()),

    url(r'^api/hidn/alert/log/$', HidnAlertLog.as_view()),
    url(r'^api/hidn/alert/log/all/$', HidnAlertLogAll.as_view()),

    url(r'^api/delete/location/$', Deletelocation.as_view()),
    url(r'^api/delete/alert/log/$', DeleteAlertLog.as_view()),
    url(r'^api/delete/alert/log/all/$', DeleteAlertLogAll.as_view()),
    url(r'^api/delete/alert/text/$', DeleteAlertText.as_view()),
    url(r'^api/delete/alert/label/$', DeleteAlertLabel.as_view()),

    url(r'^api/create/location/maker/$', CreateLocationMaker.as_view()),
    url(r'^api/create/rule/maker/$', CreateRuleMaker.as_view()),

    url(r'^api/load/alert/list/$', LoadAlertList.as_view()),
    url(r'^api/load/alert/image/$', LoadAlertImage.as_view()),

    url(r'^api/alert/list/log/date/$', AlertLogDateSearch.as_view()),
    url(r'^api/alert/list/log/date/view/$', AlertLogDateSearchView.as_view()),

    url(r'^api/UserLog/date/$', UserLogDateSearch.as_view()),
    url(r'^api/UserLog/date/view/$', UserLogDateSearchView.as_view()),

    url(r'^api/alert/active/log/$', AlertActiveLog.as_view()),

    url(r'^api/beacon/list/view/$', BeaconListSearchView.as_view()),
    url(r'^api/beacon/list/range/$', BeaconListRange.as_view())

]
