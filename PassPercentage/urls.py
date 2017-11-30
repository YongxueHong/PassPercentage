from django.conf.urls import url
from PassPercentage import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about/$', views.about, name='about'),
    url(r'^platforms/(?P<platform_slug_name>[\w\-]+)/$', views.show_testloops, name='show_testloops'),
    url(r'^line_charts/(?P<platform_slug_name>[\w\-]+)/$', views.show_line_charts, name='show_line_charts'),
    url(r'^lines_charts/(?P<platform_slug_name>[\w\-]+)/$', views.display_lines_charts, name='display_lines_charts'),
    url(r'^column_charts/(?P<platform_slug_name>[\w\-]+)/$', views.show_column_chart, name='show_column_chart'),
    url(r'^area_charts/(?P<platform_slug_name>[\w\-]+)/$', views.show_area_chart, name='show_area_chart'),
]