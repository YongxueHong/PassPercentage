from django.shortcuts import render
import os, sys
# Create your views here.
import django
from django.contrib.auth.models import User
from PassPercentage.models import Platform, TestLoop, Name, Comment
from PassPercentage.forms import PlatformForm, TestLoopForm, LoopSelectForm, CommentForm, UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from utils import create_datapoints_column,create_datapoints_area, create_datapoints_line, query_latest_loop, get_all_loop
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


def homepage(request):
    print 'The host info :',request.get_host()
    context_dict = {}
    context_dict['homepage_name'] = 'PassPercentage'
    platform = Platform.objects.order_by('-platform_name')[:]
    context_dict['platform_list'] = platform
    print context_dict['platform_list']

    context_dict['ppc_loop_lists'] = get_all_loop('ppc')
    context_dict['x86_loop_lists'] = get_all_loop('x86')
    context_dict['arm_loop_lists'] = get_all_loop('arm')
    context_dict['s390x_loop_lists'] = get_all_loop('s390x')
    context_dict['virtio_win_loop_lists'] = get_all_loop('virtio-win')

    return render(request, 'PassPercentage/homepage.html', context_dict)

def about(request):
    context_dict = {}
    version = django.get_version()
    context_dict['version'] = version
    context_dict['author'] = 'yhong'
    print ('The version of django : %s' % context_dict['version'])

    return render(request, 'PassPercentage/about.html', context_dict)

def show_testloops(request, platform_slug_name):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    test_loop = TestLoop.objects.filter(platform=platform)
    context_dict = {}
    context_dict['platforms'] = platform
    context_dict['test_loops'] = test_loop
    for list in test_loop:
        print '%s loop line info : [update time : %s, case pass nums : %s, case total nums : %s , version: %s]' \
              % (list.loop_name, list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num,
                 list.loop_case_total_num,
                 list.loop_host_ver)

    return render(request, 'PassPercentage/testloop.html', context_dict)

def show_column_chart(request, platform_slug_name):
    context_dict = {}
    context_dict['xml_name'] = 'latest_columnpoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    context_dict['platforms'], context_dict['test_loops'] = create_datapoints_column(platform_slug_name, context_dict['xml_name'])

    return render(request, 'PassPercentage/column_chart_from_xml.html', context_dict)

def show_line_charts(request, platform_slug_name):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    context_dict = {}
    context_dict['platforms'] = platform
    context_dict['xml_name'] = 'multi_linepoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    host_ver = ['RHEL7.5', 'RHEL7.4']
    test_loop_name = 'acceptance'
    platform_name = 'ppc'

    context_dict['test_loop_name'] = test_loop_name
    versions = create_datapoints_line(platform_name, test_loop_name, host_ver, context_dict['xml_name'])
    test_loop = TestLoop.objects.filter(loop_name=test_loop_name)
    context_dict['test_loops'] = test_loop
    context_dict['test_host_ver'] = versions

    return render(request, 'PassPercentage/multi-series-line-chart_from_xml.html', context_dict)

def display_lines_charts(request, platform_slug_name):
    context_dict = {}
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    context_dict['platforms'] = platform
    context_dict['xml_name'] = 'multi_linepoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    if request.method == 'POST':
        form = LoopSelectForm(request.POST)
        if form.is_valid():
            loop_select_name = form.cleaned_data['loop_select_name']
            print 'Selected loop :', loop_select_name
    else:
        form = LoopSelectForm()

    loop_select_name_nospace = loop_select_name.replace(' ', '_')
    print 'loop select name no space :', loop_select_name_nospace

    total_host_ver = ['RHEL7.5', 'RHEL7.4', 'RHEL7.3']
    context_dict['loop_select_name'] = loop_select_name
    context_dict['loop_select_name_nospace'] = loop_select_name_nospace
    versions = create_datapoints_line(platform.platform_name, loop_select_name, total_host_ver, context_dict['xml_name'])

    print '+++',versions
    context_dict['test_host_ver'] = versions
    print '---', context_dict['test_host_ver']

    return render(request, 'PassPercentage/multi-lines-chart_from_xml.html',  context_dict)

def show_area_chart(request, platform_slug_name):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    test_loop = TestLoop.objects.filter(platform=platform)
    context_dict = {}
    context_dict['platforms'] = platform
    context_dict['test_loops'] = test_loop
    context_dict['xml_name'] = 'multi_areapoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    test_loop_name = 'acceptance'
    host_version = 'RHEL7.5'
    platform_name = 'x86'
    context_dict['host_version'] = host_version
    context_dict['test_loop_name'] = test_loop_name
    create_datapoints_area(platform_name, test_loop_name, host_version, context_dict['xml_name'])

    return render(request, 'PassPercentage/multi-series-area-chart_from_xml.html', context_dict)

def display_area_chart(request, platform_slug_name, loop_select_name, host_ver):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    #test_loop = TestLoop.objects.filter(platform=platform)
    context_dict = {}
    context_dict['platforms'] = platform

    context_dict['xml_name'] = 'multi_areapoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    print platform_slug_name
    print loop_select_name
    host_ver = host_ver.replace('_', '.')
    print host_ver
    loop_select_name = loop_select_name.replace('_', ' ')
    print 'loop_select_name', loop_select_name
    context_dict['host_version'] = host_ver
    context_dict['test_loop_name'] = loop_select_name
    create_datapoints_area(platform.platform_name, loop_select_name, host_ver, context_dict['xml_name'])

    return render(request, 'PassPercentage/multi-series-area-chart_from_xml.html', context_dict)

def comments(request, platform_slug_name, loop_select_name, host_ver, x_point):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    context_dict = {}
    context_dict['platforms'] = platform
    context_dict['loop_name_no_underline'] = loop_select_name.replace('_',' ')
    context_dict['loop_select_name'] = loop_select_name
    context_dict['host_ver'] = host_ver
    context_dict['host_version'] = host_ver.replace('_','.')
    context_dict['x_point'] = x_point
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            print 'form is valid'
            comment_form.save(commit=True)
            comment = Comment.objects.order_by("-comment_updated_time")[0]
            print comment.comment_user, comment.comment_title, comment.comment_context
            comment.comment_version = host_ver.replace('_','.')
            comment.comment_platform = platform.platform_name
            comment.comment_point = x_point
            comment.comment_testloop = loop_select_name.replace('_',' ')
            comment.save()
            """
            comment_user = comment_form.cleaned_data['comment_user']
            print 'comment_user :', comment_user
            comment_title = comment_form.cleaned_data['comment_title']
            print 'comment_title :', comment_title
            comment_context = comment_form.cleaned_data['comment_context']
            print 'comment_context :', comment_context
            """

    else:
        comment_form = CommentForm()

    context_dict['comment_form'] = comment_form
    comment = Comment.objects.all().order_by("-comment_updated_time")[:]
    context_dict['comments'] = comment
    #print  comment
    for list in comment:
        print 'comment user: %s; title: %s; context: %s; updated time: %s' \
              'version: %s; platform: %s; testloop: %s; point: %s' \
              %(list.comment_user, list.comment_title, list.comment_context, list.comment_updated_time,
                list.comment_version, list.comment_platform, list.comment_testloop, list.comment_point)

    return render(request, 'PassPercentage/comments.html', context_dict)

def register(request):
    registered = False

    print 'method of request :%s' % request.method

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            print '=== user %s' % user

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print (user_form.errors, profile_form.errors)
    else:
        print 'Creating a user form...'
        user_form = UserForm()
        print 'Creating a User Profile form...'
        profile_form = UserProfileForm()

    return render(request, 'PassPercentage/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print '%s' % username
        password = request.POST.get('password')
        print  '%s' % password

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print '%s login sucessfully!' % username
                return HttpResponseRedirect(reverse('homepage'))
            else:
                print '%s login failed!' % username
                return HttpResponse("Your Rango account is disabled.")

        else:
            print ("Invaild login details : {0}, {1}".format(username, password))
            return HttpResponse('Invaild login details supplied.')

    else:
        return render(request, 'PassPercentage/login.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))