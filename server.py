from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os

import requests

import random



app = Flask(__name__)
#請在左方.env的檔案中加上： SECRET='這裡面請填你line後台的SECRET碼'
scn=os.environ.get('SECRET')

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('LINE_ACCESS_TOKEN'))

# Channel Secret           
handler = WebhookHandler(scn)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        
        handler.handle(body, signature)    
    except InvalidSignatureError:
        abort(100)
    return 'OK'

# 處理訊息 
#以下這段請先將webhook認證成功後 再將這段取消註解
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", "回覆:" + event.message.text)

# 貼圖回覆
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

# 照片回覆
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    return_message = "Photo received!"
    return_message_2 = "yes"
    # 發送單條訊息
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text = return_message))
    # 同時發送多條訊息
    # line_bot_api.reply_message(event.reply_token, [TextSendMessage(text = return_message), TextSendMessage(text=return_message_2)])
    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇地區',
                                actions=[
                                    PostbackTemplateAction(
                                        label='台中市',
                                        text='台中市',
                                        data='A&台中市'
                                    ),
                                    PostbackTemplateAction(
                                        label='高雄市',
                                        text='高雄市',
                                        data='A&高雄市'
                                    )
                                ]
                            )
                        )
                    )

    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
