import os
import re
import collections
import logging

from PassPercentage.models import Platform
from PassPercentage.models import TestLoop
from PassPercentage.models import TestsID
from PassPercentage.models import CaseDetail
from PassPercentage.models import AvocadoFeatureMapping

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
XML_DIR = os.path.join(STATIC_DIR, 'xml')

print(BASE_DIR)
print(STATIC_DIR)
print(XML_DIR)


logger = logging.getLogger(__name__)


def get_avocado_feature_mapping_by_cmd(loop_cmd):
    feature_mappings = AvocadoFeatureMapping.objects.all()
    features = []
    matched_feature = None
    cmd_args = {}

    for args in loop_cmd.split():
        if "=" in args:
            key = args.split('=')[0][2:]
            val = args.split('=')[-1]
            cmd_args[key] = val
            if ',' in val:
                cmd_args[key] = set(val.split(','))

    for feature in feature_mappings:
        if cmd_args['category'] == feature.category:
            features.append(feature)

    if features:
        if len(features) == 1:
            matched_feature = features[0]
        elif len(features) > 1:
            for feature in features:
                config_args = {}
                for config in feature.configs.split():
                    if "=" in config:
                        key = config.split('=')[0][2:]
                        val = config.split('=')[-1]
                        config_args[key] = val
                        if ',' in val:
                            config_args[key] = set(val.split(','))
                for key, val in config_args.items():
                    if key not in cmd_args or val != cmd_args[key]:
                        break
                else:
                    matched_feature = feature
        if matched_feature:
            return matched_feature
    return None


def update_testloop_model_by_avocado_feature_mapping(test_loop):
    feature = get_avocado_feature_mapping_by_cmd(test_loop.loop_cmd)
    if feature:
        test_loop.loop_feature_name = feature.main_feature
        test_loop.loop_feature_owner = feature.owner
        test_loop.save(update_fields=['loop_feature_name', 'loop_feature_owner'])
        return True
    return False


def query_latest_loop(platform_name, verbose=True):
    test_loop = TestLoop.objects.filter(platform=platform_name)
    names = set('')
    loop_list = []
    latest_dict = {}

    for test in test_loop:
        names.add(test.loop_name)

    for name in names:
        loop = TestLoop.objects.filter(platform=platform_name).filter(
                loop_name=name).order_by("-loop_updated_time")[0]
        if verbose:
            print('Latest %s loop column info : [update time : %s, '
                  'case pass nums : %s, case total nums : %s , '
                  'pass percent: %.2f]' % (loop.loop_feature_name, loop.loop_updated_time,
                                           loop.loop_case_pass_num,
                                           loop.loop_case_total_num,
                                           (float(loop.loop_case_pass_num * 100)
                                            / loop.loop_case_total_num)))
        if loop.loop_case_total_num != 0:
            loop_list.append(loop)
            latest_dict[loop.loop_feature_name] = (float(loop.loop_case_pass_num * 100)
                                           / loop.loop_case_total_num)
    return collections.OrderedDict(sorted(latest_dict.items())), loop_list


def create_datapoints_column(platform_name, file_xml_name):
    """
    :param platform_name:
    :param file_xml_name:
    :return:
    """
    platform = Platform.objects.get(platform_slug=platform_name)
    print('Platform : %s' % platform.platform_name)
    dict, test_loop = query_latest_loop(platform_name=platform, verbose=True)
    context = ""
    context += "<data>\n"
    for (name, percent) in dict.items():
        context += "    <point>\n" \
                   "        <x>%s</x>\n" \
                   "        <y>%.2f</y>\n" \
                   "    </point>\n" % (name, percent)
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    if not os.path.exists(XML_DIR):
        os.makedirs(XML_DIR)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()

    return platform, test_loop


def create_datapoints_line(platform_name, test_loop_feature_name, test_host_ver,
                           file_xml_name, verbose=True):
    """
    :param platform_name:
    :param test_loop_feature_name: This param is no any space char. since it stored with underline in xml.
    :param test_host_ver:
    :param file_xml_name:
    :param verbose:
    :return:
    """
    context_dict = {}
    platform = Platform.objects.get(platform_slug=platform_name)
    context_dict['platforms'] = platform
    print('Platform : %s' % platform.platform_name)
    versions = ''
    context = ""
    context += "<data>\n"
    for ver in test_host_ver:
        loops = TestLoop.objects.filter(platform=platform).filter(
                loop_feature_name=test_loop_feature_name).filter(
                loop_host_ver=ver).order_by("loop_updated_time")[:]
        if len(loops) == 0:
            loop = TestLoop.objects.filter(platform=platform).filter(
                    loop_feature_name=test_loop_feature_name.replace('_', ' ')).filter(
                    loop_host_ver=ver).order_by("loop_updated_time")[:]
        if loops:
            for loop in loops:
                if verbose:
                    print('Total %s loop line info : [update time : %s, '
                          'case pass nums : %s, case total nums : %s , '
                          'pass percent : %.2f, version: %s]' %
                          (loop.loop_feature_name,
                           loop.loop_updated_time.isoformat(' ').split('.')[0],
                           loop.loop_case_pass_num,
                           loop.loop_case_total_num,
                           (float(loop.loop_case_pass_num * 100) / loop.loop_case_total_num),
                           loop.loop_host_ver))
            context += "    <%s>\n" % loop.loop_host_ver.replace('.', '_').replace('-', '_')
            versions += loop.loop_host_ver.replace('.', '_').replace('-', '_') + ','
            t = 0
            for loop in loops:
                # Need to shit the loop_updated_time(stored in db with UTC timezone) to local time.
                #list.loop_updated_time_local = list.loop_updated_time + datetime.timedelta(hours=8)
                if loop.loop_case_total_num != 0:
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
                               "        </point>\n" % (t,
                                                       (float(loop.loop_case_pass_num * 100)/loop.loop_case_total_num),
                                                       loop.loop_case_pass_num,
                                                       loop.loop_case_total_num,
                                                       loop.loop_feature_owner,
                                                       loop.loop_qemu_ver,
                                                       loop.loop_host_kernel_ver,
                                                       loop.loop_host_ver,
                                                       loop.loop_guest_kernel_ver,
                                                       loop.loop_guest_ver,
                                                       loop.loop_guest_plat,
                                                       loop.loop_virtio_win_ver,
                                                       loop.loop_image_backend,
                                                       loop.loop_image_format,
                                                       loop.loop_cmd,
                                                       loop.loop_updated_time
                                                       )
                    t = t + 1
            context += "    </%s>\n" % loop.loop_host_ver.replace('.', '_').replace('-', '_')
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    if not os.path.exists(XML_DIR):
        os.makedirs(XML_DIR)
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
    print('Platform : %s' %(platform.platform_name))

    loops = TestLoop.objects.filter(platform=platform).filter(
            loop_name=test_loop_name).filter(
            loop_host_ver=host_version).order_by("loop_updated_time")[:]
    for loop in loops:
        print('%s loop area info : [update time : %s, case pass nums : %s, '
              'case total nums : %s , version: %s]' %
              (loop.loop_name, loop.loop_updated_time.isoformat(' ').split('.')[0],
               loop.loop_case_pass_num,
               loop.loop_case_total_num, loop.loop_host_ver))
    context = ""
    context += "<data>\n"
    context += "    <pass>\n"
    for loop in loops:
        context += "        <point>\n" \
                   "            <x>%s</x>\n" \
                   "            <y>%s</y>\n" \
                   "        </point>\n" % (loop.loop_updated_time.isoformat(' ').split('.')[0],
                                           loop.loop_case_pass_num)
    context += "    </pass>\n"
    context += "    <total>\n"
    for loop in loops:
        context += "        <point>\n" \
                   "            <x>%s</x>\n" \
                   "            <y>%s</y>\n" \
                   "        </point>\n" % (loop.loop_updated_time.isoformat(' ').split('.')[0],
                                           loop.loop_case_total_num)
    context += "    </total>\n"
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    if not os.path.exists(XML_DIR):
        os.makedirs(XML_DIR)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()


def get_all_loop(platform_name):
    loop_name = set('')
    platform = Platform.objects.get(platform_name=platform_name)

    testloop_list = TestLoop.objects.filter(platform=platform)
    for testloop in testloop_list:
        loop_name.add(testloop.loop_name)

    total_loop = list(loop_name)

    if not total_loop:
        total_loop.append('No loops')
        print('%s no loops' % platform_name)
    else:
        print('total loop of %s: %s' % (platform_name, total_loop))
    return total_loop, testloop_list


def display_meta(request):
    values = request.META.items()
    values.sort()
    for key, val in values:
        print('key: %s, val: %s' % (key, val))


def create_datapoints_pie(file_xml_name, dict):
    context = ""
    context += "<data>\n"
    print(dict)
    for (name, percent) in dict.items():
        context += "    <point>\n" \
                   "        <x>%s</x>\n" \
                   "        <y>%s</y>\n" \
                   "    </point>\n" %(name, percent)
    context += "</data>"

    file_xml = os.path.join(XML_DIR, file_xml_name)
    if not os.path.exists(XML_DIR):
        os.makedirs(XML_DIR)
    file = open(file_xml, "w")
    file.writelines(context)
    file.close()


def display_test_details(platform, loop_feature_name, updated_time,
                         failed_error=False, verbose=True):
    testloop = TestLoop.objects.filter(platform=platform).filter(
            loop_feature_name=loop_feature_name).filter(loop_updated_time=updated_time)

    if len(testloop) == 0:
        testloop = TestLoop.objects.filter(platform=platform).filter(
                loop_feature_name=loop_feature_name.replace('_', ' ')).filter(
                loop_updated_time=updated_time)

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
    print('test id : ', testid)
    cases = CaseDetail.objects.filter(test_id=testid)
    if verbose:
        for case in cases:
            print('=============================================')
            print('status:', case.case_status)
            print('fail_reason:', case.case_fail_reason)
            print('url:', case.case_url)
            print('whiteboard:', case.case_whiteboard)
            print('start:', case.case_start)
            print('logdir:', case.case_logdir)
            print('time:', case.case_time)
            print('test:', case.case_test)
            print('end:', case.case_end)
            print('logfile:', case.case_logfile)
            print('id:', case.case_id)
    pass_info = ''
    pass_cont = 0
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

    if failed_error:
        for case in cases:
            if re.findall(r'PASS', case.case_status):
                pass_cont = pass_cont + 1
                all_cont = all_cont + 1
                pass_info +='Case ID:' + case.case_id + '.\n'
                all_info += 'Case ID:' + case.case_id + '.\n'

            if re.findall(r'FAIL', case.case_status):
                fail_cont = fail_cont + 1
                all_cont = all_cont + 1
                fail_info +='Case ID:' + case.case_id + '.\n' + 'Fail reason: ' + case.case_fail_reason + '.\n' + '\n'
                all_info += 'Case ID:' + case.case_id + '.\n' + 'Fail reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'ERROR', case.case_status):
                error_cont = error_cont + 1
                all_cont = all_cont + 1
                error_info +='Case ID:' + case.case_id + '.\n' + 'Error reason: ' + case.case_fail_reason + '.\n' + '\n'
                all_info += 'Case ID:' + case.case_id + '.\n' + 'Error reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'CANCEL', case.case_status):
                cancel_cont = cancel_cont + 1
                all_cont = all_cont + 1
                cancel_info +='Case ID:' + case.case_id + '.\n' + 'Cancel reason: ' + case.case_fail_reason + '.\n' + '\n'
                all_info += 'Case ID:' + case.case_id + '.\n' + 'Cancel reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'SKIP', case.case_status):
                skip_cont = skip_cont + 1
                all_cont = all_cont + 1
                skip_info +='Case ID:' + case.case_id + '.\n' + 'Skip reason: ' + case.case_fail_reason + '.\n' + '\n'
                all_info += 'Case ID:' + case.case_id + '.\n' + 'Skip reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'WARN', case.case_status):
                warn_cont = warn_cont + 1
                all_cont = all_cont + 1
                warn_info +='Case ID:' + case.case_id + '.\n' + 'Warn reason: ' + case.case_fail_reason + '.\n' + '\n'
                all_info += 'Case ID:' + case.case_id + '.\n' + 'Warn reason: ' + case.case_fail_reason + '.\n' + '\n'

            if re.findall(r'INTERRUPT', case.case_status):
                interrupt_cont = interrupt_cont + 1
                all_cont = all_cont + 1
                interrupt_info +='Case ID:' + case.case_id + '.\n' + 'Interrupt reason: ' + case.case_fail_reason + '.\n' + '\n'
                all_info += 'Case ID:' + case.case_id + '.\n' + 'Interrupt reason: ' + case.case_fail_reason + '.\n' + '\n'

    fail_info_dict['pass_info'] = pass_info
    fail_cont_dict['pass_cont'] = pass_cont
    fail_percent_dict['PASS'] = float(pass_cont * 100) / testloop[0].loop_case_total_num
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
    fail_info_dict['all_info'] = all_info
    fail_cont_dict['all_cont'] = all_cont

    actual_cont = fail_cont + error_cont + cancel_cont + skip_cont + warn_cont + interrupt_cont + pass_cont
    if testloop[0].loop_case_total_num > actual_cont:
        unknown_cont = testloop[0].loop_case_total_num - actual_cont
        fail_percent_dict['UNKNOWN'] = (float(unknown_cont * 100) /
                                        testloop[0].loop_case_total_num)

    fail_dict['pass']['pass_info'] = fail_info_dict['pass_info']
    fail_dict['pass']['pass_cont'] = fail_cont_dict['pass_cont']
    fail_dict['pass']['pass_info_percent'] = fail_percent_dict['PASS']

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

    return cases, fail_dict, fail_percent_dict
