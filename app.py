"""
    Line Simple meme bots!

    Main Program
    By fauh45
    2020
"""

import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_ACCESS', ''));
handler = WebhookHandler(os.getenv('LINE_SECRET', ''));


@app.route("/")
def home():
    return 'Yes It is not here,\n go back to your hole\n\nBm\'l vextk axkx. Iextlx vhfx utvd. Ibvd nl ni.'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def text_handler(event):
    text_content = event.message.text

    if text_content[:5] == '/memes':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Umm, not done yet mate...\n\n"
                                 "Contact fauh45 for more info")
        )


if __name__ == '__main__':
    app.run()
