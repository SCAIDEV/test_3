from django.contrib import admin
from django.urls import path, re_path
from django.urls import path,re_path
# from django.conf.urls import url
from inspection import views

urlpatterns = [
    # re_path(r'^get_camera_urls/$', views.get_camera_urls),
    # re_path(r'^save_results_ocr/$', views.save_inspection_results_ocr),
    # re_path(r'^save_results_burr/$', views.save_inspection_results_burr),
    re_path(r'^get_running_process/$', views.get_running_process_views),
    re_path(r'^get_current_process/$', views.get_current_process_views),
    re_path(r'^start_process/$', views.start_process),
    re_path(r'^start_inspection/$', views.start_inspection),
    re_path(r'^end_process/$', views.end_process),
    re_path(r'^submit/$', views.submit_process),
    re_path(r'^manual_entry/$', views.manual_entry),
    re_path(r'^print/$', views.print_process),
    # re_path(r'^getDefectList/(?P<inspectionid>[A-Za-z0-9-._]+)$', views.getDefectList),
    # re_path(r'^get_data_stream/(?P<cameraid>[A-Za-z0-9-._]+)/$', views.get_data_stream),
    # re_path(r'^get_output_stream/(?P<cameraid>[A-Za-z0-9-._]+)/$', views.get_input_stream),


    ######################TBAL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # re_path(r'^configure_new_aircraft_inspection/$', views.configure_new_aircraft_inspection),
    re_path(r'^add_aircraft_for_inspections/$', views.add_aircraft_for_inspections),
    re_path(r'^get_aircraft_status_for_inspections/$', views.get_aircraft_status_for_inspections),

    re_path(r'^end_aircraft_for_inspections/$', views.end_aircraft_for_inspections),
    re_path(r'^reset_aircraft_for_inspections/$', views.reset_aircraft_for_inspections),

    #Zones
    #Get Aircraft number for inspection
    re_path(r'^get_aircraft_number_for_inspection/$', views.get_aircraft_number_for_inspection),
    re_path(r'^get_interior_exterior_for_inspection/$', views.get_interior_exterior_for_inspection),
    re_path(r'^get_zone_for_inspection/$', views.get_zone_for_inspection),
    re_path(r'^get_fs_range_for_inspection/$', views.get_fs_range_for_inspection),
    re_path(r'^get_wl_bl_range_for_inspection/$', views.get_wl_bl_range_for_inspection),
    re_path(r'^get_roi_details/$', views.get_roi_details),

    #Upload from mobile
    # re_path(r'^mobile_upload/$', views.mobile_upload),
    # re_path(r'^get_predictions/$', views.get_predictions),
    
    # #Get prediction
    # re_path(r'^get_predictions/$', views.get_predictions),

    #Redis frame
    re_path(r'^redis_camera/(?P<key>[A-Za-z0-9-_.]+)/$/$', views.redis_camera),
    re_path(r'^stream/(?P<key>[A-Za-z0-9-_.]+)/$', views.get_redis_stream), 
    re_path(r'^server_upload/$', views.server_upload),

    # Flagged regions operation
    re_path(r'^operator_flag/$', views.operator_flag),
    re_path(r'^set_mannual_status/$', views.set_mannual_status),
    re_path(r'^get_flagged_regions/$', views.get_flagged_regions),
    re_path(r'^get_flagged_region_url/$', views.get_flagged_region_url),
    re_path(r'^get_flagged_status/$', views.get_flagged_status),

    # Reset the scanned regions
    re_path(r'^get_completed_regions/$', views.get_completed_regions),
    re_path(r'^reset_region_scan_status/$', views.reset_region_scan_status),

    # Set the False predictions
    re_path(r'^set_false_predictions/$', views.set_false_predictions),
    re_path(r'^update_file/$', views.update_file),
    re_path(r'^get_master_file/$', views.get_master_file),
    re_path(r'^get_dateformat_file/$', views.get_dateformate_file),


    re_path(r'^health_check/$', views.health_check),
    # get_dateformat_file
    

]
