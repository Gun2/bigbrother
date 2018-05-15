from django.contrib import admin
from bigbrother_sniper.models import (
                                     AdminProfile,
                                     EmployeeProfile,
                                     TextGuardList,
                                     LabelGuardList,
                                     PostAlertMessageLog,
                                     GuardOrUtilImageSavezone,
                                     DateRecord,
                                     LocationList,
                                     UserActiveLog,

                                     )

# Register your models here.
#admin.site.register(AdminProfile)
#admin.site.register(EmployeeProfile)
#admin.site.register(ProfileImage)
admin.site.register(TextGuardList)
admin.site.register(LabelGuardList)
admin.site.register(PostAlertMessageLog)
admin.site.register(GuardOrUtilImageSavezone)
admin.site.register(DateRecord)
admin.site.register(LocationList)
admin.site.register(UserActiveLog)



