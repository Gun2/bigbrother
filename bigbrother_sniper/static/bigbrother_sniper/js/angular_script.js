
//var token = "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InByb2Zlc3NvcjEiLCJvcmlnX2lhdCI6MTUxMDU1NTEwOSwidXNlcl9pZCI6MTcsImVtYWlsIjoicHJvZmVzc29yMUBkanUuYWMua3IiLCJleHAiOjE1MTA2MTUxMDl9.TwFWXxuA7aiqOMHTS0RZZwumS1KDdgmoafJOI69kNZQ";
var token;

var app = angular.module('BigBrotherApp', ['ngFileUpload','ngSanitize']);


app.controller('localStorage', function($scope, $http){
    const loggedInfo = localStorage.getItem('storedUserAuthData');

    if (loggedInfo != null) {
        token = loggedInfo;
        $scope.completeLogin();
    }
});

app.controller('BigBrotherController', function($scope, $http){

    $scope.completeLogin = function (){
        $scope.LoginPage = false;
        $scope.VirtualClassPage = true;

    }

     $scope.completeLogout = function (){
        $scope.LoginPage = true;
        $scope.VirtualClassPage = false;
    }

});

app.controller('LogoutController', function($scope, $http){

    $scope.doLogout = function(){
            $scope.completeLogout();
            localStorage.removeItem('storedUserAuthData');
        }
});

app.controller('LoginController', function($scope, $http){

        if(localStorage.getItem('id') != 'null' && localStorage.getItem('pw') != 'null' &&localStorage.getItem('check') == 'true'){
            $scope.login_checkbox = true;
            $scope.login_username = localStorage.getItem('id');
            $scope.login_password = localStorage.getItem('pw');
        }

        else{
          $('#checkbox1').checked = false;
         }

$scope.doInfoCheck = function(){
var login_error;
 var userIdData ={
            "login_username" : $scope.login_username
            };

            $http.post("/bigbrother_sniper/api/user_register/info/check/", userIdData)
        .then(function(response){
        //success
             if(response.data.result ==1){
                    $scope.doLogin();

             } else{
                   login_error = " 로그인이 불가합니다. 어플리케이션을 이용해주세요";
                   $("#no_login").html(login_error);
                   $("#login_error").appendTo('body').modal();
                }
        }, function(response){
        /*
            login_error = "회원이 아닙니다. 회원신청 바랍니다.";
            $("#no_login").html(login_error);
            $("#login_error").appendTo('body').modal();*/
            });
  };

    $scope.doLogin = function(){



        var userAuthData = {
            "username": $scope.login_username,
            "password": $scope.login_password
        };

        if(localStorage.getItem('check') == 'true'){
            $('#checkbox1').checked = true;

                if(localStorage.getItem('id') == null || localStorage.getItem('pw') == null){
                      localStorage.setItem('id',$scope.login_username);
                      localStorage.setItem('pw',$scope.login_password);
                }
                 else{
                      if($scope.login_username != localStorage.getItem('id')|| $scope.login_password != localStorage.getItem('pw') ){
                            if($scope.login_username != localStorage.getItem('id')){
                                       localStorage.setItem('id',$scope.login_username);
                            }
                            if($scope.login_password != localStorage.getItem('pw')){
                                       localStorage.setItem('pw',$scope.login_password);
                            }

                      }

                 }


        }

       else{
              localStorage.setItem('check','false');
              localStorage.setItem('id','');
              localStorage.setItem('pw','');
       }


                  $http.post("/bigbrother_sniper/api/user_auth/", userAuthData)
                  .then(function(response){
                   //success
                   token = "JWT " + response.data.token;
                   $scope.completeLogin();
                   $scope.login_username = "";
                   $scope.login_password = "";
                   localStorage.setItem('storedUserAuthData',token);

                    }, function (response){
                   //error
                 $("#registration-failed-modal").appendTo("body").modal();
                  });

    };
    $scope.checked_storage = function(state){
         if(state == true){
             localStorage.setItem('check','true');
         }
         else{
             localStorage.setItem('check','false');
         }
    };


});

app.controller('RegisterController',['$scope', '$http', function ($scope, $http){

 var username_flag = false;
  var id_flag= false;

    $scope.doCheckId = function (){

        var userAuthData = {
            "reg_username": $scope.reg_username
        };

        $http.post("/bigbrother_sniper/api/user_register/id/check/", userAuthData)
            .then(function(response){

               if(response.data.result == '1'){
                     if(username_flag == true){
                            username_flag = false;
                            $('[data-toggle="popover"]').popover({placement: 'top', content: "중복된 아이디 입니다."}).popover("show");
                     }
               }
                else{
                     if(username_flag == false){
                           $('[data-toggle="popover"]').popover('hide');
                           username_flag = true;
                     }
                }

        }, function (response){

        });

     };




}]);


app.controller('BigbrotherController', function($scope, $http, $interval, $sce){

    $scope.loadAlertList = function () {
        $http.get('/bigbrother_sniper/api/bigbrother/post/alert/message/list/view/', {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            alert_list = response.data.alerts;
            $scope.alerts = [];
            for ( index in alert_list ) {
                $scope.alerts.push(alert_list[index]);
            }

        }, function (response){
        });
    };


    $scope.flagBgcolorSellect = function(color, flag) {
               return $sce.trustAsHtml("<font style='background-color:"+color+"'>"+flag+"</font>");
             };

    $scope.deletealert = function(){
        $http.post('/bigbrother_sniper/api/bigbrother/delete/',{"id": deleteId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
                $scope.loadAlertList();

        },function(response){
             $("#bigbrother-failed-modal").appendTo("body").modal();
        });

    };

    $scope.loadalertlist = function () {
        $http.get('/bigbrother_sniper/api/bigbrother/list/', {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            bigbrother_list = response.data.bigbrothers;
            $scope.bigbrothers = [];
            for ( index in bigbrother_list ) {
                $scope.bigbrothers.push(bigbrother_list[index]);
            }

        }, function (response){
        });
    };


/*

Bigbrother 디비 삭제 (로그삭제
*/




    $scope.HidnAlertFilter = function(deleteTarget){
    deleteId = deleteTarget.id
        $http.post('/bigbrother_sniper/api/hidn/alert/log/',{"id": deleteId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
                $scope.loadAlertList();

        },function(response){
             $("#Bigbrother-failed-modal").appendTo("body").modal();
        });

    };

        var deleteId = 0;
      $scope.clickdelete = function(deleteTarget){
      $interval.cancel(timeIntervalReset);
            deleteId = deleteTarget.id;
            $("#deleteCheck").css("z-index", "9999");
            $("#deleteCheck").appendTo("body").modal();
             }
             /*사진미리보기*/



    var selectTarget = 0;
    $scope.clickpreview = function(selectTarget){
    $interval.cancel(timeIntervalReset);
    selectId = selectTarget.id
        $http.post('/bigbrother_sniper/api/bigbrother/post/alert/message/list/preview/',{"id": selectId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            $scope.alertInfo = response.data;
            $scope.loadalertlist();
            $("#ViewPicture").css("z-index", "9999");
            $("#ViewPicture").appendTo("body").modal();
        },function(response){

        });

    };
  //알림 전체 삭제
    $scope.alertAllDelete = function(){
             $interval.cancel(timeIntervalReset);
            $("#deleteAllModal").css("z-index", "9999");
            $("#deleteAllModal").appendTo("body").modal();
             }


    $scope.alertAllHidnStart = function(){
        $http.get('/bigbrother_sniper/api/hidn/alert/log/all/', {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){

        },function(response){
            $scope.startInterval();
        });

    };
//새로고침
        var timeIntervalprocess = 0;
    $scope.startInterval = function () {
         //$interval.cancel(timeIntervalReset);

         timeIntervalReset = $interval(function () {

            if (timeIntervalprocess > 0){
                $interval.cancel(timeIntervalReset);
                timeIntervalprocess -= 1;
            }
            $scope.timeIntervalprocess += 1;
             $scope.loadAlertList();
        }, 1000,1000);
        $scope.timeIntervalReset();


    };

//알림 클래스
  $scope.alertClass = function (flag, newFlag) {
    var className = '';
    if (newFlag == true){
        if (flag === 'Drop') {
          className = 'alert alert-danger';
        } else {
          className = 'alert alert-warning';
        }
    }
    else{
          className = 'well';
    }
    return className;
  };

  $scope.newAlertWasRead = function(clickId){
        $http.post('/bigbrother_sniper/api/read/new/alert/',{"id": clickId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
                $scope.loadAlertList();

        },function(response){
        });

    };
});

app.controller('BigbrotherSniperCheckController', function($scope, $http, $interval, $sce){

//Bigbrother 장소 리스트
 $scope.loadListLocation = function () {
        $http.get('/bigbrother_sniper/api/bigbrother/filter/list/view/location/', {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            location_list = response.data.locationFilters;
            $scope.locations = [];
            for ( index in location_list ) {
                $scope.locations.push(location_list[index]);
            }
            

        }, function (response){
        });
    };

//Bigbrother 규칙 리스트
 $scope.loadFilterListText = function () {
        $http.get('/bigbrother_sniper/api/bigbrother/filter/list/view/text/', {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            textFilter_list = response.data.textFilters;
            $scope.textFilters = [];
            for ( index in textFilter_list ) {
                $scope.textFilters.push(textFilter_list[index]);
            }

        }, function (response){
        });
    };

    //Bigbrother 규칙 리스트
 $scope.loadFilterListLabel = function () {
        $http.get('/bigbrother_sniper/api/bigbrother/filter/list/view/label/', {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            labelFilter_list = response.data.labelFilters;
            $scope.labelFilters = [];
            for ( index in labelFilter_list ) {
                $scope.labelFilters.push(labelFilter_list[index]);
            }

        }, function (response){
        });
    };

    //위치 삭제
   $scope.deleteLocationList = function(){
        $http.post('/bigbrother_sniper/api/delete/location/',{"id": deleteId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            $scope.loadListLocation();


        },function(response){
             $("#bigbrother-failed-modal").appendTo("body").modal();

        });

    };

    $scope.deleteAlertFilterText = function(){
        $http.post('/bigbrother_sniper/api/delete/alert/text/',{"id": deleteId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            $scope.loadListLocation();


        },function(response){
             $("#bigbrother-failed-modal").appendTo("body").modal();

        });

    };
     $scope.deleteAlertFilterLabel = function(){
        $http.post('/bigbrother_sniper/api/delete/alert/label/',{"id": deleteId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){

            $scope.loadListLocation();

        },function(response){
             $("#bigbrother-failed-modal").appendTo("body").modal();

        });

    };

    var deleteId;
        //위치 삭제 알림창
  $scope.clicklocationdelete = function(deleteTarget){

        deleteId = deleteTarget.id;
        $("#deletelocation").css("z-index", "9999");
        $("#deletelocation").appendTo("body").modal();
         }
  $scope.clickdelete = function(deleteTarget){
        deleteId = deleteTarget.id;
        $("#deleteText").css("z-index", "9999");
        $("#deleteText").appendTo("body").modal();
         }
  $scope.clickdelete2 = function(deleteTarget){
        deleteId = deleteTarget.id;
        $("#deleteLabel").css("z-index", "9999");
        $("#deleteLabel").appendTo("body").modal();
         }


/***

새로고침
*/
        var timeIntervalprocess = 0;
    $scope.startInterval = function () {
         //$interval.cancel(timeIntervalReset);

         timeIntervalReset = $interval(function () {

            if (timeIntervalprocess > 0){
                $interval.cancel(timeIntervalReset);
                timeIntervalprocess -= 1;
            }
            $scope.timeIntervalprocess += 1;
             $scope.loadFilterListLabel();
             $scope.loadFilterListText();
        }, 1000,5);
        $scope.timeIntervalReset();

    }
/***
***규칙 만들기
***/
    $scope.locationModalUp = function () {
            //selectedUuid=-1;
            $("#locationSetting").appendTo('body').modal();
        };
    var GlovalSelectedId;
    var GlovalSelectedUuid;
    var GlovalSelectedRange;
    var GlovalSelectedLocation;

    $scope.RuleModalUp = function (id, uuid, range, location) {
    GlovalSelectedId = id;
    GlovalSelectedUuid = uuid;
    GlovalSelectedRange = range;
    GlovalSelectedLocation = location;
        //selectedUuid=-1;
        $("#ruleSetting").appendTo('body').modal();
    };



$scope.createLocationMaker = function () {

            $("#beaconReachSetting").appendTo('body').modal();
            $http.post('/api/create/location/maker/', {"uuid": $scope.createLocationMaker.uuid, "location": $scope.createLocationMaker.location, "maxRange": $scope.createLocationMaker.maxRange},
            {
                headers: {
                    'Authorization' : token
                }

            }).then(function(response){

            if (response.data=="success")
            {
            $scope.createLocationMaker.uuid ="";
            $scope.createLocationMaker.maxRange = "";
            $scope.createLocationMaker.location = "";
            $scope.loadListLocation();
            //$scope.loadFilterListText();
            //$scope.loadFilterListLabel();
            //ruleMakerInputInit();
            }


            }, function (response){


            });



        };

    $scope.createRuleMaker = function () {
            var picRequest = false;
            if ($scope.createRuleMaker.picRequest){picRequest = $scope.createRuleMaker.picRequest;}
            $("#beaconReachSetting").appendTo('body').modal();
            $http.post('/api/create/rule/maker/', {"val": $scope.createRuleMaker.val,"drop_on_flag": $scope.createRuleMaker.dropFlag, "filter": $scope.createRuleMaker.filter, "explain": $scope.createRuleMaker.explain, "pk": GlovalSelectedId, "range":$scope.createRuleMaker.range, "picRequest": picRequest},
            {
                headers: {
                    'Authorization' : token
                }

            }).then(function(response){

            if (response.data=="success")
            {
            $scope.createRuleMaker.filter ="";
            $scope.createRuleMaker.explain = "";
            $scope.createRuleMaker.dropFlag = "";
            $scope.createRuleMaker.picRequest = "";
            $scope.createRuleMaker.val = "";
            $scope.createRuleMaker.range = "";
            $scope.selectedUuid = "";
            selectedUuidRange = -1;
            $scope.loadListLocation();
            //$scope.loadFilterListText();
            //$scope.loadFilterListLabel();
            //ruleMakerInputInit();
            }


            }, function (response){


            });



        };
/*
**비콘 목록 불러오기
*/
   $scope.beaconListView = function () {
        $http.get('/bigbrother_sniper/api/beacon/list/view/',
        {
            headers: {
                'Authorization' : token
            }

        }).then(function(response){
            Beacons = response.data;
            $scope.BeaconList = [];
            for ( index in Beacons)
                {
                    $scope.BeaconList.push(Beacons[index]);
                }
         },function (response){

         });




    };

/*
**규칙 설정 시 비콘 선택 이벤트
*/
    var selectedUuid;
    var selectedUuidRange;
    $scope.uuidListClick = function () {
    selectedUuid = $scope.selectedUuid;

        $http.post('/bigbrother_sniper/api/beacon/list/range/', {"id": selectedUuid},{
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            selectedUuidRange = response.data;
        }, function (response){
        });

    };


    $scope.ruleSettingAboutDialog = function() {


        var mLine = "";
        $scope.linebreak = function(text) {mLine = mLine + text};
                $scope.linebreak("<font size=\"5\">위치 : "+GlovalSelectedLocation+"</font><br>");
                $scope.linebreak("<font size=\"2\">UUID : "+GlovalSelectedUuid+"</font><br>");
                $scope.linebreak("<font size=\"3\">최대 반경 : "+GlovalSelectedRange+"cm</font>");
        if(GlovalSelectedRange==0){$scope.createRuleMaker.range = 0;}
        return $sce.trustAsHtml(mLine)



             };

    $scope.locationTable = function(location, uuid, range) {

        var mLine = "";
        $scope.linebreak = function(text) {mLine = mLine + text};

                $scope.linebreak("<th width=200>");
                       $scope.linebreak("위치 : "+location);
                $scope.linebreak("</th>");
                $scope.linebreak("<th width=400>");
                       $scope.linebreak("비콘 uuid : "+uuid);
                $scope.linebreak("</th>");
                $scope.linebreak("<th align=center width=150>");
                       $scope.linebreak("최대 반경 : "+range+"cm");
                $scope.linebreak("</th>");


        return $sce.trustAsHtml(mLine)

             };

    $scope.labelFilterTable = function(flag, label_value, explain, location, range, picRequest) {

        var mLine = "";
        $scope.linebreak = function(text) {mLine = mLine + text};
        var color;
        if (flag=="Drop")
            color="red";
        else
            color="yellow";

                $scope.linebreak("<th width=50>");
                    $scope.linebreak("<font style='background-color:"+color+"'>"+flag+"</font>");
                $scope.linebreak("</th>");
                $scope.linebreak("<th width=200>");
                       $scope.linebreak("제한 사물명 : "+label_value);
                $scope.linebreak("</th>");
                $scope.linebreak("<th width=200>");
                       $scope.linebreak("분야 : "+explain);
                $scope.linebreak("</th>");
                $scope.linebreak("<<th width=200>");
                       $scope.linebreak("반경 : "+range+"cm");
                $scope.linebreak("</th>");
                $scope.linebreak("<th>");
                       $scope.linebreak("사진 요청 : "+picRequest);
                $scope.linebreak("</th>");





        return $sce.trustAsHtml(mLine)

             };

    $scope.textFilterTable = function(flag, text_value, explain, location, range, picRequest) {

        var mLine = "";
        $scope.linebreak = function(text) {mLine = mLine + text};
        var color;
        if (flag=="Drop")
            color="red";
        else
            color="yellow";

                $scope.linebreak("<th width=50>");
                    $scope.linebreak("<font style='background-color:"+color+"'>"+flag+"</font>");
                $scope.linebreak("</th>");
                $scope.linebreak("<th width=200>");
                       $scope.linebreak("제한 텍스트 : "+text_value);
                $scope.linebreak("</th>");
                $scope.linebreak("<th width=200>");
                       $scope.linebreak("분야 : "+explain);
                $scope.linebreak("</th>");
                 $scope.linebreak("<<th width=200>");
                       $scope.linebreak("반경 : "+range+"cm");
                $scope.linebreak("</th>");
                $scope.linebreak("<th>");
                       $scope.linebreak("사진 요청 : "+picRequest);
                $scope.linebreak("</th>");





        return $sce.trustAsHtml(mLine)

             };
});



function onEnterSubmit(sw){
    if( sw == true){
     var keyCode = window.event.keyCode;
     document.getElementById("login-submit").click();
  }
}
function onEnter(){
        if(window.event.keyCode == 13)
        document.getElementById("login-submit").click();
}

function activeMyInfo() {
    localStorage.setItem('chulCheckActived',"20132308");
}
function activeChulCheck() {
    localStorage.setItem('chulCheckActived',"20132307");
}
function activeChulCheckList() {
    localStorage.setItem('chulCheckActived',"20132309");
}

function chulcheckJS() {
    const chulCheckInfo = localStorage.getItem('chulCheckActived');

    if (chulCheckInfo == "20132307") {
        $(document).ready(function(){
            $('#chul2').tab('show');
        });
    }
    else if (chulCheckInfo == "20132308") {
        $(document).ready(function(){
            $('#chul1').tab('show');
        });
    }
    else if(chulCheckInfo == "20132309") {
        $(document).ready(function(){
            $('#chul3').tab('show');
        });
    }
}

function ruleMakerInputInit(){
    document.beaconReachSetting.filter.value="";
}

app.controller('AlertInfoController_list', function($scope, $http){

   $scope.alertInfoListView = function () {
        $http.get('/bigbrother_sniper/api/alert/list/log/date/',
        {
            headers: {
                'Authorization' : token
            }

        }).then(function(response){
            LogDates = response.data;
            $scope.DateList = [];
            for ( index in LogDates)
                {
                    $scope.DateList.push(LogDates[index]);
                }
         },function (response){

         });




    };

    var selectedDate;
    $scope.alertInfoListViewClick = function () {
    selectedDate = $scope.selectedDate;
        $http.post('/bigbrother_sniper/api/alert/list/log/date/view/', {"date": $scope.selectedDate},{
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            alert_list = response.data;
            $scope.alerts = [];
            for ( index in alert_list ) {
                $scope.alerts.push(alert_list[index]);
            }

        }, function (response){
        });
    };

        var deleteId = 0;
        //알림 삭제창
      $scope.clickdelete = function(deleteTarget){

            deleteId = deleteTarget.id;
            $("#deleteLogCheck").css("z-index", "9999");
            $("#deleteLogCheck").appendTo("body").modal();
             }



     $scope.deleteAlertFilter = function(){
        $http.post('/bigbrother_sniper/api/delete/alert/log/',{"id": deleteId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
         $scope.alertInfoListViewClick();

        },function(response){


        });

    };

      //알림 전체 삭제
    $scope.alertAllDelete = function(){
            $("#deleteLogAllModal").css("z-index", "9999");
            $("#deleteLogAllModal").appendTo("body").modal();
             }


    $scope.alertAllDeleteStart = function(){
        $http.post('/bigbrother_sniper/api/delete/alert/log/all/', {"date":selectedDate},{
            headers: {
                'Authorization' : token
            }
        }).then(function(response){

        },function(response){

        });

    };

        var selectTarget = 0;
    $scope.clickpreview = function(selectTarget){
    selectId = selectTarget.id
        $http.post('/bigbrother_sniper/api/bigbrother/post/alert/message/list/preview/',{"id": selectId}, {
            headers: {
                'Authorization' : token
            }
        }).then(function(response){
            $scope.alertInfo = response.data;
            $("#ViewPictureLog").css("z-index", "9999");
            $("#ViewPictureLog").appendTo("body").modal();
        },function(response){

        });

    };
});










