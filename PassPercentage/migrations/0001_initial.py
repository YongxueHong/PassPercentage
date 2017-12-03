# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-12-03 14:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_user', models.CharField(blank=True, max_length=100)),
                ('comment_email', models.EmailField(blank=True, max_length=254)),
                ('comment_title', models.CharField(blank=True, max_length=10000)),
                ('comment_context', models.CharField(blank=True, max_length=10000000)),
                ('comment_updated_time', models.DateTimeField(auto_now=True, verbose_name='Comment published')),
                ('comment_platform', models.CharField(blank=True, max_length=200)),
                ('comment_testloop', models.CharField(blank=True, max_length=200)),
                ('comment_version', models.CharField(blank=True, max_length=200)),
                ('comment_point', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_name', models.CharField(blank=True, max_length=100)),
                ('your_name_slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_name', models.CharField(help_text='Here is the platform', max_length=200, unique=True)),
                ('platform_slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Automation_Platform',
                'verbose_name_plural': 'platforms',
            },
        ),
        migrations.CreateModel(
            name='TestLoop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loop_name', models.CharField(blank=True, max_length=200)),
                ('loop_feature_name', models.CharField(blank=True, max_length=200)),
                ('loop_feature_owner', models.CharField(blank=True, max_length=200)),
                ('loop_qemu_ver', models.CharField(blank=True, max_length=200)),
                ('loop_host_kernel_ver', models.CharField(blank=True, max_length=200)),
                ('loop_host_ver', models.CharField(blank=True, help_text='Please use the following format: eg:rhel7.4', max_length=200)),
                ('loop_guest_kernel_ver', models.CharField(blank=True, max_length=200)),
                ('loop_guest_ver', models.CharField(blank=True, help_text='Please use the following format: eg:rhel7.4', max_length=200)),
                ('loop_case_total_num', models.IntegerField(blank=True, default=0)),
                ('loop_case_pass_num', models.IntegerField(blank=True, default=0)),
                ('loop_cmd', models.CharField(blank=True, max_length=200)),
                ('loop_updated_time', models.DateTimeField(auto_now=True, verbose_name='Data published')),
                ('loop_slug', models.SlugField()),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PassPercentage.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
