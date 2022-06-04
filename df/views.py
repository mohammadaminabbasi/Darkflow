import json
import os
import time
from random import random

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def ping1(request):
    data = {'ping': str(random())}
    time.sleep(2 * 60)
    return HttpResponse(json.dumps(data),
                        content_type='application/json; charset=utf8')


def index_req(request):
    query = request.GET.get('id', '')
    print(query)
    return JsonResponse({"3": "e"})


def home(request):
    query = request.GET.get('id', '')
    print(query)
    return JsonResponse({"3": "e"})
