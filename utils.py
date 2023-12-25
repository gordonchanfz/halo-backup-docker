# -*- coding: utf-8 -*-
import logging
import requests
import json
import tempfile
import qrcode
import hashlib
import base64


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



def webhook_send_text(webhook: str, message: str) -> None:
    # wecom_example = {
    #     "msgtype": "text",
    #     "text": {
    #         "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意."
    #     }
    # }
    response = requests.post(
        url=webhook,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "msgtype": "text",
            "text": {
                "content": message
            }
        }),
    )

    # 判断请求是否成功，并记录日志
    if response.status_code == 200:
        logger.info('消息发送成功')
        logger.info(response.text)
    else:
        logger.error('消息发送失败')


def webhook_send_md(webhook: str, message: str) -> None:
    response = requests.post(
        url=webhook,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "msgtype": "markdown",
            "markdown": {
                "content": str(message)
            }
        }),
    )
    # 判断请求是否成功，并记录日志
    if response.status_code == 200:
        logger.info('消息发送成功')
        logger.info(response.text)
    else:
        logger.error('消息发送失败')


def webhook_send_text_pic(webhook: str, qr_link: str) -> None:
    response = requests.post(
        url=webhook,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": "博客登录验证",
                        "url": qr_link,
                        "picurl": qr_link
                    }
                ]
            }
        }),
    )

    # 判断请求是否成功，并记录日志
    if response.status_code == 200:
        logger.info('消息发送成功')
        logger.info(response.text)
    else:
        logger.error('消息发送失败')


def webhook_send_pic(webhook: str, qr_link: str) -> None:
    # 1.将二维码链接转为图片
    qr_img = qrcode.make(qr_link)
    png_file = tempfile.mktemp('.png')
    qr_img.save(png_file)

    with open(png_file, 'rb') as f:
        # 转换图片为base64格式
        base64_data = base64.b64encode(f.read())
        image_data = str(base64_data, 'utf-8')
    with open(png_file, 'rb') as f:
        # 获取图片的md5值
        md = hashlib.md5()
        md.update(f.read())
        image_md5 = md.hexdigest()

    # 企业微信机器人发送图片消息
    response = requests.post(
        url=webhook,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "msgtype": "image",
            "image": {
                "base64": image_data,
                "md5": image_md5
            }
        }),
    )
    print(response.text)

if __name__=='__main__':
    webhook=''
    png_file=''
    with open(png_file, 'rb') as f:
        # 转换图片为base64格式
        base64_data = base64.b64encode(f.read())
        image_data = str(base64_data, 'utf-8')
    with open(png_file, 'rb') as f:
        # 获取图片的md5值
        md = hashlib.md5()
        md.update(f.read())
        image_md5 = md.hexdigest()

    # 企业微信机器人发送图片消息
    response = requests.post(
        url=webhook,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "msgtype": "image",
            "image": {
                "base64": image_data,
                "md5": image_md5
            }
        }),
    )
    print(response.text)