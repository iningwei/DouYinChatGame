from genericpath import isfile
import os
import xml.etree.ElementTree as ET



from archives.roleJoin import RoleJoin

# 教程
# https://blog.csdn.net/hu694028833/article/details/81089959?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-81089959-blog-119954423.pc_relevant_3mothn_strategy_and_data_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-81089959-blog-119954423.pc_relevant_3mothn_strategy_and_data_recovery&utm_relevant_index=6







# 增加换行符
def __indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class XMLTool():
    def __init__(self):
        path=os.path.split(os.path.realpath(__file__))[0]
        self.savePath = f'{path}\\archiveXmlFile\\PlayerJoin.SC2Bank.xml'
        self.readedRoleJoinData=RoleJoin()
        self.cachedRoleJoinData=RoleJoin()

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
        guid_join_out.set("Key","GUID_Join_Out")
        j_section.append(guid_join_out)
        ##创建GUID_Join_Out的Value
        guid_join_out_value=ET.Element("Value")
        guid_join_out_value.set("int",self.cachedRoleJoinData.GUID_Join_OutValue)
        ##TODO:

        ##增加换行符
        ##__indent(root)
        ##写文件
        if not os.path.exists(self.savePath):
            print("not exist,create file")
            open(self.savePath,'w').close()
        tree.write(self.savePath,encoding="utf-8",xml_declaration=True)
        print("save success")
    def Read(self):
        print("begin read xml file:"+self.savePath)

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
    
    def ClearCachedRoleJoinData(self):
        self.cachedRoleJoinData.JoinDic.clear()
    def Join(self,id,nick):
        if not id in self.cachedRoleJoinData.JoinDic and len(self.cachedRoleJoinData.JoinDic)<10:
            self.cachedRoleJoinData.JoinDic[id]=nick