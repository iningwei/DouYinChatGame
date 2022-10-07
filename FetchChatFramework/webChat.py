# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 
# @Author  :
import os
import time
import socket
import requests as requests

from messages import message_pb2
from messages.chat import ChatMessage

def downloadImg(url,path):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            open(path, 'wb').write(r.content) # 将内容写入图片
            #print(f"CODE: {r.status_code} download {url} to {path}") # 返回状态码
            r.close()
            return path
        else:
            print(f"CODE: {r.status_code} download {url} Failed.")
            #return "error"
            return
    except ConnectionResetError:
        print("ConnectionResetError, download {url} Failed.")
        return
    except Exception as e:
        print('download Failed:'+e)
        return
    

def getScriptDir():
    return os.path.split(os.path.realpath(__file__))[0]

class Socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('192.168.1.105', 2555) # Socket服务器地址,根据自己情况修改
    def connet():
        try:
            Socket.s.connect(Socket.address)  # 尝试连接服务端
            print("connect success!")
        except OSError:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' [ERROR] 无法连接到Socket服务器,OSError')
            Socket.close()
        except Exception as e:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' [ERROR] 无法连接到Socket服务器,请检查服务器是否启动:'+e)
            Socket.close()
    def sendMsg(msg):        
        try:
            #s.sendall(msg.encode()) # 尝试向服务端发送消息
            Socket.s.sendall(bytes(msg,'utf8'))
        except ConnectionAbortedError:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' [ERROR] ConnectionAbortedError,Do connet():')
            Socket.close()
            Socket.connet()
        except OSError:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' [ERROR] 无法发送消息到Socket服务器,OSError')
            Socket.close()
            Socket.connet()
        except Exception as e:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' [ERROR] 无法发送消息到Socket服务器,Do connet():'+e)
            Socket.close()
            Socket.connet()
    def close():
        Socket.s.close()

class Watcher():
    def __init__(self):
        self.monitoringFile = f'{getScriptDir()}\\douyinLiveFile'

    def startWatcher(self):	
        while True:
            files = os.listdir(self.monitoringFile)
            if files:
                for _ in files:
                    filepath = self.monitoringFile + '\\' + _
                    if "a.gitignore" in filepath:
                        continue
                    with open(filepath, 'rb') as f:
                        # print(f.read())
                        response = message_pb2.Response()
                        response.ParseFromString(f.read())

                    for message in response.messages:
                        if message.method == 'WebcastChatMessage':
                            chat_message = ChatMessage()
                            chat_message.set_payload(message.payload)

                            # userID
                            userID = chat_message.user().id
                            # nick
                            nick= chat_message.user().nickname
                            # shortId
                            shortId=chat_message.user().shortId
                            # specialId
                            specialId=chat_message.user().specialId
                            # displayId
                            displayId=chat_message.user().displayId
                            # 发言
                            content = chat_message.instance.content
                            # 头像
                            userHeaderImg = chat_message.user().avatarThumb.urlList[0]
                            # print(userID, content, userHeaderImg)
                            # print(userID, content)
                            filePath1=f"{getScriptDir()}\\userImages\\{shortId}.jpg"
                            if not os.path.exists(filePath1):
                                filePath = downloadImg(userHeaderImg,filePath1)
                            #Socket.sendMsg(f"{userID}\0{content}\0{filePath}")
                            # 用户uid\0用户发送的消息\0用户头像路径
                            # Socket.sendMsg(f"{userID}\0{content}\0{filePath}")
                            Socket.sendMsg(f"{userID}@@@{content}")
                            # print(chat_message)
                            # print(f"{userID}@@@{content}@@@{filePath}")
                            print(f"{userID}:{shortId}:{nick}@@@{content}")
                    try:
                        os.remove(filepath)
                    except PermissionError as e:
                        time.sleep(1)
                        os.remove(filepath)

            time.sleep(2)

if __name__ == '__main__':
    if not os.path.isdir(getScriptDir()+"\\douyinLiveFile"):
        os.makedirs(getScriptDir()+"\\douyinLiveFile")
    if not os.path.isdir(getScriptDir()+"\\userImages"):
        os.makedirs(getScriptDir()+"\\userImages")
    Socket.connet()
    Watcher().startWatcher()