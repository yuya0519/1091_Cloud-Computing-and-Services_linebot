import requests
from flask import Flask
app = Flask(__name__)

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,StickerSendMessage,LocationSendMessage,QuickReply,QuickReplyButton,MessageAction
try:
    import xml.etree.cElement as ET
except ImportError:
    import xml.etree.ElementTree as ET
line_bot_api = LineBotApi('YpvfBk2+aw0ke1XqoQIbSd5crq5+znDqLlsw0DiGbSEM0UdnV3FWOZpLlrCu3nFY00Z9hC2aj2jPhISJnQ2PQ3iv7tXvBxDvC9UV8BXamLt/vlPnD7jnMKHfpIR+YZgGxv1tPK76ws0MGRcDQpBkjwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ffa3a1e3e8fc6580304e62ed92869ae3')

@app.route("/callback",methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):    
    mtext = event.message.text  
    if mtext == '@傳送文字':    
        try:
            message = TextSendMessage(text = "我是linebot,\n你好!")
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext =='@傳送圖片':
        try:
            message = ImageSendMessage(
                original_content_url ="https://i.imgur.com/b3i6MF4.jpg",
                preview_image_url = "https://i.imgur.com/b3i6MF4.jpg" )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext =='@傳送貼圖':
        try:
            message = StickerSendMessage(
                package_id='3',
                sticker_id='180'
                )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext =='@多項傳送':
        try:
            message = [
                StickerSendMessage(
                    package_id='3',
                    sticker_id='180'
                    ),
                TextSendMessage(
                    text = "喵~"
                    ),
                ImageSendMessage(
                    original_content_url = 'https://i.imgur.com/b3i6MF4.jpg',
                    preview_image_url = 'https://i.imgur.com/b3i6MF4.jpg'
                )
            ]
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext =='@傳送位置':
        try:
            message = LocationSendMessage(
                title='台北101',
                address='台北市信義路五段7號',
                latitude=25.034207,
                longitude=121.564590
                )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext == '@快速選單':     
        try:
            message = TextSendMessage(
                text ='請選擇最喜歡的程式語言',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="Python",text="Python")
                            ),
                        QuickReplyButton(
                            action=MessageAction(label="Java",text="Java")
                            ),
                        QuickReplyButton(
                            action=MessageAction(label="c#",text="c#")
                            ),
                        QuickReplyButton(
                            action=MessageAction(label="Basic",text="Basic")
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext == '@本期中獎號碼':
        try:
            message = TextSendMessage(monoNum(0))
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext == '@前期中獎號碼':
        try:
            message = TextSendMessage(monoNum(1)+'\n\n'+monoNum(2))
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    elif mtext == '@輸入發票最後三碼':
        message = TextSendMessage(text = '請輸入發票最後三碼進行對獎')
        line_bot_api.reply_message(event.reply_token, message)
    elif len(mtext) == 3 and mtext.isdigit():
        try:
            content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
            tree = ET.fromstring(content.text)
            items = list(tree.iter(tag='item'))
            title = items[0][0].text
            ptext = items[0][2].text
            ptext = ptext.replace('<p>','').replace('</p>','')
            temlist = ptext.split('：')
            prizelist = []
            prizelist.append(temlist[1][5:8])
            prizelist.append(temlist[2][5:8])
            for i in range(3):
                prizelist.append(temlist[3][9*i+5:9*i+8])
            sixlist = temlist[4].split('、')
            for i in range(len(sixlist)):
                prizelist.append(sixlist[i])
            if mtext in prizelist:
                message = TextSendMessage(text = '符合某獎項後三碼，請自行核對發票前五碼!\n\n'+monoNum(0))
                #message += monoNum(0)
            else:
                message = TextSendMessage(text = '很可惜，未中獎。請輸入下一張發票最後三碼。')
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    else:
        message = TextSendMessage(text = '請輸入發票最後三碼進行對獎')
        line_bot_api.reply_message(event.reply_token, message)
def monoNum(n):
    content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
    tree = ET.fromstring(content.text)
    items = list(tree.iter(tag='item'))
    title = items[n][0].text
    ptext = items[n][2].text
    ptext = ptext.replace('<p>','').replace('</p>','\n')
    return title +'月\n' + ptext[:-1]
if __name__ == '__main__':
    app.run()