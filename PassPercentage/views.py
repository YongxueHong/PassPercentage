from django.shortcuts import render
import os, sys
# Create your views here.
import django
from django.contrib.auth.models import User
from PassPercentage.models import Platform, TestLoop, Name
from PassPercentage.forms import PlatformForm, TestLoopForm, LoopSelectForm
from django.http import HttpResponse, HttpResponseRedirect
from utils import create_datapoints_column,create_datapoints_area, create_datapoints_line, query_latest_loop


def homepage(request):
    print 'The host info :',request.get_host()
    context_dict = {}
    context_dict['homepage_name'] = 'PassPercentage'
    platform = Platform.objects.order_by('-platform_name')[:]
    context_dict['platform_list'] = platform
    print context_dict['platform_list']

    context_dict['loop_lists'] = ['usb device', 'virtual block device', 'qcow2',
                                  'acceptance', 'numa', 'kdump', 'virtual nic device', 'timer device']

    print context_dict['loop_lists']

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
    test_loop_name = 'qcow'
    platform_name = 'x86'

    context_dict['test_loop_name'] = test_loop_name
    versions = create_datapoints_line(platform_name, test_loop_name, host_ver, context_dict['xml_name'])
    test_loop = TestLoop.objects.filter(loop_name=test_loop_name)
    context_dict['test_loops'] = test_loop

    print '+++',versions
    context_dict['test_host_ver'] = versions
    print '---', context_dict['test_host_ver']

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

    total_host_ver = ['RHEL7.5', 'RHEL7.4', 'RHEL7.3']
    context_dict['loop_select_name'] = loop_select_name
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
    platform_name = 'ppc'
    context_dict['host_version'] = host_version
    context_dict['test_loop_name'] = test_loop_name
    create_datapoints_area(platform_name, test_loop_name, host_version, context_dict['xml_name'])

    return render(request, 'PassPercentage/multi-series-area-chart_from_xml.html', context_dict)