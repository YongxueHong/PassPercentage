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
    feature_name = sys.argv[1]
    src_platform = sys.argv[2]
    dst_platform = sys.argv[3]
else:
    print("Usage:")
    print("    python move_feature_test_loops.py [feature name] [src platform] [dst platform]")
    sys.exit(-1)

target_loops = []
for loop in test_loop:
    if loop.platform.platform_name == src_platform:
        target_loops.append(loop)

for loop in target_loops[::]:
    if loop.loop_feature_name != feature_name:
        target_loops.remove(loop)

print("Target loops:")

for index, loop in enumerate(target_loops, 1):
    print("%d: loop cmd: %s" % (index, loop.loop_cmd))

dst_platform = Platform.objects.get(platform_slug=dst_platform)

while 1:
    to_move = input("Move the above loops from '%s' to '%s', "
                    "yes or no: " % (src_platform, dst_platform))
    if to_move == 'yes':
        for index, loop in enumerate(target_loops, 1):
            print("%d: moving loop: %s" % (index, loop.loop_cmd))
            loop.platform = dst_platform
            loop.save(update_fields=['platform'])
        print("Moved the above loops.")
        break
    elif to_move == 'no':
        print("Cancel to move.")
        break
    else:
        print('Please input "yes" or "no".')
