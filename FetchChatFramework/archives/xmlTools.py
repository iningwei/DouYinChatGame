from genericpath import isfile
import os
import random
import xml.etree.ElementTree as ET



from archives.roleJoin import RoleJoin

from archives.roleDM import RoleDM

# 教程
# https://blog.csdn.net/hu694028833/article/details/81089959?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-81089959-blog-119954423.pc_relevant_3mothn_strategy_and_data_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-81089959-blog-119954423.pc_relevant_3mothn_strategy_and_data_recovery&utm_relevant_index=6


# 玩家加入
class RoleJoinXMLTool():
    # 增加换行符
    def __indent(self,elem, level=0):
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def __init__(self):
        path=os.path.split(os.path.realpath(__file__))[0]
        self.filePath="C:\\Users\\zhouhui\\Documents\\StarCraft II\\Banks\\PlayerJoin.SC2Bank"
        self.savePath =self.filePath ####f'{path}\\archiveXmlFile\\PlayerJoin.SC2Bank.xml'
        self.readedRoleJoinData=RoleJoin()
        self.cachedRoleJoinData=RoleJoin()

    def ClearCachedRoleJoinData(self):
        self.cachedRoleJoinData.JoinDic.clear()
    def ClearCachedAllRoleJoinData(self):
        self.cachedRoleJoinData.AllJoinDic.clear()
    def InitFile(self,join_out_init_value,game_start_init_Value,join_init_value):
        #创建节点
        root=ET.Element("Bank")
        root.set("version","1")
        ##创建文档
        tree=ET.ElementTree(root)
        ##创建J Section
        j_section=ET.Element("Section")
        j_section.set("name","J")
        root.append(j_section)
        ##创建j_section的 GUID_Join_Out
        guid_join_out=ET.Element("Key")
        guid_join_out.set("name","GUID_Join_Out")
        j_section.append(guid_join_out)
        ##创建GUID_Join_Out的Value
        guid_join_out_value=ET.Element("Value")
        guid_join_out_value.set("int",join_out_init_value)
        guid_join_out.append(guid_join_out_value)
        ##创建j_section的GameStart
        game_start=ET.Element("Key")
        game_start.set("name","GameStart")
        j_section.append(game_start)
        ##创建GameStart的Value
        game_start_value=ET.Element("Value")
        game_start_value.set("int",game_start_init_Value)
        game_start.append(game_start_value)

        ##创建j_section的 GUID_Join
        guid_join=ET.Element("Key")
        guid_join.set("name","GUID_Join")
        j_section.append(guid_join)
        ##创建GameStart的Value
        guid_join_value=ET.Element("Value")
        guid_join_value.set("int",join_init_value)
        guid_join.append(guid_join_value)
 
        ##增加换行符
        self.__indent(root)
        ##写文件
        if not os.path.exists(self.savePath):
            print("not exist,create file")
            open(self.savePath,'w').close()
        tree.write(self.savePath,encoding="utf-8",xml_declaration=True)
        print("init join file success")
    def Save(self):
        #创建节点
        root=ET.Element("Bank")
        root.set("version","1")
        ##创建文档
        tree=ET.ElementTree(root)
        ##创建J Section
        j_section=ET.Element("Section")
        j_section.set("name","J")
        root.append(j_section)
        ##创建j_section的 GUID_Join_Out
        guid_join_out=ET.Element("Key")
        guid_join_out.set("name","GUID_Join_Out")
        j_section.append(guid_join_out)
        ##创建GUID_Join_Out的Value
        guid_join_out_value=ET.Element("Value")
        guid_join_out_value.set("int",self.cachedRoleJoinData.GUID_Join_OutValue)
        guid_join_out.append(guid_join_out_value)
        ##创建j_section的GameStart
        game_start=ET.Element("Key")
        game_start.set("name","GameStart")
        j_section.append(game_start)
        ##创建GameStart的Value
        game_start_value=ET.Element("Value")
        game_start_value.set("int",self.cachedRoleJoinData.GameStartValue)
        game_start.append(game_start_value)

        ##创建j_section的 GUID_Join
        guid_join=ET.Element("Key")
        guid_join.set("name","GUID_Join")
        j_section.append(guid_join)
        ##创建GameStart的Value
        guid_join_value=ET.Element("Value")
        guid_join_value.set("int",self.cachedRoleJoinData.GUID_JoinValue)
        guid_join.append(guid_join_value)



        ##判断加入玩家数
        joinPlayerCount=len(self.cachedRoleJoinData.JoinDic)
        print("joined role count:"+str(joinPlayerCount))
        if joinPlayerCount>0:
            random_GUID_JOIN_Value=random.randint(1,99999)
            print("random join_value:"+str(random_GUID_JOIN_Value))
            guid_join_value.set("int",str(random_GUID_JOIN_Value))
            index=0
            for x in self.cachedRoleJoinData.JoinDic:
                roleId=x
                roleNick=self.cachedRoleJoinData.JoinDic[x]
                print("role:"+roleNick+",id:"+roleId)
                ##创建玩家JPN
                index=index+1
                jpn=ET.Element("Key")
                jpn.set("name","JPN"+str(index))
                j_section.append(jpn)
                ##创建JPN值
                jpn_value=ET.Element("Value")
                jpn_value.set("int",str(roleId))
                jpn.append(jpn_value)
                ######创建玩家Section
                player_section=ET.Element("Section")
                player_section.set("name",str(roleId))
                root.append(player_section)
                ##创建玩家section的昵称信息
                pname=ET.Element("Key")
                pname.set("name","PName")
                player_section.append(pname)
                pname_value=ET.Element("Value")
                pname_value.set("text",roleNick)
                pname.append(pname_value)
        ## 清空JoinData
        self.ClearCachedRoleJoinData()
        ##增加换行符
        self.__indent(root)
        ##写文件
        if not os.path.exists(self.savePath):
            print("not exist,create file")
            open(self.savePath,'w').close()
        tree.write(self.savePath,encoding="utf-8",xml_declaration=True)
        print("save join success")
    def Read(self):
        #print("begin read xml file:"+self.savePath)

        tree = ET.parse(self.savePath)
        root = tree.getroot()
        for node in list(root):
            sectionName=node.get("name")
            if sectionName=="J":
                for node2 in list(node):
                    keyName= node2.get("name")
                    if keyName=="GameStart":
                        for node3 in list(node2):
                            keyValue=node3.get("int")
                            self.readedRoleJoinData.GameStartValue=keyValue
                            self.cachedRoleJoinData.GameStartValue=keyValue
                    if keyName=="GUID_Join_Out":
                        for node3 in list(node2):
                            keyValue=node3.get("int")
                            self.readedRoleJoinData.GUID_Join_OutValue=keyValue
                            self.cachedRoleJoinData.GUID_Join_OutValue=keyValue
                    if keyName=="GUID_Join":
                        for node3 in list(node2):
                            keyValue=node3.get("int")
                            self.readedRoleJoinData.GUID_JoinValue=keyValue
                            self.cachedRoleJoinData.GUID_JoinValue=keyValue



    def Join(self,id,nick):
        if not (id in self.cachedRoleJoinData.JoinDic) :
            self.cachedRoleJoinData.Join(id,nick)

# 弹幕
class DMXMLTool():
    # 增加换行符
    def __indent(self,elem, level=0):
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def __init__(self):
        path=os.path.split(os.path.realpath(__file__))[0]
        self.filePath="C:\\Users\\zhouhui\\Documents\\StarCraft II\\Banks\\PlayerDM"
        self.savePath =self.filePath ####f'{path}\\archiveXmlFile\\PlayerDM.xml'
        self.readedRoleDMData=RoleDM()
        self.cachedRoleDMData=RoleDM()

    def ClearCachedRoleDMData(self):
        self.cachedRoleDMData.DMDic.clear()
    def ClearCachedAllRoleDMData(self):
        self.cachedRoleDMData.AllDMDic.clear()
    def InitFile(self,dm_out_init_value,dm_in_init_value):
        #创建节点
        root=ET.Element("Bank")
        root.set("version","1")
        ##创建文档
        tree=ET.ElementTree(root)
        ##创建dm Section
        dm_section=ET.Element("Section")
        dm_section.set("name","DM")
        root.append(dm_section)
        ##创建dm_section的 DM_Out
        dm_out=ET.Element("Key")
        dm_out.set("name","DM_Out")
        dm_section.append(dm_out)
        ##创建 DM_Out 的Value
        dm_out_value=ET.Element("Value")
        dm_out_value.set("int",dm_out_init_value)
        dm_out.append(dm_out_value)
   
        ##创建dm_section的 DM_In
        dm_in=ET.Element("Key")
        dm_in.set("name","DM_In")
        dm_section.append(dm_in)
        ##创建 DM_In 的Value
        dm_in_value=ET.Element("Value")
        dm_in_value.set("int",dm_in_init_value)
        dm_in.append(dm_in_value)
 
        ##增加换行符
        self.__indent(root)
        ##写文件
        if not os.path.exists(self.savePath):
            print("not exist,create file")
            open(self.savePath,'w').close()
        tree.write(self.savePath,encoding="utf-8",xml_declaration=True)
        print("init dm file success")
    def Save(self):
        #创建节点
        root=ET.Element("Bank")
        root.set("version","1")
        ##创建文档
        tree=ET.ElementTree(root)
        ##创建 DM Section
        dm_section=ET.Element("Section")
        dm_section.set("name","DM")
        root.append(dm_section)
        ##创建 dm_section的 DM_Out
        dm_out=ET.Element("Key")
        dm_out.set("name","DM_Out")
        dm_section.append(dm_out)
        ##创建 DM_Out的Value
        dm_out_value=ET.Element("Value")
        dm_out_value.set("int",self.cachedRoleDMData.DM_OutValue)
        dm_out.append(dm_out_value)
        
        ##创建 dm_section的 DM_In
        dm_in=ET.Element("Key")
        dm_in.set("name","DM_In")
        dm_section.append(dm_in)
        ##创建 DM_In 的Value
        dm_in_value=ET.Element("Value")
        dm_in_value.set("int",self.cachedRoleDMData.DM_InValue)
        dm_in.append(dm_in_value)



        ##判断加入玩家数
        dmPlayerCount=len(self.cachedRoleDMData.DMDic)
        print("DMed role count:"+str(dmPlayerCount))
        if dmPlayerCount>0:
            random_DM_In_Value=random.randint(1,99999)
            print("random DM_In_value:"+str(random_DM_In_Value))
            dm_in_value.set("int",str(random_DM_In_Value))
            index=0
            for x in self.cachedRoleDMData.DMDic:
                roleId=x
                conent=self.cachedRoleDMData.DMDic[x]
                print("id:"+roleId+", content:"+conent)
                #TODO TODO TODO
                ##创建玩家DM
                index=index+1
                dmdm=ET.Element("Key")
                dmdm.set("name","DM"+str(index))
                dm_section.append(dmdm)
                ##创建 DM 值
                dm_value=ET.Element("Value")
                dm_value.set("int",str(roleId))
                dmdm.append(dm_value)
                ######创建玩家Section
                player_section=ET.Element("Section")
                player_section.set("name",str(roleId))
                root.append(player_section)
                ##创建玩家section的 内容 信息
                pcontent=ET.Element("Key")
                pcontent.set("name","DM")
                player_section.append(pcontent)
                pname_value=ET.Element("Value")
                pname_value.set("text",conent)
                pcontent.append(pname_value)
        ## 清空DMData
        self.ClearCachedRoleDMData()
        ##增加换行符
        self.__indent(root)
        ##写文件
        if not os.path.exists(self.savePath):
            print("not exist,create file")
            open(self.savePath,'w').close()
        tree.write(self.savePath,encoding="utf-8",xml_declaration=True)
        print("save dm success")
    def Read(self):
        #print("begin read xml file:"+self.savePath)

        tree = ET.parse(self.savePath)
        root = tree.getroot()
        for node in list(root):
            sectionName=node.get("name")
            if sectionName=="DM":
                for node2 in list(node):
                    keyName= node2.get("name")
                     
                    if keyName=="DM_Out":
                        for node3 in list(node2):
                            keyValue=node3.get("int")
                            self.readedRoleDMData.DM_OutValue=keyValue
                            self.cachedRoleDMData.DM_OutValue=keyValue
                    if keyName=="DM_In":
                        for node3 in list(node2):
                            keyValue=node3.get("int")
                            self.readedRoleDMData.DM_InValue=keyValue
                            self.cachedRoleDMData.DM_InValue=keyValue



    def Add(self,id,content):
        if not (id in self.cachedRoleDMData.DMDic) :
            self.cachedRoleDMData.Add(id,content)
