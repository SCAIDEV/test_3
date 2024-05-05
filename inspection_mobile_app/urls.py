from django.urls import path,re_path
from inspection_mobile_app import views


urlpatterns = [
    # re_path(r'^testLogs/$', views.test_logs),
    #re_path(r'^add_assects/$', views.add_assects),
    #re_path(r'^update_assect/$', views.update_assect),
    #re_path(r'^get_assect/$', views.get_assect),
    # re_path(r'^start_process/$', views.start_process),
    # re_path(r'^plan_production_counter_modify/$', views.plan_production_counter_modify),
    # re_path(r'^end_process/$', views.end_process),
    # re_path(r'^report_process/$', views.report_process),
    # re_path(r'^get_virtual_button/$', views.get_virtual_button),
    # re_path(r'^get_plc_button/$', views.get_plc_button),
    # re_path(r'^get_running_process/(?P<workstation_id>[A-Za-z0-9-_]+)$', views.get_running_process),
    # re_path(r'^get_metrics/(?P<inspection_id>[A-Za-z0-9-_]+)$', views.get_metrics),

    #mobile app
    re_path(r'^get_all_parts_mobile/$', views.get_all_parts_mobile),
    re_path(r'^get_reference_image/$', views.get_reference_image),
    re_path(r'^get_inference_mobile/$', views.get_inference_mobile),
    
    re_path(r'^get_all_regions/$', views.get_all_regions_view),

]

