from django.contrib import admin
from PassPercentage.models import Platform, TestLoop, Name, Comment

# Register your models here.
class PlatformAdmin(admin.ModelAdmin):
    prepopulated_fields = {'platform_slug':('platform_name',)}

class TestLoopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'loop_slug':('loop_name',)}


admin.site.register(Platform, PlatformAdmin)
admin.site.register(TestLoop, TestLoopAdmin)
admin.site.register(Name)
admin.site.register(Comment)