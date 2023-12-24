import base64
import time
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from aligo import Aligo
import tempfile
import qrcode
from ..utils import webhook_send_text,webhook_send_text_pic,webhook_send_pic




# 加载环境变量
load_dotenv()
#推送机器人（可选）
webhook = os.getenv("WEBHOOK")

def show(qr_link: str):
    """自定义显示二维码"""
    # 1.将二维码链接转为图片
    qr_img = qrcode.make(qr_link)
    png_file = tempfile.mktemp('.png')
    qr_img.save(png_file)

    # 2.将二维码发送到企业微信机器人
    webhook_send_text_pic(webhook,qr_link)
    webhook_send_pic(webhook,qr_link)


# 使用环境变量
# 网站地址
website = os.getenv("WEBSITE")
# halo2备份文件夹路径
backup_halo_path = os.getenv("BACKUP_HALO_PATH")
# 要备份的阿里云盘文件夹ID
ali_folder = os.getenv("ALI_FOLDER")
#halo网站用户名和密码
user = os.getenv("USER")
password = os.getenv("PASSWORD")


backup_api = website + "/apis/migration.halo.run/v1alpha1/backups"
check_api = website + "/apis/migration.halo.run/v1alpha1/backups?sort=metadata.creationTimestamp%2Cdesc"





if webhook is None:
    ali = Aligo()
else:
    ali=Aligo(show=show)
# 获取现在的时间 2023-09-24T13:14:18.650Z
now_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
print(now_time)
# 构建认证头部
auth_header = "Basic " + base64.b64encode((user + ":" + password).encode()).decode()
payload = json.dumps({
    "apiVersion": "migration.halo.run/v1alpha1",
    "kind": "Backup",
    "metadata": {
        "generateName": "backup-",
        "name": ""
    },
    "spec": {
        "expiresAt": now_time,
    }
})
headers = {
    'User-Agent': '',
    'Content-Type': 'application/json',
    'Authorization': "Basic " + base64.b64encode((user + ":" + password).encode()).decode(),
}
response = requests.request("POST", backup_api, headers=headers, data=payload)
print(response.text)
if response.status_code == 201:
    print("备份请求成功！")
    new_backup_name = ""
    while True:
        check_response = requests.request("GET", check_api, headers=headers)
        if check_response.status_code == 200:
            backup_data = json.loads(check_response.text)
            items = backup_data.get("items", [])
            if items[0]["status"]["phase"] == "SUCCEEDED":
                print("备份完成！")
                new_backup_name = items[0]["status"]["filename"]
                break
            if items[0]["status"]["phase"] == "RUNNING":
                print("正在备份！")
                time.sleep(10)

        else:
            print(f"查询备份请求失败！错误代码：{check_response.status_code}")
    ali.upload_file(backup_halo_path + "/" + new_backup_name,
                    parent_file_id=ali_folder)
    # for test
    #ali.upload_file("data/main.py",parent_file_id=ali_folder)
    print("阿里云盘上传完成！")
    webhook_send_text(webhook,"博客备份阿里云盘成功！")

else:
    print(f"备份请求失败！错误代码：{response.status_code}")
    webhook_send_text(webhook, f"博客备份阿里云盘失败！错误代码：{response.status_code}")

