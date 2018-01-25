# Dashboard-Pycharm
code from pycharm
This project just show kinds of chart with data.


pip install -U django==1.9.10
pip install pillow

python manage.py migrate
python manage.py createsuperuser
python manage.py makemigrations PassPercentage
python manage.py migrate


python manage.py runserver 10.66.10.20:8000
python manage.py runserver 10.66.65.161:8000
python manage.py runserver 10.72.12.33:8000

http://10.66.10.20:8000/PassPercentage/
http://10.66.65.161:8000/PassPercentage/


python dump_post_pp.py 10.66.10.20 /root/avocado/job-results/latest/passpercentage

python dump_post_pp.py 10.66.10.20 /root/avocado/job-results/job-2018-01-21T08.09-b47566c/passpercentage
