from django.urls import path,re_path
from parts import views


urlpatterns = [
    re_path(r'^set_region/$', views.set_region_details),
    re_path(r'^get_progress/$', views.get_progress),
    re_path(r'^add_part/$', views.add_part_details),
    re_path(r'^delete_part/$', views.delete_part),
    re_path(r'^update_part/$', views.update_part),
    re_path(r'^get_region/$', views.get_region),
    re_path(r'^part_details/(?P<part_id>[A-Za-z0-9-_]+)', views.get_part_details),
    re_path(r'^get_parts/$', views.get_all_part_details),

    re_path(r'^get_all_parts_type/$', views.get_all_parts_type_view),


    #TBAL
    #Configuration
    re_path(r'^get_configuration_list/$', views.get_configuration_list),

    # #Air craft
    # re_path(r'^get_aircraft_number_new/$', views.get_aircraft_number_new),
    # re_path(r'^get_aircraft_number_used/$', views.get_aircraft_number_used),
    
    # re_path(r'^get_aircraft_number_completed_list/$', views.get_aircraft_number_completed),
    # re_path(r'^get_aircraft_number_inprogress_completed_list/$', views.get_aircraft_number_inprogress_completed),
    
    #New DEC 7

    # re_path(r'^get_aircraft_number/$', views.get_aircraft_number),
    # re_path(r'^add_aircraft/$', views.add_aircraft),

]