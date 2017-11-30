import sys,os
from PassPercentage.models import Platform, TestLoop
from django.db.models import Count
import datetime
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
XML_DIR = os.path.join(STATIC_DIR, 'xml')

print BASE_DIR
print STATIC_DIR
print XML_DIR


def query_latest_loop(platform_name):
    test_loop = TestLoop.objects.filter(platform=platform_name)
    names = []
    loop_list = []
    latest_dict = {}

    for list in test_loop:
        names.append(list.loop_name)

    for list in set(names):
        loop = TestLoop.objects.filter(loop_name=list).order_by("-loop_updated_time")[0]
        print 'Latest %s loop column info : [update time : %s, case pass nums : %s, case total nums : %s , pass percentage: %.2f]'\
              %(loop, loop.loop_updated_time, loop.loop_case_pass_num, loop.loop_case_total_num,
                float(loop.loop_case_pass_num * 100) /loop.loop_case_total_num)
        loop_list.append(loop)
        latest_dict[loop.loop_name] = float(loop.loop_case_pass_num * 100) /loop.loop_case_total_num
        """
        print list
        index = 0
        for name in names:
            if (list == name):
                tmp_times.append(times[index])
            index = index + 1
            tmp_times.sort()
        print 'new times', tmp_times
        pos = 0
        for time in times:
            if (tmp_times[-1] == time):
                latest_dict[list] = percentages[pos]
                print 'pos', pos
                break
            pos = pos + 1
        tmp_times = []
        """
    return latest_dict, loop_list

def create_datapoints_column(platform_name, file_xml_name):
    platform = Platform.objects.get(platform_slug=platform_name)
    print 'Platform : %s' % (platform.platform_name)
    dict = {}
    test_loop = []
    dict, test_loop = query_latest_loop(platform)
    context = ""
    context += "<data>\n"
    for (name, percentage) in dict.items():
        context += "    <point>\n" \
                   "        <x>%s</x>\n" \
                   "        <y>%.2f</y>\n" \
                   "    </point>\n" %(name, percentage)
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()

    return platform, test_loop

def create_datapoints_line(platform_name,test_loop_name, test_host_ver, file_xml_name):
    context_dict = {}
    platform = Platform.objects.get(platform_slug=platform_name)
    context_dict['platforms'] = platform
    print 'Platform : %s' % (platform.platform_name)

    versions = ''
    context = ""
    context += "<data>\n"
    for ver in test_host_ver:
        loop = TestLoop.objects.filter(loop_name=test_loop_name).filter(loop_host_ver=ver).order_by(
            "loop_updated_time")[:]
        for list in loop:
            print '%s loop line info : [update time : %s, case pass nums : %s, case total nums : %s , version: %s]' \
                  % (list.loop_name, list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num, list.loop_case_total_num,
                     list.loop_host_ver)
        context += "    <%s>\n" % list.loop_host_ver.replace('.', '_').replace('-', '_')
        versions += list.loop_host_ver.replace('.', '_').replace('-', '_') + ','
        t = 0
        for list in loop:
            context += "        <point>\n" \
                       "            <x>T%d</x>\n" \
                       "            <y>%.2f</y>\n" \
                       "        </point>\n" %(t, (float(list.loop_case_pass_num * 100)/list.loop_case_total_num))
            t = t + 1
        context += "    </%s>\n" % list.loop_host_ver.replace('.', '_').replace('-', '_')
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()
    print 'list of versions :',versions
    return versions

def create_datapoints_area(platform_name,test_loop_name, host_version, file_xml_name):
    context_dict = {}
    platform = Platform.objects.get(platform_slug=platform_name)
    context_dict['platforms'] = platform
    print 'Platform : %s' %(platform.platform_name)

    loop = TestLoop.objects.filter(platform=platform).filter(loop_name=test_loop_name).filter(loop_host_ver=host_version).order_by("loop_updated_time")[:]
    for list in loop:
        print '%s loop area info : [update time : %s, case pass nums : %s, case total nums : %s , version: %s]' \
              % (list.loop_name, list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num, list.loop_case_total_num,
                 list.loop_host_ver)
    context = ""
    context += "<data>\n"
    context += "    <pass>\n"
    for list in loop:
        context += "        <point>\n" \
                   "            <x>%s</x>\n" \
                   "            <y>%s</y>\n" \
                   "        </point>\n" %(list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num)
    context += "    </pass>\n"
    context += "    <total>\n"
    for list in loop:
        context += "        <point>\n" \
                   "            <x>%s</x>\n" \
                   "            <y>%s</y>\n" \
                   "        </point>\n" %(list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_total_num)
    context += "    </total>\n"
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()
