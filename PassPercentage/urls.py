from django.conf.urls import url
from PassPercentage import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    #url(r'^$', views.homepage_column, name='homepage_column'),
    url(r'^about/$', views.about, name='about'),
    url(r'^platforms/(?P<platform_slug_name>[\w\-]+)/$', views.show_testloops, name='show_testloops'),
    #url(r'^line_charts/(?P<platform_slug_name>[\w\-]+)/$', views.show_line_charts, name='show_line_charts'),
    #url(r'^lines_charts/(?P<platform_slug_name>[\w\-]+)/$', views.display_lines_charts, name='display_lines_charts'),
    url(r'^lines_charts/(?P<platform_slug_name>[\w\-]+)/(?P<loop_select_name_underline>[\w\-]+)/$', views.display_lines_charts_from_column, name='display_lines_charts_from_column'),
    url(r'^column_charts/(?P<platform_slug_name>[\w\-]+)/$', views.show_column_chart, name='show_column_chart'),
    #url(r'^area_charts/(?P<platform_slug_name>[\w\-]+)/$', views.show_area_chart, name='show_area_chart'),
    url(r'^select_area_charts/(?P<platform_slug_name>[\w\-]+)/(?P<loop_select_name_underline>[\w\-]+)/(?P<host_ver>[\w\-]+)/$', views.display_area_chart, name='display_area_chart'),
    #url(r'^comments/(?P<platform_slug_name>[\w\-]+)/(?P<loop_select_name>[\w\-]+)/(?P<host_ver>[\w\-]+)/(?P<x_point>[\w\-]+)/$', views.comments, name='comments'),
    url(r'^comments/(?P<platform_slug_name>[\w\-]+)/(?P<loop_select_name>[\w\-]+)/(?P<host_ver>[\w\-]+)/(?P<x_point>[\w\-]+)/(?P<updated_time>[\w\-]+)/$', views.comments, name='comments'),
    #url(r'^comments/$', views.show_comments, name='show_comments'),
    url(r'^server_api/$', views.server_api, name='server_api'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
]