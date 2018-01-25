import json
import requests
import sys

def post(ip, file):
    with open(file) as json_data:
        pp_dict = json_result = json.load(json_data)
        tests_list = []
        for k, v in pp_dict.items():
            if k == 'tests':
                for i in v:
                    s = str(i)
                    tests_list.append(s)
        pp_dict['tests'] = tests_list
    url = "http://%s:8000/PassPercentage/server_api/" %ip
    r = requests.post(url, data=pp_dict)
    for (key, val) in pp_dict.items():
        print ('key: %s, val: %s' % (key,val))
    print(r.status_code, r.reason)

if __name__ == '__main__':
    post(ip=sys.argv[1], file=sys.argv[2])
