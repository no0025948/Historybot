from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import  pymysql 
import json
# Create your views here.

def highchart(request):
	conn  =  pymysql.connect( host = '127.0.0.1' ,  user = 'test123' ,  passwd = "test123" ,  db = 'iot' ) 
	cur  =  conn.cursor()  
	cur.execute( "SELECT * FROM light" ) 
	result = cur.fetchall() 
	dic = {
	        'value': [rows[2] for rows in result],
	        'status': [rows[4] for rows in result],
	        'time': [str(rows[1]) for rows in result]
	        }
	cur.close() 
	conn.close() 
	return render(request,"highchart.html",{'dic':dic}) 

