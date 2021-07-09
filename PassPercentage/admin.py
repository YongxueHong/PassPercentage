from django.contrib import admin
from PassPercentage.models import Platform
from PassPercentage.models import TestLoop
from PassPercentage.models import Name
from PassPercentage.models import Comment
from PassPercentage.models import TestsID
from PassPercentage.models import CaseDetail
from PassPercentage.models import AvocadoFeatureMapping
from PassPercentage.models import MemberInfo


# Register your models here.
class PlatformAdmin(admin.ModelAdmin):
    prepopulated_fields = {'platform_slug': ('platform_name',)}


class TestLoopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'loop_slug': ('loop_name',)}
    search_fields = ('loop_name', 'loop_feature_name',
                     'loop_feature_owner', 'loop_cmd',
                     'loop_updated_time')


class AvocadoFeatureMappingAdmin(admin.ModelAdmin):
    search_fields = ('category', 'configs',
                     'owner', 'main_feature',
                     'sub_feature')


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('comment_user', 'comment_email',
                     'comment_context', 'comment_updated_time',
                     'comment_platform', 'comment_testloop',
                     'comment_version', 'comment_point_real_time')


class MemberInfoAdmin(admin.ModelAdmin):
    search_fields = ('member_name', 'kerbose_id',
                     'member_email', 'leader_email',
                     'manager_email')


admin.site.register(Platform, PlatformAdmin)
admin.site.register(TestLoop, TestLoopAdmin)
admin.site.register(Name)
admin.site.register(Comment, CommentAdmin)
admin.site.register(TestsID)
admin.site.register(CaseDetail)
admin.site.register(AvocadoFeatureMapping, AvocadoFeatureMappingAdmin)
admin.site.register(MemberInfo, MemberInfoAdmin)
