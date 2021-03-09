import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')

import django
django.setup()

from PassPercentage.models import AvocadoFeatureMapping


def add_feature(**kwargs):
    f = AvocadoFeatureMapping.objects.create(**kwargs)
    f.save()
    return f


kwargs = {}
with open("./feature_info.cfg") as feature_info:
    for info in feature_info:
        info = info.split("; ")
        kwargs['category'] = info[0]
        kwargs['configs'] = info[1]
        kwargs['owner'] = info[2]
        kwargs['main_feature'] = info[3]
        kwargs['sub_feature'] = info[4]
        print("populating data: %s" % kwargs)
        add_feature(**kwargs)
