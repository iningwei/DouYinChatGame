# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 
# @Author  :
from math import fabs
import os
from pickle import TRUE
##from telnetlib import theNULL
import time
import socket
import requests as requests
import xml.etree.ElementTree as ET
import datetime  # 导入datetime模块
import threading  # 导入threading模块


from messages import message_pb2
from messages.chat import ChatMessage
from messages.member import MemberMessage
from messages.like import LikeMessage
from messages.social import SocialMessage
from messages.gift import GiftMessage
from archives.xmlTools import XMLTool

xmlTool=XMLTool()
global previousJoinOutValue
previousJoinOutValue="-1"
global previousGameStartValue
previousGameStartValue="0"

global isXMLReadedByQiangGeGe
isXMLReadedByQiangGeGe=False


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

                            ###暂时先不下载头像---->
                            #filePath1=f"{getScriptDir()}\\userImages\\{shortId}.jpg"
                            #if not os.path.exists(filePath1):
                            #    filePath = downloadImg(userHeaderImg,filePath1)
                            ###----->

                            #Socket.sendMsg(f"{userID}\0{content}\0{filePath}")
                            # 用户uid\0用户发送的消息\0用户头像路径
                            # Socket.sendMsg(f"{userID}\0{content}\0{filePath}")
                            ###Socket.sendMsg(f"{userID}@@@{content}")
                            # print(chat_message)
                            # print(f"{userID}@@@{content}@@@{filePath}")
                            #print(f"{userID}:{shortId}:{nick}@@@{content}")


                            if not content=="":
                            #if content=="j" or content=="J":
                                #print(f"try join:{nick}")
                                shortIdStr=str(shortId)[0:7]#取7位，防止强哥那边越界
                                xmlTool.Join(shortIdStr,f"{nick}")
                                    

                        elif message.method=="WebcastMemberMessage":
                            member_message=MemberMessage()
                            member_message.set_payload(message.payload)

                            #userID
                            userID=member_message.user().id
                             # nick
                            nick= member_message.user().nickname
                            # shortId
                            shortId=member_message.user().shortId
                            # 发言
                            content = "来了"
                            #print(f"WebcastMemberMessage:{userID}:{shortId}:{nick}@@@{content}")
                        elif message.method=="WebcastLikeMessage":
                            like_message=LikeMessage()
                            like_message.set_payload(message.payload)

                            #userID
                            userID=like_message.user().id
                             # nick
                            nick= like_message.user().nickname
                            # shortId
                            shortId=like_message.user().shortId
                            # 发言
                            content = "点赞"
                            # 点赞总数
                            count=like_message.instance.count
                            total=like_message.instance.total
                            #print(f"{userID}:{shortId}:{nick}@@@{content},count:{count},total:{total}")
                        elif message.method=="WebcastSocialMessage":
                            social_message=SocialMessage()
                            social_message.set_payload(message.payload)

                            #userID
                            userID=social_message.user().id
                             # nick
                            nick= social_message.user().nickname
                            # shortId
                            shortId=social_message.user().shortId
                            # 发言
                            content = "关注"
                            # 关注总数
                            followCount=social_message.instance.followCount
                            #print(f"{userID}:{shortId}:{nick}@@@{content},total:{followCount}")
                        elif message.method=="WebcastGiftMessage":
                            gift_message=GiftMessage()
                            gift_message.set_payload(message.payload)

                            #userID
                            userID=gift_message.user().id
                             # nick
                            nick= gift_message.user().nickname
                            # shortId
                            shortId=gift_message.user().shortId
                            # 发言
                            content ="礼物："+gift_message.gift().describe+","+str(gift_message.gift().id)
                            #print(f"{userID}:{shortId}:{nick}@@@{content}")
                            # 0 粉丝团，463 小星星，3992 人气票，3242 入团卡，165 棒棒糖，2006 一捧鲜花 ，2001 一只玫瑰
                            # 2110 一顶贵冠 ，164 抖音
                    try:
                        os.remove(filepath)
                    except PermissionError as e:
                        time.sleep(1)
                        os.remove(filepath)

            time.sleep(2)



# 定义xml读取方法
def runXML():  
    try:
        global isXMLReadedByQiangGeGe
        global previousJoinOutValue
        global previousGameStartValue
        isXMLReadedByQiangGeGe=False        
        xmlTool.Read()
        ##处理重开局
        if not previousGameStartValue==xmlTool.readedRoleJoinData.GameStartValue:
            print("重开局！！！！！！！！！！！！！！")
            previousGameStartValue=xmlTool.readedRoleJoinData.GameStartValue
            xmlTool.InitFile("0",previousGameStartValue,"0")
            xmlTool.ClearCachedAllRoleJoinData()
            xmlTool.Read()
        if not xmlTool.readedRoleJoinData.GameStartValue=="0" and not xmlTool.readedRoleJoinData.GUID_Join_OutValue==previousJoinOutValue:
            previousJoinOutValue=xmlTool.readedRoleJoinData.GUID_Join_OutValue            
            isXMLReadedByQiangGeGe=True
            print("previousJoinOutValue:"+previousJoinOutValue)

        if not xmlTool.readedRoleJoinData.GameStartValue=="0" and len(xmlTool.cachedRoleJoinData.JoinDic)>0:
            isXMLReadedByQiangGeGe=True

        if isXMLReadedByQiangGeGe==True:            
            xmlTool.Save()
            
            
    except PermissionError as e:
        print("Permission error!")
    timer=threading.Timer(1,runXML)  # 每秒运行
    timer.start()  # 执行方法



if __name__ == '__main__':
    if not os.path.isdir(getScriptDir()+"\\douyinLiveFile"):
        os.makedirs(getScriptDir()+"\\douyinLiveFile")
    if not os.path.isdir(getScriptDir()+"\\userImages"):
        os.makedirs(getScriptDir()+"\\userImages")

    #XML读取
    #先初始化xml文件
    xmlTool.InitFile("0","0","0")
    t1=threading.Timer(1,function=runXML)  # 创建定时器
    t1.start()  # 开始执行线程

    
    





    ##Socket.connet()#强哥项目不需要socket

    Watcher().startWatcher()