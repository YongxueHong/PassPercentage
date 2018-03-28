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


def query_latest_loop(platform_name, verbose=True):
    test_loop = TestLoop.objects.filter(platform=platform_name)
    names = set('')
    loop_list = []
    latest_dict = {}

    for list in test_loop:
        names.add(list.loop_name)

    for list in names:
        loop = TestLoop.objects.filter(platform=platform_name).filter(loop_name=list).order_by("-loop_updated_time")[0]
        if verbose == True:
            print 'Latest %s loop column info : [update time : %s, case pass nums : %s, case total nums : %s , pass percent: %.2f]'\
                  %(loop, loop.loop_updated_time, loop.loop_case_pass_num, loop.loop_case_total_num,
                    float(loop.loop_case_pass_num * 100) /loop.loop_case_total_num)
        #print 'Test details: %s' % (str(loop.loop_test_details))
        loop_list.append(loop)
        latest_dict[loop.loop_name] = float(loop.loop_case_pass_num * 100) /loop.loop_case_total_num

    return latest_dict, loop_list

def create_datapoints_column(platform_name, file_xml_name):
    """

    :param platform_name:
    :param file_xml_name:
    :return:
    """
    platform = Platform.objects.get(platform_slug=platform_name)
    print 'Platform : %s' % (platform.platform_name)
    dict = {}
    test_loop = []
    dict, test_loop = query_latest_loop(platform_name=platform, verbose=True)
    context = ""
    context += "<data>\n"
    for (name, percent) in dict.items():
        context += "    <point>\n" \
                   "        <x>%s</x>\n" \
                   "        <y>%.2f</y>\n" \
                   "    </point>\n" %(name, percent)
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()

    return platform, test_loop

def create_datapoints_line(platform_name, test_loop_name, test_host_ver, file_xml_name, verbose=True):
    """
    :param platform_name:
    :param test_loop_name: This param is no any space char. since it stored with underline in xml.
    :param test_host_ver:
    :param file_xml_name:
    :param verbose:
    :return:
    """
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
        #print loop, type(loop), len(loop), ver
        if len(loop) == 0:
            loop = TestLoop.objects.filter(platform=platform).filter(loop_name=test_loop_name.replace('_', ' ')) \
                       .filter(loop_host_ver=ver).order_by(
                "loop_updated_time")[:]
        if loop:
            for list in loop:
                if verbose == True:
                    print 'Total %s loop line info : [update time : %s, case pass nums : %s, case total nums : %s , ' \
                          'pass percent : %.2f, version: %s]' \
                          % (list.loop_name, list.loop_updated_time.isoformat(' ').split('.')[0], list.loop_case_pass_num,
                             list.loop_case_total_num, (float(list.loop_case_pass_num * 100) / list.loop_case_total_num),
                             list.loop_host_ver)
                #print 'Test details <%s>: %s' % (type(str(list.loop_test_details)), str(list.loop_test_details))
            context += "    <%s>\n" % list.loop_host_ver.replace('.', '_').replace('-', '_')
            versions += list.loop_host_ver.replace('.', '_').replace('-', '_') + ','
            t = 0
            for list in loop:
                # Need to shit the loop_updated_time(stored in db with UTC timezone) to local time.
                #list.loop_updated_time_local = list.loop_updated_time + datetime.timedelta(hours=8)
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
                           "            <guest_plat>%s</guest_plat>\n" \
                           "            <virtio_win_ver>%s</virtio_win_ver>\n" \
                           "            <image_backend>%s</image_backend>\n" \
                           "            <image_format>%s</image_format>\n" \
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
                                                  list.loop_guest_plat,
                                                  list.loop_virtio_win_ver,
                                                  list.loop_image_backend,
                                                  list.loop_image_format,
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

def create_datapoints_area(platform_name, test_loop_name, host_version, file_xml_name):
    """

    :param platform_name:
    :param test_loop_name:
    :param host_version:
    :param file_xml_name:
    :return:
    """
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
        #list.loop_updated_time_local = list.loop_updated_time + datetime.timedelta(hours=8)
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


def create_datapoints_pie(file_xml_name, dict):
    context = ""
    context += "<data>\n"
    print dict
    for (name, percent) in dict.items():
        #print 'Pie member ==> %s, %s' %(name, percent)
        context += "    <point>\n" \
                   "        <x>%s</x>\n" \
                   "        <y>%s</y>\n" \
                   "    </point>\n" %(name, percent)
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()

def display_test_details(platform, loopname, updated_time, failed_error=False, verbose=True):
    testloop = TestLoop.objects.filter(platform=platform).filter(loop_name=loopname)\
        .filter(loop_updated_time=updated_time)

    if len(testloop) == 0:
        testloop = TestLoop.objects.filter(platform=platform).filter(loop_name=loopname.replace('_', ' ')) \
            .filter(loop_updated_time=updated_time)

    fail_dict = {}
    fail_dict['fail'] = {}
    fail_dict['error'] = {}
    fail_dict['cancel'] = {}
    fail_dict['skip'] = {}
    fail_dict['warn'] = {}
    fail_dict['interrupt'] = {}
    fail_dict['all'] = {}
    fail_dict['pass'] = {}

    fail_dict['fail']['fail_info'] = {}
    fail_dict['fail']['fail_cont'] = {}
    fail_dict['fail']['fail_percnet'] = {}

    fail_dict['error']['error_info'] = {}
    fail_dict['error']['error_cont'] = {}
    fail_dict['error']['error_percent'] = {}

    fail_dict['cancel']['cancel_info'] = {}
    fail_dict['cancel']['cancel_cont'] = {}
    fail_dict['cancel']['cancel_percent'] = {}

    fail_dict['skip']['skip_info'] = {}
    fail_dict['skip']['skip_cont'] = {}
    fail_dict['skip']['skip_percent'] = {}

    fail_dict['warn']['warn_info'] = {}
    fail_dict['warn']['warn_cont'] = {}
    fail_dict['warn']['warn_percent'] = {}

    fail_dict['interrupt']['interrupt_info'] = {}
    fail_dict['interrupt']['interrupt_cont'] = {}
    fail_dict['interrupt']['interrupt_percent'] = {}

    fail_dict['all']['all_info'] = {}
    fail_dict['all']['all_cont'] = {}

    fail_info_dict = {}
    fail_cont_dict = {}
    fail_percent_dict = {}

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
    fail_info = ''
    fail_cont = 0
    error_info = ''
    error_cont = 0
    cancel_info = ''
    cancel_cont = 0
    skip_info = ''
    skip_cont = 0
    warn_info = ''
    warn_cont = 0
    interrupt_info = ''
    interrupt_cont = 0
    all_info = ''
    all_cont = 0

    if failed_error == True:
        for case in cases:
            if re.findall(r'FAIL', case.case_status):
                fail_cont = fail_cont + 1
                fail_info +='Case ID:' +  case.case_id + '.\n' + 'Fail reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'ERROR', case.case_status):
                error_cont = error_cont + 1
                error_info +='Case ID:' +  case.case_id + '.\n' + 'Error reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'CANCEL', case.case_status):
                cancel_cont = cancel_cont + 1
                cancel_info +='Case ID:' +  case.case_id + '.\n' + 'Cancel reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'SKIP', case.case_status):
                skip_cont = skip_cont + 1
                skip_info +='Case ID:' +  case.case_id + '.\n' + 'Skip reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'WARN', case.case_status):
                warn_cont = warn_cont + 1
                warn_info +='Case ID:' +  case.case_id + '.\n' + 'Warn reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'INTERRUPT', case.case_status):
                interrupt_cont = interrupt_cont + 1
                interrupt_info +='Case ID:' +  case.case_id + '.\n' + 'Interrupt reason: ' + case.case_fail_reason + '.\n' + '\n'

    fail_info_dict['fail_info'] = fail_info
    fail_cont_dict['fail_cont'] = fail_cont
    fail_percent_dict['FAIL'] = float(fail_cont * 100) / testloop[0].loop_case_total_num
    fail_info_dict['error_info'] = error_info
    fail_cont_dict['error_cont'] = error_cont
    fail_percent_dict['ERROR'] = float(error_cont * 100) / testloop[0].loop_case_total_num
    fail_info_dict['cancel_info'] = cancel_info
    fail_cont_dict['cancel_cont'] = cancel_cont
    fail_percent_dict['CANCEL'] = float(cancel_cont * 100) / testloop[0].loop_case_total_num
    fail_info_dict['skip_info'] = skip_info
    fail_cont_dict['skip_cont'] = skip_cont
    fail_percent_dict['SKIP'] = float(skip_cont * 100) / testloop[0].loop_case_total_num
    fail_info_dict['warn_info'] = warn_info
    fail_cont_dict['warn_cont'] = warn_cont
    fail_percent_dict['WARN'] = float(warn_cont * 100) / testloop[0].loop_case_total_num
    fail_info_dict['interrupt_info'] = interrupt_info
    fail_cont_dict['interrupt_cont'] = interrupt_cont
    fail_percent_dict['INTERRUPT'] = float(interrupt_cont * 100) / testloop[0].loop_case_total_num
    #pass_count = total_case_num - fail_cont - error_cont - cancel_cont - skip_cont
    fail_percent_dict['PASS'] = float(testloop[0].loop_case_pass_num * 100) / testloop[0].loop_case_total_num

    fail_info_dict['all_info'] = fail_info + error_info + cancel_info + skip_info + warn_info + interrupt_info
    fail_cont_dict['all_cont'] = fail_cont + error_cont + cancel_cont + skip_cont + warn_cont + interrupt_cont

    # if not fail_info_dict['fail_info']:
    #     fail_info_dict['fail_info'] = 'No such cases.'
    # if not fail_info_dict['error_info']:
    #     fail_info_dict['error_info'] = 'No such cases.'
    # if not fail_info_dict['cancel_info']:
    #     fail_info_dict['cancel_info'] = 'No such cases.'
    # if not fail_info_dict['skip_info']:
    #     fail_info_dict['skip_info'] = 'No such cases.'
    # if not fail_info_dict['all_info']:
    #     fail_info_dict['all_info'] = 'All cases passed.'
    #
    for k, v in fail_info_dict.items():
        if not v:
            if k == 'all_info':
                fail_info_dict[k] = 'All cases passed.'
            else:
                fail_info_dict[k] = 'No such cases.'

    fail_dict['fail']['fail_info'] = fail_info_dict['fail_info']
    fail_dict['fail']['fail_cont'] = fail_cont_dict['fail_cont']
    fail_dict['fail']['fail_percnet'] = fail_percent_dict['FAIL']

    fail_dict['error']['error_info'] = fail_info_dict['error_info']
    fail_dict['error']['error_cont'] = fail_cont_dict['error_cont']
    fail_dict['error']['error_percent'] = fail_percent_dict['ERROR']

    fail_dict['cancel']['cancel_info'] = fail_info_dict['cancel_info']
    fail_dict['cancel']['cancel_cont'] = fail_cont_dict['cancel_cont']
    fail_dict['cancel']['cancel_percent'] = fail_percent_dict['CANCEL']

    fail_dict['skip']['skip_info'] = fail_info_dict['skip_info']
    fail_dict['skip']['skip_cont'] = fail_cont_dict['skip_cont']
    fail_dict['skip']['skip_percent'] = fail_percent_dict['SKIP']

    fail_dict['warn']['warn_info'] = fail_info_dict['warn_info']
    fail_dict['warn']['warn_cont'] = fail_cont_dict['warn_cont']
    fail_dict['warn']['warn_percent'] = fail_percent_dict['WARN']

    fail_dict['interrupt']['interrupt_info'] = fail_info_dict['interrupt_info']
    fail_dict['interrupt']['interrupt_cont'] = fail_cont_dict['interrupt_cont']
    fail_dict['interrupt']['interrupt_info_percent'] = fail_percent_dict['INTERRUPT']

    fail_dict['all']['all_info'] = fail_info_dict['all_info']
    fail_dict['all']['all_cont'] = fail_cont_dict['all_cont']

    fail_dict['pass']['pass_percent'] = fail_percent_dict['PASS']

    #print fail_dict

    return cases, fail_dict, fail_percent_dict
