import requests
dict = {}
dict ['name'] = 'acceptance',
dict ['feature_name'] = 'acceptance',
dict ['feature_owner'] = 'xuma',
dict ['qemu_ver'] = 'qemu-kvm-rhev-2.10.0-1.el7',
dict ['host_kernel_ver'] = 'kernel-3.10.0-718.el7.ppc64le',
dict ['host_ver'] = 'RHEL7.5',
dict ['guest_kernel_ver'] = 'kernel-3.10.0-718.el7.ppc64le',
dict ['guest_ver'] = 'RHEL7.5',
dict ['case_total_num'] = 120,
dict ['case_pass_num'] = 100,
dict ['cmd'] = 'python ConfigTest.py --category=acceptance --driveformat=virtio_blk --imageformat=qcow2 --nicmodel=virtio_net --guestname=RHEL.7.5 --platform=ppc64le --mem=8192 --vcpu=8 --verbose=no'

r = requests.post('http://10.66.10.20:8000/PassPercentage/server_api/', data=dict)