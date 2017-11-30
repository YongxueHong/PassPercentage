from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Platform(models.Model):
    platform_name = models.CharField(max_length=200, unique=True, help_text='Here is the platform')
    platform_slug = models.SlugField()

    class Meta:
        verbose_name = 'Automation_Platform'
        verbose_name_plural = 'platforms'

    def save(self, *args, **kwargs):
        self.platform_slug = slugify(self.platform_name)
        super(Platform, self).save(*args, **kwargs)

    def __str__(self):
        return self.platform_name

class TestLoop(models.Model):
    platform = models.ForeignKey(Platform)
    loop_name = models.CharField(max_length=200, blank=True)
    loop_feature_name = models.CharField(max_length=200, blank=True)
    loop_feature_owner = models.CharField(max_length=200, blank=True)
    loop_qemu_ver = models.CharField(max_length=200, blank=True)
    loop_host_kernel_ver = models.CharField(max_length=200, blank=True)
    loop_host_ver = models.CharField(max_length=200, blank=True, help_text="Please use the following format: eg:rhel7.4")
    loop_guest_kernel_ver = models.CharField(max_length=200, blank=True)
    loop_guest_ver = models.CharField(max_length=200, blank=True,help_text="Please use the following format: eg:rhel7.4")
    loop_case_total_num = models.IntegerField(default=0, blank=True)
    loop_case_pass_num = models.IntegerField(default=0, blank=True)
    loop_cmd = models.CharField(max_length=200, blank=True)
    loop_updated_time = models.DateTimeField('Data published', auto_now=True)
    loop_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.loop_slug = slugify(self.loop_name)
        super(TestLoop, self).save(*args, **kwargs)

    def __str__(self):
        return self.loop_name
