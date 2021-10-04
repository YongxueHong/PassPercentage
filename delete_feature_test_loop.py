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

if len(sys.argv) == 2:
    loop_updated_time = sys.argv[1]

else:
    print("Usage:")
    print("    python delete_feature_test_loops.py [loop_updated_time]")
    sys.exit(-1)

target_loops = []
for loop in test_loop:
    if loop_updated_time in str(loop.loop_updated_time):
        target_loops.append(loop)

if target_loops:
    print("Target loop:")
    for index, loop in enumerate(target_loops, 1):
        print("%d: loop cmd: %s" % (index, loop.loop_cmd))
else:
    print("No found the target loop!!")
    sys.exit(-1)

if len(target_loops) > 1:
    print("Too many target loops!!")
    sys.exit(-1)

while 1:
    to_del = input("Delete the above loop, yes or no: ")
    if to_del == 'yes':
        target_loops[0].delete()
        print("Deleted the above loop.")
        break
    elif to_del == 'no':
        print("Cancel to delete.")
        break
    else:
        print('Please input "yes" or "no".')
