# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt


from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import requests, json

# 這邊是Linebot的授權TOKEN

line_bot_api = LineBotApi('BG0rpVvnFUw+bf/210EnJI8yUGUOJYvEWBP2FdNixTucirGQOxrH4mUkIkbUMDr8byGaA75gvDNGzujfyjvUlcTSg43XtumLwySa1or4gjXreFnWLJSLFUhzskS+uIlH6JVmO5j3viis+fx574bcYAdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('529bcfe640c19c10681b0b9efac4934d')


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                answer = get_answer(event.message.text)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=answer)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()




def get_answer(message_text):
    
    url = "https://iotproject1.azurewebsites.net/qnamaker/knowledgebases/f069e634-0e13-4614-b722-305603d53090/generateAnswer"


    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': 'EndpointKey 528db17a-4c12-487e-8fec-cfe5bb3521c1'
                   }
               )

    data = response.json()

    try: 
        if "error" in data:
            return data["error"]["message"]
        #這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']

        return answer

    except Exception:

        return "Error occurs when finding answer"

