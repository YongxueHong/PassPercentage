from django.shortcuts import render
import os, sys
import re
import json
# Create your views here.
import django
from django.contrib.auth.models import User
from PassPercentage.models import Platform, TestLoop, Name, Comment, CaseDetail, TestsID
from PassPercentage.forms import PlatformForm, TestLoopForm, LoopSelectForm, CommentForm, UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from utils import create_datapoints_column,create_datapoints_area, create_datapoints_line, \
    query_latest_loop, get_all_loop, display_test_details, create_datapoints_pie
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from PassPercentage import populate_data
import time, datetime

def homepage(request):
    print 'The host info :',request.get_host()
    context_dict = {}
    context_dict['homepage_name'] = 'PassPercentage'
    platform = Platform.objects.order_by('-platform_name')[:]
    context_dict['platform_list'] = platform
    print context_dict['platform_list']

    for plat in platform:
        if plat:
            context_dict['ppc_loop_lists'], _ = get_all_loop(plat.platform_name)

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
    verbose = True
    if verbose == True:
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

def display_lines_charts_from_column(request, platform_slug_name, loop_select_name_underline):
    context_dict = {}
    total_host_ver = set('')
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    context_dict['platforms'] = platform
    context_dict['xml_name'] = 'multi_linepoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    #loop_select_name = loop_select_name_underline.replace('_', ' ')

    _, test_loops = get_all_loop(platform.platform_name)
    for loop in test_loops:
        total_host_ver.add(loop.loop_host_ver)

    total_host_ver = list(total_host_ver)
    print 'the set of total_host_ver : ', total_host_ver

    context_dict['loop_select_name'] = loop_select_name_underline.replace('_', ' ')
    context_dict['loop_select_name_nospace'] = loop_select_name_underline
    #versions = create_datapoints_line(platform.platform_name, loop_select_name, total_host_ver, context_dict['xml_name'])
    versions = create_datapoints_line(platform.platform_name, loop_select_name_underline, total_host_ver,
                                      context_dict['xml_name'], False)

    context_dict['test_host_ver'] = versions
    print 'List of host version :', context_dict['test_host_ver']

    return render(request, 'PassPercentage/multi-lines-chart_from_xml.html',  context_dict)

def display_area_chart(request, platform_slug_name, loop_select_name_underline, host_ver):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    #test_loop = TestLoop.objects.filter(platform=platform)
    context_dict = {}
    context_dict['platforms'] = platform

    context_dict['xml_name'] = 'multi_areapoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    print platform_slug_name
    print loop_select_name_underline
    host_ver = host_ver.replace('_', '.')
    print host_ver
    loop_select_name = loop_select_name_underline.replace('_', ' ')
    print 'loop_select_name', loop_select_name
    context_dict['host_version'] = host_ver
    context_dict['test_loop_name'] = loop_select_name
    create_datapoints_area(platform_name=platform.platform_name, test_loop_name=loop_select_name_underline,
                           host_version=host_ver, file_xml_name=context_dict['xml_name'])

    return render(request, 'PassPercentage/multi-series-area-chart_from_xml.html', context_dict)

def comments(request, platform_slug_name, loop_select_name, host_ver, x_point, updated_time):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    updated_time_list = re.split(r'_', updated_time)
    updated_time_list[1] = re.sub(r'-', ':', updated_time_list[1])
    updated_time_list[3] = re.sub(r'-', ':', updated_time_list[3])
    print updated_time_list
    updated_time_orgin = updated_time_list[0] + ' ' + updated_time_list[1] + \
                   '.' + updated_time_list[2] + '+' + updated_time_list[3]
    print  updated_time_orgin
    fail_err_info = ''
    context_dict = {}
    context_dict['platforms'] = platform

    context_dict['loop_name_no_underline'] = loop_select_name.replace('_',' ')
    context_dict['loop_select_name'] = loop_select_name
    context_dict['host_ver'] = host_ver
    context_dict['host_version'] = host_ver.replace('_','.')
    context_dict['x_point'] = x_point
    context_dict['updated_time'] = updated_time
    cases, fail, fail_percent = display_test_details(platform=platform, loopname=loop_select_name,
                                       failed_error=True, verbose=False, updated_time=updated_time_orgin)
    #print fail
    context_dict['fail'] = fail
    # context_dict['fail_info'] = fail_info
    # context_dict['fail_cont'] = fail_cont
    context_dict['fail_percent'] = fail_percent
    context_dict['cases'] = cases
    context_dict['xml_name'] = 'pie_points.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    create_datapoints_pie(file_xml_name=context_dict['xml_name'], dict=context_dict['fail_percent'])

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #print 'form is valid'
            comment_form.save(commit=True)
            comment = Comment.objects.order_by("-comment_updated_time")[0]
            print comment.comment_user, comment.comment_context
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
    verbose = False
    if verbose == True:
        for list in comment:
            print 'comment user: %s; context: %s; updated time: %s' \
                  'version: %s; platform: %s; testloop: %s; point: %s' \
                  %(list.comment_user, list.comment_context, list.comment_updated_time,
                    list.comment_version, list.comment_platform, list.comment_testloop, list.comment_point)

    return render(request, 'PassPercentage/comments.html', context_dict)

def server_api(request):
    verbose = True
    name = 'unknown'
    tests = 'unknown'
    feature_name = 'unknown'
    feature_owner = 'unknown'
    image_backend = 'unknown'
    image_format = 'unknown'
    qemu_ver = 'unknown'
    host_kernel_ver = 'unknown'
    host_ver = 'unknown'
    guest_kernel_ver = 'unknown'
    guest_ver = 'unknown'
    guest_plat = 'unknown'
    #virtio_win_ver = 'unknown'
    case_total_num = 0
    case_pass_num = 0
    cmd = 'unknown'

    context_dict = {}
    datas = json.loads(request.body)
    recv_time = time.ctime()
    print 'Beijing %s : Received data from client.' % (recv_time)
    for key, val in datas.items():
        if key == 'host_arch':
            platform = val
            if not platform:
                platform = 'unknown'
            #print ('key: %s, val: %s' %(key, platform))
        elif key == 'feature':
            feature_name = val
            if not feature_name:
                feature_name = 'unknown'
            #print ('key: %s, val: %s' % (key, feature_name))
        elif key == 'qemu_version':
            qemu_ver = val
            if not qemu_ver:
                qemu_ver = 'unknown'
            #print ('key: %s, val: %s' % (key, qemu_ver))
        elif key == 'owner':
            feature_owner = val
            if not feature_owner:
                feature_owner = 'unknown'
            #print ('key: %s, val: %s' % (key, feature_owner))
        elif key == 'image_backend':
            image_backend = val
            if not image_backend:
                image_backend = 'unknown'
            #print ('key: %s, val: %s' % (key, image_backend))
        elif key == 'image_format':
            image_format = val
            if not image_format:
                image_format = 'unknown'
            #print ('key: %s, val: %s' % (key, image_format))
        elif key == 'host_kernel_version':
            host_kernel_ver = val
            if not host_kernel_ver:
                host_kernel_ver = 'unknown'
            #print ('key: %s, val: %s' % (key, host_ver))
        elif key == 'host_version':
            host_ver = val
            if not host_ver:
                host_ver = 'unknown'
            #print ('key: %s, val: %s' % (key, host_ver))
        elif key == 'guest_version':
            guest_ver = val
            if not guest_ver:
                guest_ver = 'unknown'
            #print ('key: %s, val: %s' % (key, guest_ver))
        elif key == 'guest_arch':
            guest_plat = val
            if not guest_plat:
                guest_plat = 'unknown'
            #print ('key: %s, val: %s' % (key, guest_plat))
        elif key == 'virtio_win_version':
            virtio_win_ver = val
            if not virtio_win_ver:
                virtio_win_ver = 'none'
            #print ('key: %s, val: %s' % (key, virtio_win_ver))
        elif key == 'total':
            case_total_num = val
            if not case_total_num:
                case_total_num = 0
            #print ('key: %s, val: %s' % (key, case_total_num))
        elif key == 'pass':
            case_pass_num = val
            #print val, type(val)
            if not case_pass_num:
                case_pass_num = 0
            #print ('key: %s, val: %s' % (key, case_pass_num))
        elif key == 'staf_cml':
            cmd = val
            if not cmd:
                cmd = 'unknown'
            #print ('key: %s, val: %s' % (key, cmd))
        elif key == 'tests':
            tests = val
            #print type(tests)
            if not tests:
                tests = 'unknown'
            #print ('key: %s, val: %s' % (key, tests))

    populate_data.add_platform(platform)
    platform = Platform.objects.get(platform_name=platform)
    # Replace the name of loop with loop_feature_name if the attribute of loop_name is 'unknown
    if name == 'unknown':
        name = feature_name

    loop = populate_data.add_testloop(platform=platform,
                             name=name,
                             feature_name=feature_name,
                             feature_owner=feature_owner,
                             image_backend=image_backend,
                             image_format=image_format,
                             qemu_ver=qemu_ver,
                             host_kernel_ver=host_kernel_ver,
                             host_ver=host_ver,
                             guest_kernel_ver=guest_kernel_ver,
                             guest_ver=guest_ver,
                             guest_plat=guest_plat,
                             virtio_win_ver=virtio_win_ver,
                             case_total_num=case_total_num,
                             case_pass_num=case_pass_num,
                             cmd=cmd)

    case_status = 'unknown'
    case_fail_reason = 'unknown'
    case_url = 'unknown'
    case_whiteboard = 'unknown'
    case_start = 'unknown'
    case_logdir = 'unknown'
    case_time = 'unknown'
    case_test = 'unknown'
    case_end = 'unknown'
    case_logfile = 'unknown'
    case_id = 'unknown'

    obj_list = []
    start_time = time.time()
    test_id = populate_data.add_testid(loop=loop, id=loop.loop_updated_time)
    for t in tests:
        print '--------------------------------------------------------------------------------'
        for key, val in t.items():
            #print ('key: %s, val: %s' % (key, val))
            if key == 'status':
                case_status = val
                if not case_status:
                    case_status = 'unknown'
                print ('key: %s, val: %s' % (key, case_status))
            elif key == 'fail_reason':
                case_fail_reason = val
                if not case_fail_reason:
                    case_fail_reason = 'unknown'
                print ('key: %s, val: %s' % (key, case_fail_reason))
            elif key == 'url':
                case_url = val
                if not case_url:
                    case_url = 'unknown'
                print ('key: %s, val: %s' % (key, case_url))
            elif key == 'whiteboard':
                case_whiteboard = val
                if not case_whiteboard:
                    case_whiteboard = 'unknown'
                #print ('key: %s, val: %s' % (key, case_whiteboard))
            elif key == 'start':
                case_start = val
                if not case_start:
                    case_start = 'unknown'
                #print ('key: %s, val: %s' % (key, case_start))
            elif key == 'logdir':
                case_logdir = val
                if not case_logdir:
                    case_logdir = 'unknown'
                #print ('key: %s, val: %s' % (key, case_logdir))
            elif key == 'time':
                case_time = val
                if not case_time:
                    case_time = 'unknown'
                #print ('key: %s, val: %s' % (key, case_time))
            elif key == 'test':
                case_test = val
                if not case_test:
                    case_test = 'unknown'
                #print ('key: %s, val: %s' % (key, case_test))
            elif key == 'end':
                case_end = val
                if not case_end:
                    case_end = 'unknown'
                #print ('key: %s, val: %s' % (key, case_end))
            elif key == 'logfile':
                case_logfile = val
                if not case_logfile:
                    case_logfile = 'unknown'
                #print ('key: %s, val: %s' % (key, case_logfile))
            elif key == 'id':
                case_id = val
                if not case_id:
                    case_id = 'unknown'
                #print ('key: %s, val: %s' % (key, case_logfile))

        obj = CaseDetail(test_id=test_id, case_status=case_status, case_fail_reason=case_fail_reason,
                                   case_url=case_url, case_whiteboard=case_whiteboard, case_start=case_start,
                                   case_logdir=case_logdir, case_time=case_time, case_test=case_test,
                                   case_end=case_end, case_logfile=case_logfile, case_id=case_id)
        obj_list.append(obj)
    CaseDetail.objects.bulk_create(obj_list)
    end_time = time.time()
    done_time = time.ctime()
    total_time = end_time - start_time

    if verbose == True:
        print '======================  Summary  ================================='
        for key, val in datas.items():
            if key != 'tests':
                print ('key: %s, val: %s' % (key, val))
            #print ('key: %s, val: %s' % (key, val))

    print 'Recevice time : %s - Done time : %s ; Total time of finished : %s' %(recv_time, done_time, total_time)

    return render(request, 'PassPercentage/homepage.html', context_dict)

def show_fail_pie_chart(request):
    pass

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