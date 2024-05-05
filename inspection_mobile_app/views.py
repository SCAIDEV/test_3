# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
# from django.http import HttpResponse
# from inspection_mobile_app.utils import *
# import json
# from common.utils import *

# from logs.utils import add_logs_util

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny

# from accounts.views import check_permission

from json import encoder
import json
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

# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def plan_production_counter_modify(request):
#     check_permission(request,"can_plan_production_counter_modify")
#     data = json.loads(request.body)
#     from inspection.utils import plan_production_counter_modify_util
#     response = plan_production_counter_modify_util(data)
#     return HttpResponse(json.dumps(response,cls=Encoder), content_type="application/json")
    
# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_running_process(request,workstation_id):
#     check_permission(request,"can_get_running_process")
#     #print("viewssss")
#     response,status_code = get_running_process_util(workstation_id)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
    
    
# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_metrics(request,inspection_id):
#     check_permission(request,"can_get_metrics")
#     response,status_code = get_metrics_util(inspection_id)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")    
        
        
        
# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_virtual_button(request):
#     check_permission(request,"can_get_virtual_button")
#     data = json.loads(request.body)
#     print("virtual button :::::::::::::::::::::")
#     print(data)
#     from inspection.utils import get_virtual_button_util
#     resp = get_virtual_button_util(data)
#     return HttpResponse(json.dumps( {'message' : resp} , cls=Encoder), content_type="application/json")
#     #part_id = data.get('part_id')
#     # print(part_id)
#     # if part_id:
#     #     resp = get_feature_util(part_id)
#     #     return HttpResponse(json.dumps( resp , cls=Encoder), content_type="application/json")
#     # return HttpResponse(json.dumps( {'message' : "Failed"} , cls=Encoder), content_type="application/json")

# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_plc_button(request):
#     data = json.loads(request.body)
#     print("virtual plcccccccccccc button :::::::::::::::::::::")
#     print(data)
#     from inspection.utils import get_plc_button_util
#     resp = get_plc_button_util(data)
#     return HttpResponse(json.dumps( {'message' : resp} , cls=Encoder), content_type="application/json")

# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def start_process(request):
#     check_permission(request,"can_start_process")
#     token_user_id = request.user.user_id
#     operation_type = "inspection"
#     notes = "start inspection"
    
#     add_logs_util(token_user_id,operation_type,notes)
    
    
#     data = json.loads(request.body)
    
    
#     response,status_code = start_process_util(data,token_user_id)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def end_process(request):
#     check_permission(request,"can_end_process")
#     token_user_id = request.user.user_id
#     operation_type = "inspection"
#     notes = "start inspection"
    
#     add_logs_util(token_user_id,operation_type,notes)
    
    
#     data = json.loads(request.body)
    
    
#     response,status_code = end_process_util(data,token_user_id)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
        

# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def report_process(request):
#     check_permission(request,"can_report_process")
#     token_user_id = request.user.user_id
#     operation_type = "inspection"
#     notes = "start inspection"
    
#     add_logs_util(token_user_id,operation_type,notes)
    
    
#     data = json.loads(request.body)
    
    
#     response,status_code = report_process_util(data,token_user_id)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")



###################################mobile app####################################
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_all_parts_mobile(request):
    # print("Inside?>>>>>>>>>>>>>>>>>>>>>>>>>>get_all_parts_mobile>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print("request:::",request)
    # print("request.body::::",request.body)
    # check_permission(request,"can_upload_images")
    # token_user_id = request.user.user_id
    # operation_type = "inspection"
    # notes = "start inspection"
    
    # add_logs_util(token_user_id,operation_type,notes)
    
    
    data = json.loads(request.body)
    # print(data,'qwwqdqwdwq')
    
    
    response,status_code = get_all_parts_mobile_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_reference_image(request):
    # check_permission(request,"can_upload_images")
    # token_user_id = request.user.user_id
    # operation_type = "inspection"
    # notes = "start inspection"
    
    # add_logs_util(token_user_id,operation_type,notes)
    
    
    # data = json.loads(request.body)
    # print("request:::",request)
    data = json.loads(request.body)
    
    response,status_code = get_reference_image_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_inference_mobile(request):
    # check_permission(request,"can_upload_images")
    # token_user_id = request.user.user_id
    operation_type = "inspection"
    notes = "start inspection"
    
    # add_logs_util(token_user_id,operation_type,notes)
    
    
    # data = json.loads(request.body)
    
    
    response,status_code = get_inference_mobile_util(request)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_all_regions_view(request):
   
    response,status_code = get_all_regions_util()
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")