#!/usr/bin/env python
import json
import requests

with open("/root/avocado/job-results/latest/passpercentage") as json_data:
    pp_dict = json_result = json.load(json_data)
r = requests.post("http://10.66.10.20:8000/PassPercentage/server_api/", data=pp_dict)
for (key, val) in pp_dict.items():
    print ('key: %s, val: %s' % (key, val))
print(r.status_code, r.reason)
