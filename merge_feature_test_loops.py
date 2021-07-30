import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')

import django
django.setup()


try:
    input = raw_input
except NameError:
    pass


from PassPercentage.models import TestLoop, Platform

test_loop = TestLoop.objects.all()

if len(sys.argv) == 4:
    platform = sys.argv[1]
    src_feature = sys.argv[2]
    dst_feature = sys.argv[3]

else:
    print("Usage:")
    print("    python merge_feature_test_loops.py [platform] [src feature] [dst feature]")
    sys.exit(-1)

target_loops = []
for loop in test_loop:
    if loop.loop_feature_name == src_feature:
        target_loops.append(loop)

for loop in target_loops[::]:
    if loop.platform.platform_name != platform:
        target_loops.remove(loop)

print("Target loops:")

for index, loop in enumerate(target_loops, 1):
    print("%d: loop cmd: %s" % (index, loop.loop_cmd))

while 1:
    to_move = input("Merge the above loops from '%s' into '%s', "
                    "yes or no: " % (src_feature, dst_feature))
    if to_move == 'yes':
        for index, loop in enumerate(target_loops, 1):
            print("%d: moving loop: %s" % (index, loop.loop_cmd))
            loop.loop_feature_name = dst_feature
            loop.save(update_fields=['loop_feature_name'])
        print("Merged the above loops.")
        break
    elif to_move == 'no':
        print("Cancel to merge.")
        break
    else:
        print('Please input "yes" or "no".')
