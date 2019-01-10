#from django.http import HttpResponse
#from django.http import JsonResponse
import  pymysql 

def getData():
	conn  =  pymysql.connect(host = '140.120.13.163' ,user = 'test123' ,passwd = "test123" ,db = 'iot',charset='utf8' ) 
	cur  =  conn.cursor()  
	cur . execute( "SELECT * FROM light" ) 
	result = cur.fetchall() 
	dic1 = {
	        'value': [rows[1] for rows in result],
	        'status': [rows[2] for rows in result],
	        'time': [str(rows[3]) for rows in result]
	        }
	cur.close () 
	conn.close() 
	return dic1
	
def getAddress():
	conn  =  pymysql.connect(host = '127.0.0.1' ,user = 'test123' ,passwd = "test123" ,db = 'historymap',charset='utf8' ) 
	cur  =  conn.cursor ()  
	cur . execute( "SELECT * FROM topic where inquired = 1" ) 
	result = cur.fetchall() 
	dic2 = {
	        'id': [rows[0] for rows in result],
	        'address': [rows[3] for rows in result],
	        }
	cur.close() 
	conn.close() 
	return dic2

def ajax2(username):
    conn  =  pymysql.connect(host = '127.0.0.1' ,user = 'test123' ,passwd = "test123" ,db = 'historymap',charset='utf8' ) 
    cur  =  conn.cursor ()
    cur . execute( "SELECT * FROM topic where site = %s and inquired = 1 ",username ) 
    result = cur.fetchall()

    dic2 =  {
             'question': [rows[1] for rows in result],
	         'answer': [rows[2] for rows in result],
	    }
    cur.close() 
    conn.close() 
    return dic2
