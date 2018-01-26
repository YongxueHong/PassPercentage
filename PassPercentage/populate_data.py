import os, time, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')
import django
django.setup()
from PassPercentage.models import Platform, TestLoop, TestsID, CaseDetail

def add_testloop(platform=None,
                 name=None,
                 feature_name=None,
                 feature_owner=None,
                 image_backend=None,
                 qemu_ver=None,
                 host_kernel_ver=None,
                 host_ver=None,
                 guest_kernel_ver=None,
                 guest_ver=None,
                 virtio_win_ver=None,
                 case_total_num=None,
                 case_pass_num=None,
                 cmd=None):
    #t = TestLoop.objects.get_or_create(platform=platform,
    t = TestLoop.objects.create(platform=platform,
                                       loop_name=name,
                                       loop_feature_name=feature_name, 
                                       loop_feature_owner=feature_owner,
                                       loop_image_backend=image_backend,
                                       loop_qemu_ver=qemu_ver, 
                                       loop_host_kernel_ver=host_kernel_ver,
                                       loop_host_ver=host_ver, 
                                       loop_guest_kernel_ver=guest_kernel_ver,
                                       loop_guest_ver=guest_ver,
                                       loop_virtio_win_ver=virtio_win_ver,
                                       loop_case_total_num=case_total_num,
                                       loop_case_pass_num=case_pass_num, 
                                       loop_cmd=cmd)
    print '%s : Created %s test loop object.' % (time.ctime(), name)
    print "- {0} - {1} - {2}".format(str(platform), str(t), str(t.loop_updated_time))
    t.save()
    #for p in Platform.objects.all():
    #    for t in TestLoop.objects.filter(platform=p):
    #        print "- {0} - {1} - {2}".format(str(p), str(t), str(t.loop_updated_time))
    return t

def add_platform(name):
    p = Platform.objects.get_or_create(platform_name=name)[0]
    p.save()
    return p

def add_testid(loop, id):
    id = TestsID.objects.create(loop=loop, tests_id=id)
    id.save()
    return id

def add_details(test_id, case_status, case_fail_reason, case_url, case_whiteboard, case_start, case_logdir,
                case_time, case_test, case_end, case_logfile, case_id):
    detail = CaseDetail.objects.create(test_id=test_id, case_status=case_status, case_fail_reason=case_fail_reason,
                                       case_url=case_url, case_whiteboard=case_whiteboard, case_start=case_start,
                                       case_logdir=case_logdir, case_time=case_time, case_test=case_test,
                                       case_end=case_end, case_logfile=case_logfile, case_id=case_id)
    detail.save()
    return detail

# Start execution here!
if __name__ == '__main__':
    print "Starting PassPercentage population script..."
