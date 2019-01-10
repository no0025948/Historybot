# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt


from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import requests, json

# 這邊是Linebot的授權TOKEN

line_bot_api = LineBotApi('token')
parser = WebhookParser('secret')


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
    
    url = "url"


    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'type',
                       'Authorization': 'auth'
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

