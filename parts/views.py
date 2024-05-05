from urllib import response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from parts.utils import *
import json
from common.utils import *
from common.utils import Encoder
from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from logs.utils import add_logs_util
from accounts.views import check_permission
from rest_framework.decorators import api_view, permission_classes


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'part_number': openapi.Schema(type=openapi.TYPE_STRING, example='pt11'),
        'part_description': openapi.Schema(type=openapi.TYPE_STRING, example='fjjff')
    }
))

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_part_details(request):
    data = json.loads(request.body)
    from parts.utils import add_part_details_task
    part_id = add_part_details_task(data)
    return HttpResponse(json.dumps({'message' : 'Part added Successfully!', 'model_number' : part_id}, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_region(request):
    data = json.loads(request.body)
    from parts.utils import get_region_task
    part_id = get_region_task(data)
    return HttpResponse(json.dumps({'cordinates' : part_id}, cls=Encoder), content_type="application/json")



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def set_region_details(request):
    #check_permission(request,"can_add_part_details")
    data = json.loads(request.body)
    from parts.utils import set_region_details_task
    part_id = set_region_details_task(data)
    return HttpResponse(json.dumps({'message' : part_id}, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def delete_part(request):
    data = json.loads(request.body)
    from parts.utils import delete_part_task
    delete_part_task(data)
    return HttpResponse(json.dumps({'message' : 'Part deleted Successfully!'}, cls=Encoder), content_type="application/json")


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        '_id' : openapi.Schema(type=openapi.TYPE_STRING, example='5f32677047b362fbb536f1c0'),
        'part_number': openapi.Schema(type=openapi.TYPE_STRING, example='pt11'),
        'part_description': openapi.Schema(type=openapi.TYPE_STRING, example='fjjff')
    }
))

@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes(AllowAny,)
def update_part(request):
    data = json.loads(request.body)
    from parts.utils import update_part_task
    response = update_part_task(data)
    return HttpResponse(json.dumps({'message' : response}, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_part_details(request, part_id):
    from parts.utils import get_part_details_task
    response = get_part_details_task(part_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_all_part_details(request):
    from parts.utils import get_all_part_details_task
    response = get_all_part_details_task()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")



@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_all_parts_type_view(request):
    from parts.utils import get_all_part_type_util
    response = get_all_part_type_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_progress(request):
    from parts.utils import get_progress_details
    response  =  get_progress_details()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_parts(request):
    check_permission(request,"can_get_parts")
    token_user_id = request.user.user_id
    operation_type = "parts"
    notes = "get parts"
    
    add_logs_util(token_user_id,operation_type,notes)
    from parts.utils import get_parts_task 
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit' , 10)
    response = get_parts_task(skip, limit)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


######################################TBAL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_configuration_list(request):
    # print("Here>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(request)

    check_permission(request,"can_get_configuration_list")
    token_user_id = request.user.user_id
    operation_type = "parts"
    notes = "get parts"
    
    add_logs_util(token_user_id,operation_type,notes)
    from parts.utils import get_configuration_list_util 
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit' , 10)
    response = get_configuration_list_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_aircraft_number_new(request):
    check_permission(request,"can_get_new_aircraft_numbers")
    token_user_id = request.user.user_id
    operation_type = "parts"
    notes = "get parts"
    
    add_logs_util(token_user_id,operation_type,notes)
    from parts.utils import get_aircraft_number_new_util 
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit' , 10)
    response = get_aircraft_number_new_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_aircraft_number_used(request):
    check_permission(request,"can_get_used_aircraft_numbers")
    token_user_id = request.user.user_id
    operation_type = "parts"
    notes = "get parts"
    
    add_logs_util(token_user_id,operation_type,notes)
    from parts.utils import get_aircraft_number_used_util 
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit' , 10)
    response = get_aircraft_number_used_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# def get_aircraft_number_completed(request):
#     check_permission(request,"can_get_aircraft_number_new")
#     token_user_id = request.user.user_id
#     operation_type = "parts"
#     notes = "get parts"
    
#     add_logs_util(token_user_id,operation_type,notes)
#     from parts.utils import get_aircraft_number_completed_util 
#     skip = request.GET.get('skip', 0)
#     limit = request.GET.get('limit' , 10)
#     response = get_aircraft_number_completed_util()
#     return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# def get_aircraft_number_inprogress_completed(request):
#     check_permission(request,"can_get_aircraft_number_new")
#     token_user_id = request.user.user_id
#     operation_type = "parts"
#     notes = "get parts"
    
#     add_logs_util(token_user_id,operation_type,notes)
#     from parts.utils import get_aircraft_number_inprogress_completed_util 
#     skip = request.GET.get('skip', 0)
#     limit = request.GET.get('limit' , 10)
#     response = get_aircraft_number_inprogress_completed_util()
#     return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")