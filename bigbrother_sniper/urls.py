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
                    FilterListViewLabel,
                    FilterListViewText,
                    PostAlertMessageListView,
                    DeleteAlertLog,
                    DeleteAlertText,
                    DeleteAlertLabel,
                    CreateRuleMaker,
                    PostAlertMessageListPreview,
                    DeleteAlertLogAll,
                    LoadAlertList,
                    LoadAlertImage)


from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^main/$', mainView, name='main'),
    url(r'^login/$', loginView, name='login'),
    # url(r'^main/$', login_view, name='main'),
    url(r'^virtual_class/$', virtualClassView, name='virtual_class'),
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
    url(r'^api/bigbrother/post/alert/message/$', PostAlertMessage.as_view()),
    url(r'^api/bigbrother/post/alert/message/list/view/$', PostAlertMessageListView.as_view()),
    url(r'^api/bigbrother/post/alert/message/list/preview/$', PostAlertMessageListPreview.as_view()),
    url(r'^api/bigbrother/filter/list/view/text/$', FilterListViewText.as_view()),
    url(r'^api/bigbrother/filter/list/view/label/$', FilterListViewLabel.as_view()),
    url(r'^api/delete/alert/log/$', DeleteAlertLog.as_view()),
    url(r'^api/delete/alert/text/$', DeleteAlertText.as_view()),
    url(r'^api/delete/alert/label/$', DeleteAlertLabel.as_view()),
    url(r'^api/delete/alert/log/all/$', DeleteAlertLogAll.as_view()),
    url(r'^api/create/rule/maker/$', CreateRuleMaker.as_view()),
    url(r'^api/load/alert/list/$', LoadAlertList.as_view()),
    url(r'^api/load/alert/image/$', LoadAlertImage.as_view()),
]
