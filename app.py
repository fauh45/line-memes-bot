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
from linebot.models.sources import (
    SourceUser, SourceGroup
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationMessage, FollowEvent, ImageSendMessage
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
    text_content_list = text_content.split(' ')
    specials = False

    if text_content_list[0] == '/memes':
        text = "Not done yet mate\n"
        if len(text_content_list > 1):
            if text_content_list[1] == 'rick':
                specials = True
                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url="https://i.kym-cdn.com/entries/icons/original/000/023/608/picklerick.jpg"
                    )
                )

            elif text_content_list[1] == 'nice':
                specials = True
                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url="https://i.kym-cdn.com/entries/icons/original/000/032/180/cover4.jpg"
                    )
                )

        if not specials:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Umm, not done yet mate...\n\n"
                                     "Contact fauh45 for more info")
            )

    elif isinstance(event.source, SourceGroup):
        if text_content_list[0] == '/bye':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Goodbye, we had a good run...")
            )
            line_bot_api.leave_group(event.source.group_id)


@handler.add(MessageEvent, message=LocationMessage)
def location_handler(event):
    if isinstance(event.source, SourceUser):
        lat, lon = event.latitude, event.longitude
        text = "Lat = " + str(lat) + "\nLon=" + str(lon) + "\n\nContacting the FBI...."

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )


@handler.add(FollowEvent)
def follow_handler(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Hey!\nTo use this bot, try :\n/memes - for memes"
                             "\n\nfauh45")
    )


if __name__ == '__main__':
    app.run()
