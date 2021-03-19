import re
import json
import time
import logging

# Create your views here.
import django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


from PassPercentage.models import Platform
from PassPercentage.models import TestLoop
from PassPercentage.models import Comment
from PassPercentage.models import CaseDetail
from PassPercentage.models import AvocadoFeatureMapping

from PassPercentage.forms import CommentForm
from PassPercentage.forms import UserForm
from PassPercentage.forms import UserProfileForm
from PassPercentage.forms import AvocadoFeatureMappingForm
from PassPercentage import populate_data

from utils import create_datapoints_column
from utils import create_datapoints_area
from utils import create_datapoints_line
from utils import get_all_loop
from utils import display_test_details
from utils import create_datapoints_pie
from utils import get_avocado_feature_mapping

from utils_email import send_email


logger = logging.getLogger(__name__)


def homepage(request):
    print('The host info :', request.get_host())
    context_dict = {}
    context_dict['homepage_name'] = 'PassPercentage'
    platform = Platform.objects.order_by('-platform_name')[:]
    context_dict['platform_list'] = platform
    print(context_dict['platform_list'])

    for plat in platform:
        if plat:
            context_dict['ppc_loop_lists'], _ = get_all_loop(plat.platform_name)

    return render(request, 'PassPercentage/homepage.html', context_dict)


def about(request):
    context_dict = {}
    version = django.get_version()
    context_dict['version'] = version
    context_dict['author'] = 'yhong'
    print('The version of django : %s' % context_dict['version'])

    return render(request, 'PassPercentage/about.html', context_dict)


def show_testloops(request, platform_slug_name):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    test_loop = TestLoop.objects.filter(platform=platform)
    context_dict = {}
    context_dict['platforms'] = platform
    context_dict['test_loops'] = test_loop
    verbose = True
    if verbose:
        for test in test_loop:
            print('%s loop line info : [update time : %s, case pass nums : %s, '
                  'case total nums : %s , version: %s]' %
                  (test.loop_name, test.loop_updated_time.isoformat(' ').split('.')[0],
                   test.loop_case_pass_num, test.loop_case_total_num, test.loop_host_ver))

    return render(request, 'PassPercentage/testloop.html', context_dict)


def show_column_chart(request, platform_slug_name):
    context_dict = {}
    context_dict['xml_name'] = 'latest_columnpoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']
    platform, test_loops = create_datapoints_column(platform_slug_name, context_dict['xml_name'])
    context_dict['platforms'], context_dict['test_loops'] = platform, test_loops

    return render(request, 'PassPercentage/column_chart_from_xml.html', context_dict)


def display_lines_charts_from_column(request, platform_slug_name, loop_select_name_underline):
    context_dict = {}
    total_host_ver = set('')
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    context_dict['platforms'] = platform
    context_dict['xml_name'] = 'multi_linepoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    _, test_loops = get_all_loop(platform.platform_name)
    for loop in test_loops:
        total_host_ver.add(loop.loop_host_ver)

    total_host_ver = list(total_host_ver)
    print('the set of total_host_ver : ', total_host_ver)

    context_dict['loop_select_name'] = loop_select_name_underline.replace('_', ' ')
    context_dict['loop_select_name_nospace'] = loop_select_name_underline
    versions = create_datapoints_line(platform.platform_name,
                                      loop_select_name_underline,
                                      total_host_ver,
                                      context_dict['xml_name'], False)

    context_dict['test_host_ver'] = versions
    print('List of host version :', context_dict['test_host_ver'])

    return render(request, 'PassPercentage/multi-lines-chart_from_xml.html',  context_dict)


def display_area_chart(request, platform_slug_name, loop_select_name_underline, host_ver):
    platform = Platform.objects.get(platform_slug=platform_slug_name)
    context_dict = {}
    context_dict['platforms'] = platform

    context_dict['xml_name'] = 'multi_areapoints.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    print(platform_slug_name)
    print(loop_select_name_underline)
    host_ver = host_ver.replace('_', '.')
    print(host_ver)
    loop_select_name = loop_select_name_underline.replace('_', ' ')
    print('loop_select_name', loop_select_name)
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
    print(updated_time_list)
    updated_time_orgin = (updated_time_list[0] + ' ' + updated_time_list[1] +
                          '.' + updated_time_list[2] + '+' + updated_time_list[3])
    print(updated_time_orgin)
    context_dict = {}
    context_dict['platforms'] = platform

    context_dict['loop_name_no_underline'] = loop_select_name.replace('_',' ')
    context_dict['loop_select_name'] = loop_select_name
    context_dict['host_ver'] = host_ver
    context_dict['host_version'] = host_ver.replace('_','.')
    context_dict['x_point'] = x_point
    context_dict['updated_time'] = updated_time
    cases, fail, fail_percent = display_test_details(platform=platform,
                                                     loop_feature_name=loop_select_name,
                                                     failed_error=True,
                                                     verbose=False,
                                                     updated_time=updated_time_orgin)
    context_dict['fail'] = fail
    context_dict['fail_percent'] = fail_percent
    context_dict['cases'] = cases
    context_dict['xml_name'] = 'pie_points.xml'
    context_dict['dir_xml'] = 'xml/' + context_dict['xml_name']

    create_datapoints_pie(file_xml_name=context_dict['xml_name'],
                          dict=context_dict['fail_percent'])
    comment_form = CommentForm()
    if request.method == 'POST':
        if request.POST.get('request_action') == 'comment':
            request.POST['comment_user'] = request.POST.get('request_user')
            request.POST['comment_email'] = request.POST.get('request_email')
            request.POST['comment_context'] = request.POST.get('request_message')

            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                comment_form.save(commit=True)
                comment = Comment.objects.order_by("-comment_updated_time")[0]
                print(comment.comment_user, comment.comment_context)
                comment.comment_version = host_ver.replace('_', '.')
                comment.comment_platform = platform.platform_name
                comment.comment_point = x_point
                comment.comment_point_real_time = updated_time
                comment.comment_testloop = loop_select_name.replace('_', ' ')
                comment.save()

        if request.POST.get('request_action') == 'delete':
            user = request.POST.get('request_user')
            email = request.POST.get('request_email')
            message = request.POST.get('request_message')
            message += '\n%s' % ('=' * 80)
            message += "\nRequest user: %s" % user
            message += "\nRequest email: %s" % email
            http_host = request.META.get("HTTP_HOST")
            url = "http://" + http_host + request.path
            message += "\nRequest url: %s" % url
            target = ','.join((platform_slug_name, loop_select_name,
                              host_ver, x_point, updated_time))
            subject = ("%s requests to delete test loop@%s" % (user, target))
            send_email(subject, message)

    context_dict['comment_form'] = comment_form
    comments = Comment.objects.all().order_by("-comment_updated_time")[:]
    context_dict['comments'] = comments
    verbose = False
    if verbose:
        for comment in comments:
            print('comment user: %s; context: %s; updated time: %s' \
                  'version: %s; platform: %s; testloop: %s; point: %s' \
                  % (comment.comment_user, comment.comment_context,
                     comment.comment_updated_time, comment.comment_version,
                     comment.comment_platform, comment.comment_testloop,
                     comment.comment_point))

    return render(request, 'PassPercentage/comments.html', context_dict)


def server_api(request):
    name = 'unknown'
    tests = 'unknown'
    image_backend = 'unknown'
    image_format = 'unknown'
    qemu_ver = 'unknown'
    host_kernel_ver = 'unknown'
    host_ver = 'unknown'
    guest_kernel_ver = 'unknown'
    guest_ver = 'unknown'
    guest_plat = 'unknown'
    case_total_num = 0
    case_pass_num = 0
    cmd = 'unknown'

    context_dict = {}
    recevied_data = json.loads(request.body)
    recv_time = time.ctime()
    cases_id = []
    message = ''
    logger.info('Beijing time: %s, received data from client:' % recv_time)
    message += 'Beijing time: %s, received data from client:\n' % recv_time
    message += '%s\n' % ('=' * 80)
    logger.info('HTTP Request META:')
    message += 'HTTP Request META:\n'
    for key, val in request.META.items():
        logger.info("    %s: %s" % (key, val))
        message += "    %s: %s\n" % (key, val)

    logger.info('Test Loop Data:')
    message += '%s\n' % ('*' * 100)
    message += 'Test Loop Data:\n'
    message_cases = []
    for key, val in recevied_data.items():
        if key not in ('tests', 'feature', 'owner'):
            logger.info("    %s: %s" % (key, val))
            message += "    %s: %s\n" % (key, val)
        if key == 'host_arch':
            platform = val
            if not platform:
                platform = 'unknown'
        elif key == 'qemu_version':
            qemu_ver = val
            if not qemu_ver:
                qemu_ver = 'unknown'
        elif key == 'image_backend':
            image_backend = val
            if not image_backend:
                image_backend = 'unknown'
        elif key == 'image_format':
            image_format = val
            if not image_format:
                image_format = 'unknown'
        elif key == 'host_kernel_version':
            host_kernel_ver = val
            if not host_kernel_ver:
                host_kernel_ver = 'unknown'
        elif key == 'host_version':
            host_ver = val
            if not host_ver:
                host_ver = 'unknown'
        elif key == 'guest_version':
            guest_ver = val
            if not guest_ver:
                guest_ver = 'unknown'
        elif key == 'guest_arch':
            guest_plat = val
            if not guest_plat:
                guest_plat = 'unknown'
        elif key == 'virtio_win_version':
            virtio_win_ver = val
            if not virtio_win_ver:
                virtio_win_ver = 'none'
        elif key == 'total':
            case_total_num = val
            if not case_total_num:
                case_total_num = 0
        elif key == 'pass':
            case_pass_num = val
            if not case_pass_num:
                case_pass_num = 0
        elif key == 'staf_cml':
            cmd = val
            if not cmd:
                cmd = 'unknown'
        elif key == 'tests':
            tests = val
            for test in tests:
                message_cases.append("        id: %s\n" % test['id'])
                for k, v in test.items():
                    if k == 'id':
                        cases_id.append(v)
                    else:
                        message_cases.append("             %s: %s\n" % (k, v))
    if message_cases:
        message += "    test_cases:\n"
        for message_case in message_cases:
            message += message_case

    try:
        cmd_args = {}
        for args in cmd.split():
            if "=" in args:
                key = args.split('=')[0][2:]
                val = args.split('=')[-1]
                cmd_args[key] = val
                if ',' in val:
                    cmd_args[key] = set(val.split(','))

        # Update feature name by model AvocadoFeatureMapping
        feature = get_avocado_feature_mapping(cmd, cases_id)
        if feature:
            populate_data.add_platform(platform)
            platform = Platform.objects.get(platform_name=platform)

            # Replace the name of loop with loop_feature_name if the
            # attribute of loop_name is 'unknown'
            if name == 'unknown':
                name = cmd_args["category"]

            feature_name = feature.main_feature
            feature_owner = feature.owner

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
            test_id = populate_data.add_testid(loop=loop,
                                               test_id=loop.loop_updated_time)
            for test in tests:
                logger.info("       Case ID: %s" % test['id'])
                for key, val in test.items():
                    if key != 'id':
                        logger.info("           %s: %s" % (key, val))
                        if key == 'status':
                            case_status = val
                            if not case_status:
                                case_status = 'unknown'
                        elif key == 'fail_reason':
                            case_fail_reason = val
                            if not case_fail_reason:
                                case_fail_reason = 'unknown'
                        elif key == 'url':
                            case_url = val
                            if not case_url:
                                case_url = 'unknown'
                        elif key == 'whiteboard':
                            case_whiteboard = val
                            if not case_whiteboard:
                                case_whiteboard = 'unknown'
                        elif key == 'start':
                            case_start = val
                            if not case_start:
                                case_start = 'unknown'
                        elif key == 'logdir':
                            case_logdir = val
                            if not case_logdir:
                                case_logdir = 'unknown'
                        elif key == 'time':
                            case_time = val
                            if not case_time:
                                case_time = 'unknown'
                        elif key == 'test':
                            case_test = val
                            if not case_test:
                                case_test = 'unknown'
                        elif key == 'end':
                            case_end = val
                            if not case_end:
                                case_end = 'unknown'
                        elif key == 'logfile':
                            case_logfile = val
                            if not case_logfile:
                                case_logfile = 'unknown'
                    else:
                        case_id = val

                obj = CaseDetail(test_id=test_id,
                                 case_status=case_status,
                                 case_fail_reason=case_fail_reason,
                                 case_url=case_url,
                                 case_whiteboard=case_whiteboard,
                                 case_start=case_start,
                                 case_logdir=case_logdir,
                                 case_time=case_time,
                                 case_test=case_test,
                                 case_end=case_end,
                                 case_logfile=case_logfile,
                                 case_id=case_id)
                obj_list.append(obj)
            CaseDetail.objects.bulk_create(obj_list)
            end_time = time.time()
            done_time = time.ctime()
            total_time = end_time - start_time
            logger.info('Recevice time: %s - Done time: %s ; Total time: %s' %
                        (recv_time, done_time, total_time))
        else:
            if cases_id:
                logger.error('Loop %s(cmdline: %s) is not registered in '
                             'feature mapping, please check or register it in '
                             'http://$server_ip:$port/admin/PassPercentage/avocadofeaturemapping/',
                             cmd_args["category"], cmd)
            else:
                logger.error("No found test cases in loop %s(cmdline: %s)" %
                             (cmd_args["category"], cmd))

            message += '%s\n' % ('=' * 80)
            if message_cases:
                message += ("Failed reason: Loop %s(cmdline: %s) is not registered"
                            " in feature mapping" % (cmd_args["category"], cmd))
            else:
                message += ("Failed reason: No found test cases in loop "
                            "%s(cmdline: %s)" % (cmd_args["category"], cmd))
            subject = ('Failed to upload test loop "%s" '
                       'results at %s' % (cmd_args["category"], recv_time))
            send_email(subject, message)
    except Exception as e:
        logger.error(str(e))
    logger.info("=" * 50)

    return render(request, 'PassPercentage/homepage.html', context_dict)


def show_fail_pie_chart(request):
    pass


def register(request):
    registered = False
    print('method of request :%s' % request.method)

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            print('=== user %s' % user)

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        print('Creating a user form...')
        user_form = UserForm()
        print('Creating a User Profile form...')
        profile_form = UserProfileForm()

    return render(request, 'PassPercentage/register.html', {'user_form': user_form,
                                                            'profile_form': profile_form,
                                                            'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print('%s' % username)
        password = request.POST.get('password')
        print('%s' % password)

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print('%s login sucessfully!' % username)
                return HttpResponseRedirect(reverse('homepage'))
            else:
                print('%s login failed!' % username)
                return HttpResponse("Your Rango account is disabled.")

        else:
            print("Invaild login details : {0}, {1}".format(username, password))
            return HttpResponse('Invaild login details supplied.')

    else:
        return render(request, 'PassPercentage/login.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def settings(request):
    return render(request, 'PassPercentage/settings.html', {})


def set_avocado_feature_info_mapping(request):
    context_dict = {}

    feature_mappings = AvocadoFeatureMapping.objects.all()
    context_dict['feature_mappings'] = feature_mappings
    for feature_mapping in feature_mappings:
        print(feature_mapping.__dict__)

    if request.method == 'POST':
        feature_form = AvocadoFeatureMappingForm(data=request.POST)
        if feature_form.is_valid():
            feature_form.save(commit=True)
            feature_form.save()
    else:
        feature_form = AvocadoFeatureMappingForm()

    context_dict['feature_form'] = feature_form

    template_name = 'PassPercentage/set_avocado_feature_info_mapping.html'
    return render(request, template_name, context_dict)
