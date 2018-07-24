# PassPercentage
PassPercentage Dashboard that collecting results from automation.

# HOWTO:
<p>
pip install -U django==1.9.10
<br>pip install pillow
<br>python manage.py migrate
<br>python manage.py makemigrations PassPercentage
<br>python manage.py migrate
<br>python manage.py createsuperuser
<br>python manage.py runserver $server_ip:$port
<br>http://$server_ip:$port/PassPercentage/
<br>python dump_post_pp.py $server_ip /root/avocado/job-results/latest/passpercentage
</p>