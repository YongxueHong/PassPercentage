import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')

import django
django.setup()

from PassPercentage.models import TestLoop
from PassPercentage.models import TestsID
from PassPercentage.models import CaseDetail
from PassPercentage.models import Platform


test_loop = TestLoop.objects.filter(loop_name='guest_agent')
virtio_win_platform = Platform.objects.get(platform_slug='virtio-win')

cnt = 0
for loop in test_loop:
    if 'x86' not in loop.loop_host_kernel_ver:
        continue
    print(loop.loop_cmd)
    testid = TestsID.objects.get(tests_id=loop.loop_updated_time)
    case_details = CaseDetail.objects.filter(test_id=testid)
    loop.platform = virtio_win_platform
    loop.save(update_fields=['platform', ])
    testid.loop = loop
    testid.save(update_fields=['loop', ])

    for case_detail in case_details:
        case_detail.test_id = testid
        case_detail.save(update_fields=['test_id', ])
