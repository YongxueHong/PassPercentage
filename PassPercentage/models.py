from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Platform(models.Model):
    platform_name = models.CharField(max_length=200, unique=True,
                                     help_text='Here is the platform')
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
    loop_image_backend = models.CharField(max_length=200, blank=True)
    loop_image_format = models.CharField(max_length=200, blank=True)
    loop_qemu_ver = models.CharField(max_length=200, blank=True)
    loop_host_kernel_ver = models.CharField(max_length=200, blank=True)
    loop_host_ver = models.CharField(max_length=200, blank=True)
    loop_guest_kernel_ver = models.CharField(max_length=200, blank=True)
    loop_guest_ver = models.CharField(max_length=200, blank=True)
    loop_guest_plat = models.CharField(max_length=200, blank=True)
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
        info = ':'.join((self.platform.platform_name, self.loop_name,
                         self.loop_feature_name, self.loop_feature_owner,
                         self.loop_cmd, str(self.loop_updated_time)))
        return info


class TestsID(models.Model):
    loop = models.ForeignKey(TestLoop)
    tests_id = models.CharField(max_length=200, blank=True)
    test_id_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.test_id_slug = slugify(self.tests_id)
        super(TestsID, self).save(*args, **kwargs)

    def __str__(self):
        info = (self.loop.platform.platform_name + ':' +
                self.loop.loop_name + ':' + self.tests_id)
        return info


class CaseDetail(models.Model):
    test_id = models.ForeignKey(TestsID)
    case_status = models.CharField(max_length=200, blank=True)
    case_fail_reason = models.CharField(max_length=10000, blank=True)
    case_url = models.CharField(max_length=500, blank=True)
    case_whiteboard = models.CharField(max_length=500, blank=True)
    case_start = models.CharField(max_length=500, blank=True)
    case_logdir = models.CharField(max_length=500, blank=True)
    case_time = models.CharField(max_length=500, blank=True)
    case_test = models.CharField(max_length=500, blank=True)
    case_end = models.CharField(max_length=500, blank=True)
    case_logfile = models.CharField(max_length=500, blank=True)
    case_id = models.CharField(max_length=500, blank=True)

    detail_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.detail_slug = slugify(self.case_url)
        super(CaseDetail, self).save(*args, **kwargs)

    def __str__(self):
        info = (self.test_id.loop.platform.platform_name + ':'
                + self.test_id.loop.loop_name + ':' + self.test_id.tests_id +
                ':' + self.case_url)
        return info


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
    account_picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    comment_user = models.CharField(max_length=100, blank=True)
    comment_email = models.EmailField(blank=True)
    comment_context = models.CharField(max_length=10000000, blank=True)
    comment_updated_time = models.DateTimeField('Comment published', auto_now=True)
    comment_platform = models.CharField(max_length=200, blank=True)
    comment_testloop = models.CharField(max_length=200, blank=True)
    comment_version = models.CharField(max_length=200, blank=True)
    comment_point = models.CharField(max_length=200, blank=True)
    comment_point_real_time = models.CharField(max_length=200, blank=True)
    comment_index = models.IntegerField(default=1)

    def __str__(self):
        info = ': '.join((self.comment_platform, self.comment_testloop,
                          self.comment_email, self.comment_version,
                          'T%s' % self.comment_point,
                          str(self.comment_updated_time),
                          self.comment_context))
        return info


class AvocadoFeatureMapping(models.Model):
    category = models.CharField(max_length=200, blank=False)
    configs = models.CharField(max_length=200, blank=True, default='null')
    owner = models.CharField(max_length=200, blank=False)
    main_feature = models.CharField(max_length=200, blank=False)
    sub_feature = models.CharField(max_length=200, blank=True, default='null')

    def save(self, *args, **kwargs):
        super(AvocadoFeatureMapping, self).save(*args, **kwargs)

    def __str__(self):
        category_info = "category: %s" % self.category
        configs_info = "configs: %s" % self.configs
        owner_info = "owner: %s" % self.owner
        main_feature_info = "main_feature: %s" % self.main_feature
        sub_feature_info = "sub_feature: %s" % self.sub_feature
        info = "; ".join((category_info, configs_info, owner_info,
                          main_feature_info, sub_feature_info))
        return info


class MemberInfo(models.Model):
    member_name = models.CharField(max_length=200, blank=True)
    kerbose_id = models.CharField(max_length=200, blank=True)
    member_email = models.CharField(max_length=200, blank=True)
    leader_email = models.CharField(max_length=200, blank=True)
    manager_email = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        super(MemberInfo, self).save(*args, **kwargs)

    def __str__(self):
        member_name = "member_name: %s" % self.member_name
        kerbose_id = "kerbose_id: %s" % self.kerbose_id
        member_email = "member_email: %s" % self.member_email
        leader_email = "leader_eamil: %s" % self.leader_email
        manager_email = "manager_eamil: %s" % self.manager_email
        info = "; ".join((member_name, kerbose_id, member_email,
                          leader_email, manager_email))
        return info
