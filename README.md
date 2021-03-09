# PassPercentage
PassPercentage Dashboard that collecting results then show them from automation.

# Requirement:
<p>
python version: python2
<br>django version: 1.9
</p>

# HOWTO:
<p>
pip install -U django==1.9.10
<br>pip install pillow
<br>python manage.py migrate
<br>python manage.py makemigrations PassPercentage
<br>python manage.py migrate
<br>python manage.py createsuperuser
<br>python populate_avocado_feature_data.py
<br>python sync_avocado_feature_data.py
<br>python manage.py runserver $server_ip:$port
<br>http://$server_ip:$port/PassPercentage/
</p>

# Reference:
<p>
https://canvasjs.com/
<br>https://www.tangowithdjango.com/
</p>