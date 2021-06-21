import os
import re
import collections
import logging
import unicodedata

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


def get_avocado_feature_mapping(loop_cmd, cases_id):
    cmd_args = {}

    for args in loop_cmd.split():
        if "=" in args:
            key = args.split('=')[0][2:]
            val = args.split('=')[-1]
            cmd_args[key] = val
            if ',' in val:
                cmd_args[key] = set(val.split(','))

    category = cmd_args['category']
    target_feature_mappings = AvocadoFeatureMapping.objects.filter(category=category)

    all_case_configs = []
    found_info = 'Found loop cmd "%s" feature mapping in AvocadoFeatureMapping(%s)'
    if target_feature_mappings:
        for case_id in cases_id:
            all_case_configs.extend(case_id.split('.'))

        if len(target_feature_mappings) == 1:
            logger.info(found_info % (loop_cmd, target_feature_mappings[0]))
            return target_feature_mappings[0]
        elif len(target_feature_mappings) > 1:
            candidate_features = []
            for target_feature_mapping in target_feature_mappings:
                feature_configs = []
                for config in target_feature_mapping.configs.split():
                    if "=" in config:
                        key = config.split('=')[0][2:]
                        val = config.split('=')[-1]
                        if ',' in val:
                            for _ in val.split(','):
                                feature_configs.append(_)
                        else:
                            if 'hostname' == key:
                                # Add hostname options name to feature_configs
                                feature_configs.append(key)
                            elif 'guestname' == key:
                                # Add guestname options name to feature_configs
                                feature_configs.append(key)
                            else:
                                feature_configs.append(val)
                if feature_configs:
                    _matched = True
                    for feature_config in feature_configs:
                        if feature_config in ('hostname', 'guestname'):
                            if feature_config not in loop_cmd:
                                _matched = False
                                break
                        else:
                            if feature_config not in all_case_configs:
                                _matched = False
                    if _matched:
                        candidate_features.append(target_feature_mapping)
                else:
                    candidate_features.append(target_feature_mapping)

            if candidate_features:
                if len(candidate_features) == 1:
                    logger.info(found_info % (loop_cmd, candidate_features[0]))
                    return candidate_features[0]
                else:
                    configs_owner_main_feature = set()
                    for _ in candidate_features:
                        configs_owner_main_feature.add((_.configs, _.owner, _.main_feature))
                    if len(configs_owner_main_feature) == 1:
                        logger.info(found_info % (loop_cmd, candidate_features[0]))
                        return candidate_features[0]
                    else:
                        # workaround: maybe the kar options also as a part of case name
                        # like: virtio_net.Guest.xx.io-github-autotest-qemu.qemu_option_check.spapr-vlan.
                        # compare the owner and main feature among candidate_features
                        owner_main_feature = set()
                        for _ in configs_owner_main_feature:
                            owner_main_feature.add((_[1], _[2]))
                        if len(owner_main_feature) == 1:
                            # default get the index 0
                            logger.warn('Get the first feature mapping from '
                                        'candidate feature mappings: %s for %s,'
                                        ' since their owner and main feature are'
                                        'same.'
                                        % (candidate_features, category))
                            return candidate_features[0]
                        logger.warn('No found feature mapping in '
                                    'AvocadoFeatureMapping for "%s", '
                                    'candidate feature mappings: %s' %
                                    (category, candidate_features))
                        return None
            else:
                logger.warn('No found feature mapping configs in '
                            'AvocadoFeatureMapping for "%s": %s' %
                            (category, target_feature_mappings))
                return None
    else:
        logger.warn('No found category "%s" in AvocadoFeatureMapping' % category)
        return None


def update_testloop_model_by_avocado_feature_mapping(test_loop):
    test_id = TestsID.objects.get(loop=test_loop)
    case_details = CaseDetail.objects.filter(test_id=test_id)
    cases_id = [_.case_id for _ in case_details]
    feature = get_avocado_feature_mapping(test_loop.loop_cmd, cases_id)
    if feature:
        test_loop.loop_feature_name = feature.main_feature
        test_loop.loop_feature_owner = feature.owner
        test_loop.save(update_fields=['loop_feature_name', 'loop_feature_owner'])
        return True
    return False


def get_pass_percent(loop):
    total_case_denominator = 0
    test_id = TestsID.objects.get(loop=loop)
    cases = CaseDetail.objects.filter(test_id=test_id)

    # just involve pass fail error and interrupt as denominator
    # to caculate pass ratio
    for case in cases:
        if re.findall(r'PASS', case.case_status):
            total_case_denominator = total_case_denominator + 1
        if re.findall(r'FAIL', case.case_status):
            total_case_denominator = total_case_denominator + 1
        if re.findall(r'ERROR', case.case_status):
            total_case_denominator = total_case_denominator + 1
        if re.findall(r'INTERRUPT', case.case_status):
            total_case_denominator = total_case_denominator + 1

    if total_case_denominator == 0:
        pass_percent = 0.0
    else:
        pass_percent = float(
                loop.loop_case_pass_num * 100) / total_case_denominator
    return pass_percent


def query_latest_loop(platform_name, verbose=True):
    test_loop = TestLoop.objects.filter(platform=platform_name)
    feature_names = set('')
    loop_list = []
    latest_dict = {}

    for test in test_loop:
        feature_names.add(test.loop_feature_name)

    for feature_name in feature_names:
        loop = TestLoop.objects.filter(platform=platform_name).filter(
                loop_feature_name=feature_name).order_by("-loop_updated_time")[0]
        pass_percent = get_pass_percent(loop)
        if verbose:
            print('Latest %s loop column info : [update time : %s, '
                  'case pass nums : %s, case total nums : %s , '
                  'pass percent: %.2f]' % (loop.loop_feature_name, loop.loop_updated_time,
                                           loop.loop_case_pass_num,
                                           loop.loop_case_total_num,
                                           pass_percent))
        if loop.loop_case_total_num != 0:
            loop_list.append(loop)
            latest_dict[loop.loop_feature_name] = pass_percent
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
                pass_percent = get_pass_percent(loop)
                if verbose:
                    print('Total %s loop line info : [update time : %s, '
                          'case pass nums : %s, case total nums : %s , '
                          'pass percent : %.2f, version: %s]' %
                          (loop.loop_feature_name,
                           loop.loop_updated_time.isoformat(' ').split('.')[0],
                           loop.loop_case_pass_num,
                           loop.loop_case_total_num,
                           pass_percent, loop.loop_host_ver))
            context += "    <%s>\n" % loop.loop_host_ver.replace('.', '_').replace('-', '_')
            versions += loop.loop_host_ver.replace('.', '_').replace('-', '_') + ','
            t = 0
            for loop in loops:
                pass_percent = get_pass_percent(loop)
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
                                                       pass_percent,
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
    # \xa0 is actually non-breaking space in Latin1 (ISO 8859-1),
    # also chr(160). When .encode('utf-8'), it will encode the
    # unicode to utf-8, that means every unicode could be represented
    # by 1 to 4 bytes. For this case, \xa0 is represented by 2 bytes \xc2\xa0.
    # refer to https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
    context = unicodedata.normalize("NFKD", context)
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

    result = {}
    result['fail'] = {}
    result['error'] = {}
    result['cancel'] = {}
    result['skip'] = {}
    result['warn'] = {}
    result['interrupt'] = {}
    result['all'] = {}
    result['pass'] = {}

    result['fail']['fail_info'] = {}
    result['fail']['fail_cont'] = {}
    result['fail']['fail_percnet'] = {}

    result['error']['error_info'] = {}
    result['error']['error_cont'] = {}
    result['error']['error_percent'] = {}

    result['cancel']['cancel_info'] = {}
    result['cancel']['cancel_cont'] = {}
    result['cancel']['cancel_percent'] = {}

    result['skip']['skip_info'] = {}
    result['skip']['skip_cont'] = {}
    result['skip']['skip_percent'] = {}

    result['warn']['warn_info'] = {}
    result['warn']['warn_cont'] = {}
    result['warn']['warn_percent'] = {}

    result['interrupt']['interrupt_info'] = {}
    result['interrupt']['interrupt_cont'] = {}
    result['interrupt']['interrupt_percent'] = {}

    result['all']['all_info'] = {}
    result['all']['all_cont'] = {}

    result_info = {}
    result_cont = {}
    result_percent = {}

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

    result_info['pass_info'] = pass_info
    result_cont['pass_cont'] = pass_cont
    result_percent['PASS'] = float(pass_cont * 100) / testloop[0].loop_case_total_num
    result_info['fail_info'] = fail_info
    result_cont['fail_cont'] = fail_cont
    result_percent['FAIL'] = float(fail_cont * 100) / testloop[0].loop_case_total_num
    result_info['error_info'] = error_info
    result_cont['error_cont'] = error_cont
    result_percent['ERROR'] = float(error_cont * 100) / testloop[0].loop_case_total_num
    result_info['cancel_info'] = cancel_info
    result_cont['cancel_cont'] = cancel_cont
    result_percent['CANCEL'] = float(cancel_cont * 100) / testloop[0].loop_case_total_num
    result_info['skip_info'] = skip_info
    result_cont['skip_cont'] = skip_cont
    result_percent['SKIP'] = float(skip_cont * 100) / testloop[0].loop_case_total_num
    result_info['warn_info'] = warn_info
    result_cont['warn_cont'] = warn_cont
    result_percent['WARN'] = float(warn_cont * 100) / testloop[0].loop_case_total_num
    result_info['interrupt_info'] = interrupt_info
    result_cont['interrupt_cont'] = interrupt_cont
    result_percent['INTERRUPT'] = float(interrupt_cont * 100) / testloop[0].loop_case_total_num
    result_info['all_info'] = all_info
    result_cont['all_cont'] = all_cont

    actual_cont = fail_cont + error_cont + cancel_cont + skip_cont + warn_cont + interrupt_cont + pass_cont
    if testloop[0].loop_case_total_num > actual_cont:
        unknown_cont = testloop[0].loop_case_total_num - actual_cont
        result_percent['UNKNOWN'] = (float(unknown_cont * 100) /
                                     testloop[0].loop_case_total_num)

    result['pass']['pass_info'] = result_info['pass_info']
    result['pass']['pass_cont'] = result_cont['pass_cont']
    result['pass']['pass_info_percent'] = result_percent['PASS']

    result['fail']['fail_info'] = result_info['fail_info']
    result['fail']['fail_cont'] = result_cont['fail_cont']
    result['fail']['fail_percnet'] = result_percent['FAIL']

    result['error']['error_info'] = result_info['error_info']
    result['error']['error_cont'] = result_cont['error_cont']
    result['error']['error_percent'] = result_percent['ERROR']

    result['cancel']['cancel_info'] = result_info['cancel_info']
    result['cancel']['cancel_cont'] = result_cont['cancel_cont']
    result['cancel']['cancel_percent'] = result_percent['CANCEL']

    result['skip']['skip_info'] = result_info['skip_info']
    result['skip']['skip_cont'] = result_cont['skip_cont']
    result['skip']['skip_percent'] = result_percent['SKIP']

    result['warn']['warn_info'] = result_info['warn_info']
    result['warn']['warn_cont'] = result_cont['warn_cont']
    result['warn']['warn_percent'] = result_percent['WARN']

    result['interrupt']['interrupt_info'] = result_info['interrupt_info']
    result['interrupt']['interrupt_cont'] = result_cont['interrupt_cont']
    result['interrupt']['interrupt_info_percent'] = result_percent['INTERRUPT']

    result['all']['all_info'] = result_info['all_info']
    result['all']['all_cont'] = result_cont['all_cont']

    return cases, result, result_percent
