import sys,os,re
from PassPercentage.models import Platform, TestLoop, TestsID, CaseDetail
from django.db.models import Count
import datetime
from django.utils import timezone
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
XML_DIR = os.path.join(STATIC_DIR, 'xml')

print BASE_DIR
print STATIC_DIR
print XML_DIR


def query_latest_loop(platform_name):
    test_loop = TestLoop.objects.filter(platform=platform_name)
    names = set('')
    loop_list = []
    latest_dict = {}

    for list in test_loop:
        names.add(list.loop_name)

    for list in names:
        loop = TestLoop.objects.filter(loop_name=list).order_by("-loop_updated_time")[0]
        print 'Latest %s loop column info : [update time : %s, case pass nums : %s, case total nums : %s , pass percentage: %.2f]'\
              %(loop, loop.loop_updated_time, loop.loop_case_pass_num, loop.loop_case_total_num,
                float(loop.loop_case_pass_num * 100) /loop.loop_case_total_num)
        #print 'Test details: %s' % (str(loop.loop_test_details))
        loop_list.append(loop)
        latest_dict[loop.loop_name] = float(loop.loop_case_pass_num * 100) /loop.loop_case_total_num

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

def create_datapoints_line(platform_name, test_loop_name, test_host_ver, file_xml_name):
    context_dict = {}
    platform = Platform.objects.get(platform_slug=platform_name)
    context_dict['platforms'] = platform
    print 'Platform : %s' % (platform.platform_name)

    versions = ''
    context = ""
    context += "<data>\n"
    for ver in test_host_ver:
        loop = TestLoop.objects.filter(platform=platform).filter(loop_name=test_loop_name) \
                   .filter(loop_host_ver=ver).order_by(
            "loop_updated_time")[:]
        if loop:
            for list in loop:
                print 'Total %s loop line info : [update time : %s, case pass nums : %s, case total nums : %s , ' \
                      'pass percentage : %.2f, version: %s]' \
                      % (list.loop_name, list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num,
                         list.loop_case_total_num, (float(list.loop_case_pass_num * 100) / list.loop_case_total_num),
                         list.loop_host_ver)
                #print 'Test details <%s>: %s' % (type(str(list.loop_test_details)), str(list.loop_test_details))
            context += "    <%s>\n" % list.loop_host_ver.replace('.', '_').replace('-', '_')
            versions += list.loop_host_ver.replace('.', '_').replace('-', '_') + ','
            t = 0
            for list in loop:
                context += "        <point>\n" \
                           "            <x>T%d</x>\n" \
                           "            <y>%.2f</y>\n" \
                           "            <pass_num>%d</pass_num>\n" \
                           "            <total_num>%d</total_num>\n" \
                           "            <feature_owner>%s</feature_owner>\n" \
                           "            <qemu_ver>%s</qemu_ver>\n" \
                           "            <host_kernel_ver>%s</host_kernel_ver>\n" \
                           "            <host_ver>%s</host_ver>\n" \
                           "            <guest_kernel_ver>%s</guest_kernel_ver>\n" \
                           "            <guest_ver>%s</guest_ver>\n" \
                           "            <virtio_win_ver>%s</virtio_win_ver>\n" \
                           "            <cmd>%s</cmd>\n" \
                           "            <updated_time>%s</updated_time>\n" \
                           "        </point>\n" %(t,
                                                  (float(list.loop_case_pass_num * 100)/list.loop_case_total_num),
                                                  list.loop_case_pass_num,
                                                  list.loop_case_total_num,
                                                  list.loop_feature_owner,
                                                  list.loop_qemu_ver,
                                                  list.loop_host_kernel_ver,
                                                  list.loop_host_ver,
                                                  list.loop_guest_kernel_ver,
                                                  list.loop_guest_ver,
                                                  list.loop_virtio_win_ver,
                                                  list.loop_cmd,
                                                  list.loop_updated_time
                                                  )
                t = t + 1
            context += "    </%s>\n" % list.loop_host_ver.replace('.', '_').replace('-', '_')
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()
    return versions

def create_datapoints_area(platform_name,test_loop_name, host_version, file_xml_name):
    context_dict = {}
    platform = Platform.objects.get(platform_slug=platform_name)
    context_dict['platforms'] = platform
    print 'Platform : %s' %(platform.platform_name)

    loop = TestLoop.objects.filter(platform=platform).filter(loop_name=test_loop_name) \
               .filter(loop_host_ver=host_version).order_by("loop_updated_time")[:]
    for list in loop:
        print '%s loop area info : [update time : %s, case pass nums : %s, case total nums : %s , version: %s]' \
              % (list.loop_name, list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num,
                 list.loop_case_total_num, list.loop_host_ver)
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

def get_all_loop(platform_name):
    loop_name = set('')
    total_loop = []
    platform = Platform.objects.get(platform_name=platform_name)

    testloop_list = TestLoop.objects.filter(platform=platform)
    for testloop in testloop_list:
        loop_name.add(testloop.loop_name)

    total_loop = list(loop_name)

    if not total_loop:
        total_loop.append('No loops')
        print '%s no loops' % platform_name
    else:
        print 'total loop of %s: %s' %(platform_name, total_loop)
    return total_loop, testloop_list

def display_meta(request):
    values = request.META.items()
    values.sort()
    for key, val in values:
        print ('key: %s, val: %s' % (key, val))

def display_test_details(platform, loopname, updated_time, failed_error=False, verbose=True):
    testloop = TestLoop.objects.filter(platform=platform).filter(loop_name=loopname)\
        .filter(loop_updated_time=updated_time)
    fail_err_dict = {}
    fail_err_info = ''
    testid = TestsID.objects.filter(tests_id=updated_time)
    print 'test id : ', testid
    cases = CaseDetail.objects.filter(test_id=testid)
    if verbose == True:
        for case in cases:
            print '============================================='
            print 'status:', case.case_status
            print 'fail_reason:', case.case_fail_reason
            print 'url:', case.case_url
            print 'whiteboard:', case.case_whiteboard
            print 'start:', case.case_start
            print 'logdir:', case.case_logdir
            print 'time:', case.case_time
            print 'test:', case.case_test
            print 'end:', case.case_end
            print 'logfile:', case.case_logfile
            print 'id:', case.case_id
    if failed_error == True:
        for case in cases:
            if not re.findall(r'PASS', case.case_status):
                fail_err_info +='Case ID:' +  case.case_id + '.\n' + 'Fail reason: ' + case.case_fail_reason + '.\n' + '\n'
    return cases, fail_err_info

def check_attr_value(atrr):
    pass