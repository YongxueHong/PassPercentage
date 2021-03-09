import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')

import django
django.setup()

from PassPercentage.models import TestLoop

from PassPercentage.utils import update_testloop_model_by_avocado_feature_mapping

test_loop = TestLoop.objects.all()
cnt = 1
for loop in test_loop:
    if not update_testloop_model_by_avocado_feature_mapping(loop):
        print("%d: Delete test loop from database, loop command line: %s." %
              (cnt, loop.loop_cmd))
        cnt = cnt + 1
        loop.delete()
