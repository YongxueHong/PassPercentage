import json
import requests
import sys

def post(ip, file):
    with open(file) as json_data:
        pp_dict = json.load(json_data)
    url = "http://%s:8000/PassPercentage/server_api/" %ip
    r = requests.post(url, json=pp_dict)
    for (key, val) in pp_dict.items():
        print('key: %s, val: %s' % (key,val))
    print(r.status_code, r.reason)

if __name__ == '__main__':
    post(ip=sys.argv[1], file=sys.argv[2])
