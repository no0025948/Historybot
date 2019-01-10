from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from mapHistory.getDatasandAddress import *
import json


# Create your views here.

def historymap(request):
    dic1 = getData()
    dic2 = getAddress()
    dics = {
		'data':dic1,
		'address':dic2,
	}
    return render(request, 'mapHistory.html',dics)


def ajax(request):
    username = request.GET.get('username')

    data = ajax2(username)  

    # data = {
    #     'value': username
    # }
    # return dics
    return JsonResponse(data)
    