from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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
    loop_test_details = models.CharField(max_length=9999999999999, blank=True)
    loop_feature_name = models.CharField(max_length=200, blank=True)
    loop_feature_owner = models.CharField(max_length=200, blank=True)
    loop_image_backend = models.CharField(max_length=200, blank=True)
    loop_qemu_ver = models.CharField(max_length=200, blank=True)
    loop_host_kernel_ver = models.CharField(max_length=200, blank=True)
    loop_host_ver = models.CharField(max_length=200, blank=True)
    loop_guest_kernel_ver = models.CharField(max_length=200, blank=True)
    loop_guest_ver = models.CharField(max_length=200, blank=True)
    loop_virtio_win_ver = models.CharField(max_length=200, blank=True)
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

class Name(models.Model):
    your_name = models.CharField(max_length=100, blank=True)
    your_name_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.your_name_slug = slugify(self.your_name)
        super(Name, self).save(*args, **kwargs)

    def __str__(self):
        return self.your_name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #website = models.URLField(blank=True)
    account_picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    comment_user = models.CharField(max_length=100,blank=True)
    comment_email = models.EmailField(blank=True)
    #comment_title = models.CharField(max_length=10000,blank=True)
    comment_context = models.CharField(max_length=10000000,blank=True)
    comment_updated_time = models.DateTimeField('Comment published', auto_now=True)
    comment_platform = models.CharField(max_length=200, blank=True)
    comment_testloop = models.CharField(max_length=200, blank=True)
    comment_version = models.CharField(max_length=200, blank=True)
    comment_point = models.CharField(max_length=200, blank=True)
    comment_index = models.IntegerField(default=1)

    def __str__(self):
        return self.comment_updated_time