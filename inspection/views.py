from json import encoder
import json
from operator import sub
from django.http import HttpResponse, response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from common.utils import Encoder
from .utils import *
from rest_framework.permissions import AllowAny
from accounts.views import check_permission
from django.http import HttpResponse, StreamingHttpResponse


# @api_view(['GET'])
# @csrf_exempt
# @permission_classes((AllowAny,))
# #@permission_classes((AllowAny,))
# def getDefectList(request, inspectionid):
#     #check_permission(request,"can_get_defect_list")
#     from inspection.utils import get_defect_list
#     data = get_defect_list(inspectionid)
#     return HttpResponse(json.dumps({'data': data}), content_type="application/json")


# # @permission_classes((AllowAny,))
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes((AllowAny,))
# #@permission_classes((AllowAny,))
# def save_inspection_results_ocr(request):
#     data = request.data
#     #check_permission(request,"can_save_inspection_results")
#     from inspection.utils import save_inspection_ocr
#     #topic_detected_labels= str(cameraid)+str("_taco")
#     url = save_inspection_ocr(data)
#     return HttpResponse(json.dumps({'data': url}), content_type="application/json")


# # @permission_classes((AllowAny,))
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes((AllowAny,))
# #@permission_classes((AllowAny,))
# def save_inspection_results_burr(request):
#     data = request.data
#     #check_permission(request,"can_save_inspection_results")
#     from inspection.utils import save_inspection_burr
#     #topic_detected_labels= str(cameraid)+str("_taco")
#     url = save_inspection_burr(data)
#     return HttpResponse(json.dumps({'data': url}), content_type="application/json")


# @permission_classes((AllowAny,))
# @api_view(['GET'])
# @csrf_exempt
# @permission_classes((AllowAny,))
# #@permission_classes((AllowAny,))
# def get_data_stream(request, cameraid):
#     #check_permission(request,"can_get_capture_feed_url")
#     from inspection.utils import get_data_feed
#     #topic_detected_labels = str(cameraid) +str("_taco")
#     url = get_data_feed(cameraid)
#     return HttpResponse(json.dumps({'data': url}), content_type="application/json")


# import os
# # @permission_classes((AllowAny,))
# @api_view(['GET'])
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_camera_urls(request):
#     #check_permission(request,"can_get_capture_feed_url")
#     url_list = []
#     url_list.append(create_urls_from_camera("ocr_frame", 'http://127.0.0.1:8000') )
#     for i in range(0,6):
#         url_list.append(create_urls_from_camera(i, 'http://localhost:8000') )   
#     for i in range(6,10):
#         url_list.append(create_urls_from_camera(i, 'http://127.0.0.1:8000') )           
#     print(url_list)

#     return HttpResponse(json.dumps({'data': url_list}), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_running_process_views(request):
    #check_permission(request,"can_get_running_process")
    from inspection.utils import get_running_process_utils
    response, status_code = get_running_process_utils()
    if status_code != 200:
        return HttpResponse({response}, status = status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_current_process_views(request):
    #check_permission(request,"can_get_running_process")
    from inspection.utils import get_current_utils
    response, status_code = get_current_utils()
    if status_code != 200:
        return HttpResponse({response}, status = status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")




@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def start_process(request):
    ''''''
    # check_permission(request,"can_start_process")
    data = json.loads(request.body)
    response,status_code = start_process_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def start_inspection(request):
    ''''''
    # check_permission(request,"can_start_process")
    data = json.loads(request.body)
    response,stat,message,status_code = start_inspection_util(data)
    
    if status_code != 200:
        return HttpResponse(json.dumps({"response":message,"statu":stat}, cls=Encoder), content_type = "application/json")
    else:
        return HttpResponse(json.dumps({"response":response,"statu":stat}, cls=Encoder), content_type = "application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def end_process(request):
    #check_permission(request,"can_end_process")
    data = json.loads(request.body)
    response,status_code = end_process_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")
        
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def  submit_process(request):
    #check_permission(request,"can_end_process")
    data = json.loads(request.body)
    actual,edited,preview,message,status,status_code,label_type,font_size = submit_process_util(data)
 



    if status_code != 200:
        return HttpResponse(json.dumps({"response":message,"statu":status}, cls=Encoder), content_type = "application/json")
    else:
        return HttpResponse(json.dumps({"actual":actual,"edited":edited,"preview":preview,"message":message,"statu":status,"label_type":label_type,"font_size":font_size}, cls=Encoder), content_type = "application/json")

###############################################
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def  manual_entry(request):
    #check_permission(request,"can_end_process")
    data = json.loads(request.body)
    actual,edited,preview,message,status,status_code,label_type,font_size = manual_entry_utils(data)
   




    if status_code != 200:
        return HttpResponse(json.dumps({"response":message,"statu":status}, cls=Encoder), content_type = "application/json")
    else:
        return HttpResponse(json.dumps({"actual":actual,"edited":edited,"preview":preview,"message":message,"statu":status,"label_type":label_type,"font_size":font_size}, cls=Encoder), content_type = "application/json")
        
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def print_process(request):
    #check_permission(request,"can_end_process")
    data = json.loads(request.body)
    status_code = print_inspection(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps({"status":"succes"}, cls=Encoder), content_type = "application/json")



# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_input_stream(request,cameraid):
#     from inspection.utils import get_inference_feed
#     return StreamingHttpResponse(get_inference_feed(cameraid), content_type='multipart/x-mixed-replace; boundary=frame')



####################################TBAL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def add_aircraft_for_inspections(request):
    check_permission(request,"can_add_new_aircraft_inspection")
    data = json.loads(request.body)

    from inspection.utils import add_aircraft_for_inspections_util
    response,status_code = add_aircraft_for_inspections_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_aircraft_status_for_inspections(request):
    check_permission(request,"can_add_new_aircraft_inspection")
    # data = json.loads(request.body)
    from inspection.utils import get_aircraft_status_for_inspections_util
    response,status_code = get_aircraft_status_for_inspections_util()
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def end_aircraft_for_inspections(request):
    check_permission(request,"can_end_aircraft_inspection")
    data = json.loads(request.body)

    from inspection.utils import end_aircraft_for_inspections_util
    response,status_code = end_aircraft_for_inspections_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def reset_aircraft_for_inspections(request):
    check_permission(request,"can_end_aircraft_inspection")
    data = json.loads(request.body)

    from inspection.utils import reset_aircraft_for_inspections_util
    response,status_code = reset_aircraft_for_inspections_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_aircraft_number_for_inspection(request):
    check_permission(request,"can_get_sub_zone_levels")
    # data = json.loads(request.body)

    from inspection.utils import get_aircraft_number_for_inspection_util
    response,status_code = get_aircraft_number_for_inspection_util()
    print(response,status_code)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_interior_exterior_for_inspection(request):
    check_permission(request,"can_get_sub_zone_levels")
    data = json.loads(request.body)

    from inspection.utils import get_interior_exterior_for_inspection_util
    response,status_code = get_interior_exterior_for_inspection_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")
 
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_zone_for_inspection(request):
    check_permission(request,"can_get_sub_zone_levels")
    data = json.loads(request.body)

    from inspection.utils import get_zone_for_inspection_util
    response,status_code = get_zone_for_inspection_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json") 

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_fs_range_for_inspection(request):
    check_permission(request,"can_get_sub_zone_levels")
    data = json.loads(request.body)

    from inspection.utils import get_fs_range_for_inspection_util
    response,status_code = get_fs_range_for_inspection_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_wl_bl_range_for_inspection(request):
    check_permission(request,"can_get_sub_zone_levels")
    data = json.loads(request.body)

    from inspection.utils import get_wl_bl_range_for_inspection_util
    response,status_code = get_wl_bl_range_for_inspection_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_aircraft_sub_zone_levels(request):
    check_permission(request,"can_get_sub_zone_levels")
    data = json.loads(request.body)

    from inspection.utils import get_aircraft_sub_zone_levels_util
    response,status_code = get_aircraft_sub_zone_levels_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def mobile_upload(request):
    check_permission(request,"can_upload_images")
    message,status_code = mobile_upload_util(request)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}),
                            content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# # @permission_classes((AllowAny,))
# def get_predictions(request):
#     check_permission(request,"get_predictions")
#     data = json.loads(request.body)

#     from inspection.utils import get_predictions_util
#     print(data)
#     response,status_code = get_predictions_util(data)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_roi_details(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import get_roi_details_util
    response,status_code = get_roi_details_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def redis_camera(request,key):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import redis_camera_util
    print(data,key)
    # response = redis_camera_util(data)
    # key = data
    return StreamingHttpResponse(redis_camera_util(key), content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_redis_stream(request, key):
    # check_permission(request,"can_upload_images")
    from inspection.utils import redis_camera
    # key = RedisKeyBuilderServer(wid).get_key(cameraid, 'predicted-frame')
    # print("key:::::::::::::::::::::::::::::",key)
    return StreamingHttpResponse(redis_camera(key), content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def server_upload(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import server_upload_util
    response,status_code = server_upload_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def operator_flag(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)
    print(data)
    from inspection.utils import operator_flag_util
    response,status_code = operator_flag_util(data)
    print(response,status_code )
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def set_mannual_status(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import set_mannual_status_util
    response,status_code = set_mannual_status_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_flagged_regions(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)
    print(request)
    print(data)
    from inspection.utils import get_flagged_regions_util
    response,status_code = get_flagged_regions_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_flagged_region_url(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import get_flagged_region_url_util
    response,status_code = get_flagged_region_url_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_completed_regions(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)
    print(request)
    print(data)
    from inspection.utils import get_completed_regions_util
    response,status_code = get_completed_regions_util(data)
    # return HttpResponse( {response}, status=status_code)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def get_flagged_status(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)
    print(request)
    print(data)
    from inspection.utils import get_flagged_status_util
    response,status_code = get_flagged_status_util(data)
    # return HttpResponse( {response}, status=status_code)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def reset_region_scan_status(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import reset_region_scan_status_util
    response,status_code = reset_region_scan_status_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def set_false_predictions(request):
    check_permission(request,"can_upload_images")
    data = json.loads(request.body)

    from inspection.utils import set_false_predictions_util
    response,status_code = set_false_predictions_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")




@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def update_file(data):
    from inspection.utils import update_file_details
    response,status_code = update_file_details(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
def get_master_file(data):
    
    from inspection.utils import get_master_file_details
    response,status_code = get_master_file_details(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
def get_dateformate_file(data):
    # get_dateformat_file_details
    from inspection.utils import get_dateformat_file_details
    response,status_code = get_dateformat_file_details(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")        



@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def health_check(data):
    from inspection.utils import health_check_details
    response,status_code = health_check_details(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

    
