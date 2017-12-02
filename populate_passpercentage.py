import os, time, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')
import django
django.setup()
from PassPercentage.models import Platform, TestLoop

def populate():
    ppc_platform = add_platform('ppc')
    x86_platform = add_platform('x86')
    s390_platform = add_platform('s390')
    arm_platform = add_platform('arm')
    """
    add_testloop(ppc_platform, 
                 name='acceptance', 
                 feature_name='acceptance', 
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7', 
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5', 
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5', 
                 case_total_num=120, 
                 case_pass_num=100,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=130,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=150,
                 case_pass_num=149,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=118,
                 case_pass_num=117,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.5',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=130,
                 case_pass_num=129,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=130,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.5',
                 case_total_num=120,
                 case_pass_num=100,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.5',
                 case_total_num=120,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.10.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.5',
                 case_total_num=120,
                 case_pass_num=119,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-720.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=200,
                 case_pass_num=150,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=130,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.10.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-745.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-745.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=150,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=118,
                 case_pass_num=117,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86_64',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86_64',
                 guest_ver='RHEL7.4',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='timer device',
                 feature_name='timer device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=timer_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.10.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=110,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.10.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=200,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')


    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')


    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.5',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.5',
                 case_total_num=100,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')
    """
    """
    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.9.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=120,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.9.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=199,
                 case_pass_num=134,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.4 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-663.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-663.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=90,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.10.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.x86',
                 host_ver='RHEL7.5',
                 guest_kernel_ver='kernel-3.10.0-720.el7.x86',
                 guest_ver='RHEL7.5',
                 case_total_num=150,
                 case_pass_num=134,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')
    
    """
    """
    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=118,
                 case_pass_num=97,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=55,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=44,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-720.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=198,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=130,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=145,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-745.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-745.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=133,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=118,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86_64',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86_64',
                 guest_ver='RHEL7.4',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='timer device',
                 feature_name='timer device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=145,
                 cmd='python ConfigTest.py --category=timer_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=110,
                 case_pass_num=106,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=67,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')


    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=34,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')


    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=22,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=78,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=111,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=222,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=118,
                 case_pass_num=97,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=55,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=44,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-720.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=198,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=130,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=145,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-745.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-745.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=133,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=118,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le_64',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le_64',
                 guest_ver='RHEL7.4',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='timer device',
                 feature_name='timer device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=145,
                 cmd='python ConfigTest.py --category=timer_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=110,
                 case_pass_num=106,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=67,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')


    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=34,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')


    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=22,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=78,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=111,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=222,
                 case_pass_num=87,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')
    """

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=111,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=50,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=133,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=118,
                 case_pass_num=100,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=118,
                 case_pass_num=117,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=80,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=77,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.x86_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=77,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-720.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-720.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=11,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-720.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=130,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=130,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-745.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-745.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=122,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=118,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=130,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=118,
                 case_pass_num=66,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86_64',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86_64',
                 guest_ver='RHEL7.4',
                 case_total_num=120,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='timer device',
                 feature_name='timer device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=133,
                 cmd='python ConfigTest.py --category=timer_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=110,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=90,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=80,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=33,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.x86',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.x86',
                 guest_ver='RHEL7.3',
                 case_total_num=111,
                 case_pass_num=88,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(x86_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.x86',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.x86',
                 guest_ver='RHEL7.4',
                 case_total_num=222,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=x86 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=120,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=118,
                 case_pass_num=108,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=109,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=112,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=127,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=130,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=77,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=88,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.8.0-1.el7',
                 host_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-718.el7.ppc64le_64',
                 guest_ver='RHEL7.3',
                 case_total_num=120,
                 case_pass_num=88,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='usb device',
                 feature_name='usb device',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-2.el7',
                 host_kernel_ver='kernel-3.10.0-720.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-720.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=usb_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=130,
                 case_pass_num=93,
                 cmd='python ConfigTest.py --category=numa --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual block device',
                 feature_name='virtual block device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-745.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-745.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=150,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=virtual_block_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='virtual nic device',
                 feature_name='virtual nic device',
                 feature_owner='zhengtli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=118,
                 case_pass_num=110,
                 cmd='python ConfigTest.py --category=virtual_nic_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingli',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le_64',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le_64',
                 guest_ver='RHEL7.4',
                 case_total_num=120,
                 case_pass_num=45,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='timer device',
                 feature_name='timer device',
                 feature_owner='yhong',
                 qemu_ver='qemu-kvm-rhev-2.9.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=150,
                 case_pass_num=133,
                 cmd='python ConfigTest.py --category=timer_device --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='kdump',
                 feature_name='kdump',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=110,
                 case_pass_num=88,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='numa',
                 feature_name='numa',
                 feature_owner='mdeng',
                 qemu_ver='qemu-kvm-rhev-2.8.0-6.el7',
                 host_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-723.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=200,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=kdump --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=66,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='yilzhang',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=100,
                 case_pass_num=77,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='qcow2',
                 feature_name='qcow2',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=100,
                 case_pass_num=99,
                 cmd='python ConfigTest.py --category=qcow2 --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='pingl',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 host_ver='RHEL7.3',
                 guest_kernel_ver='kernel-3.10.0-724.el7.ppc64le',
                 guest_ver='RHEL7.3',
                 case_total_num=111,
                 case_pass_num=66,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le_64 --mem=8192 --vcpu=8 --verbose=no')

    add_testloop(ppc_platform,
                 name='acceptance',
                 feature_name='acceptance',
                 feature_owner='xuma',
                 qemu_ver='qemu-kvm-rhev-2.8.0-8.el7',
                 host_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 host_ver='RHEL7.4',
                 guest_kernel_ver='kernel-3.10.0-660.el7.ppc64le',
                 guest_ver='RHEL7.4',
                 case_total_num=222,
                 case_pass_num=111,
                 cmd='python ConfigTest.py --category=acceptance --driveformat=virtio_blk '
                     '--imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.3 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no')

    # Print out
    for p in Platform.objects.all():
        for t in TestLoop.objects.filter(platform=p):
            print "- {0} - {1}".format(str(p), str(t))

def add_testloop(platform,
                 name, 
                 feature_name, 
                 feature_owner, 
                 qemu_ver, 
                 host_kernel_ver, 
                 host_ver, 
                 guest_kernel_ver,
                 guest_ver, 
                 case_total_num, 
                 case_pass_num, cmd):
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
    time.sleep(random.randrange(10, 120))
    return t

def add_platform(name):
    p = Platform.objects.get_or_create(platform_name=name)[0]
    time.sleep(random.randrange(3, 60))
    return p



# Start execution here!
if __name__ == '__main__':
    print "Starting PassPercentage population script..."
    populate()
