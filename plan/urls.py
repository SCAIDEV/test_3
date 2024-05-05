from django.urls import path,re_path
# from django.conf.urls import url
from plan import views

urlpatterns = [
               re_path(r'^add_plan/$', views.add_plan), 
               re_path(r'^update_plan/$', views.update_plan), 
               re_path(r'^delete_plan/(?P<plan_id>[A-Za-z0-9-_]+)$', views.delete_plan), 
               re_path(r'^get_plans/$', views.plan_list), 
               re_path(r'^get_plan/(?P<plan_id>[A-Za-z0-9-_]+)$', views.plan_single), 
               re_path(r'^get_todays_planned_production/(?P<part_id>[A-Za-z0-9-_]+)$', views.get_todays_planned_production), 
]
