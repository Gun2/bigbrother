from django.contrib import admin
from bigbrother_sniper.models import (
                                     ProfessorProfile,
                                     StudentProfile,
                                     Department,
                                     ProfileImage,
                                     TextGuardList,
                                     LabelGuardList,
                                     PostAlertMessageLog,
                                     GuardOrUtilImageSavezone
                                     )

# Register your models here.
#admin.site.register(ProfessorProfile)
#admin.site.register(StudentProfile)
#admin.site.register(Department)
#admin.site.register(ProfileImage)
admin.site.register(TextGuardList)
admin.site.register(LabelGuardList)
admin.site.register(PostAlertMessageLog)
admin.site.register(GuardOrUtilImageSavezone)