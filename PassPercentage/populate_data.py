import os, time, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')
import django
django.setup()
from PassPercentage.models import Platform, TestLoop

def populate():
    ppc_platform = add_platform('ppc')
    x86_platform = add_platform('x86')
    s390_platform = add_platform('s390x')
    arm_platform = add_platform('arm')
    arm_platform = add_platform('virtio-win')
    x86_platform = add_platform('x86_64')

    # Print out
    for p in Platform.objects.all():
        for t in TestLoop.objects.filter(platform=p):
            print "- {0} - {1}".format(str(p), str(t))

def add_testloop(platform=None,
                 name=None,
                 feature_name=None,
                 feature_owner=None,
                 qemu_ver=None,
                 host_kernel_ver=None,
                 host_ver=None,
                 guest_kernel_ver=None,
                 guest_ver=None,
                 case_total_num=None,
                 case_pass_num=None,
                 cmd=None):
    t = TestLoop.objects.get_or_create(platform=platform,
                                       loop_name=name, 
                                       loop_feature_name=feature_name, 
                                       loop_feature_owner=feature_owner,
                                       loop_qemu_ver=qemu_ver, 
                                       loop_host_kernel_ver=host_kernel_ver,
                                       loop_host_ver=host_ver, 
                                       loop_guest_kernel_ver=guest_kernel_ver,
                                       loop_guest_ver=guest_ver, 
                                       loop_case_total_num=case_total_num,
                                       loop_case_pass_num=case_pass_num, 
                                       loop_cmd=cmd)[0]
    return t

def add_platform(name):
    p = Platform.objects.get_or_create(platform_name=name)[0]
    #time.sleep(random.randrange(1, 2))
    return p

# Start execution here!
if __name__ == '__main__':
    print "Starting PassPercentage population script..."
    populate()
