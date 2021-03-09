import json
import requests
import sys

if len(sys.argv) != 3:
    print("Usage:")
    print(" python dump_post_pp.py $pass_percentage_uri $pass_percentage_json_file")
    print("e.g:")
    print(" python dump_post_pp.py http://dell-per715-04-vm-passpercentage.lab.eng.pek2.redhat.com:8000/"
          "PassPercentage/server_api/ passpercentage.json")
    sys.exit(-1)


def post(url, pp_file):
    with open(pp_file) as json_data:
        pp_dict = json.load(json_data)
    r = requests.post(url, json=pp_dict)
    for (key, val) in pp_dict.items():
        print('key: %s, val: %s' % (key, val))
    print(r.status_code, r.reason)
    sys.exit(0)


if __name__ == '__main__':
    post(url=sys.argv[1], pp_file=sys.argv[2])
