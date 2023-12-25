## 简介
利用aligo对halo个人博客进行定时备份至阿里云盘，采用docker化一键部署。
>aligo项目地址：https://github.com/foyoux/aligo

## 使用教程
```shell
#创建配置目录
mkdir -p /home/gordonchanfz/halo-backup
#运行
docker run -d --restart=unless-stopped --name halo-backup \
 -v /home/gordonchanfz/halo-backup/data:/app/data \
 -v ~/.halo2/backups:/app/backups \
ghcr.io/gordonchanfz/halo-backup-docker:latest
```
说明：

~/.halo2/backups halo博客对应的backups的目录
/home/gordonchanfz/halo-backup/data 该目录放data的config.json和定时任务命令my-cron

config配置： 

复制一份config-template.json修改为config.json
```python
{
    "website":"", #website你的网站地址，不要带结尾反斜杠
    "backup_halo_path":"/app/backups",#backup_halo_path 通过挂载Halo备份的目录，与挂载目录一致即可
    "ali_folder":"",#ali_folder 你要备份到的阿里云网盘目录ID(网页进入目录后有)
    "user":"",#user 你Halo的账号
    "password":"",#password 你Halo的密码
    "webhook":""#企业微信机器人webhook（可选）
}
```