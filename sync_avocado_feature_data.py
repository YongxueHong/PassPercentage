import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')

import django
django.setup()

from PassPercentage.models import TestLoop

from PassPercentage.utils import update_testloop_model_by_avocado_feature_mapping

test_loop = TestLoop.objects.all()
unregistered_loop = []

loop_name = None
if len(sys.argv) == 2:
    loop_name = sys.argv[1]
elif len(sys.argv) > 2:
    print("Usage:")
    print("    python sync_avocado_feature_data.py [loop name]")
    sys.exit(-1)

cnt = 0
for loop in test_loop:
    search_cond = "--category=%s" % loop_name if loop_name else ''
    if search_cond in loop.loop_cmd:
        cnt = cnt + 1
        print('%d: Searching loop cmd "%s" feature mapping in '
              'AvocadoFeatureMapping' % (cnt, loop.loop_cmd))
        if not update_testloop_model_by_avocado_feature_mapping(loop):
            unregistered_loop.append(loop)
if cnt != 0:
    print("Sync avocado feature done.")

if cnt == 0 and loop_name:
    print('No found loop name "%s" from database.' % loop_name)

if unregistered_loop:
    print('*' * 100)
    cnt = 1
    for loop in unregistered_loop:
        print("%d: Unregistered loop: %s" %
              (cnt, loop.loop_cmd))
        cnt = cnt + 1
    print('*' * 100)

    while 1:
        to_delete = raw_input(
                "Delete the above unregistered loops, yes or no: ")
        if to_delete == 'yes':
            cnt = 1
            for loop in unregistered_loop:
                print("%d: Deleting loop: %s" % (cnt, loop.loop_cmd))
                loop.delete()
                cnt = cnt + 1
            print("Deleted the above loops.")
            break
        elif to_delete == 'no':
            print("Cancel to delete.")
            break
        else:
            print('Please input "yes" or "no".')
