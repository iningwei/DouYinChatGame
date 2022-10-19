import os
import xml.etree.ElementTree as ET

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
        self.savePath = f'{path}\\archiveXmlFile\\default.xml'

    def Save(self):
        #创建节点
        root=ET.Element("Bank")
        root.set("version","1")
        ##创建文档
        tree=ET.ElementTree(root)

        ##增加换行符
        ##__indent(root)
        ##写文件
        tree.write(self.savePath,encoding="utf-8",xml_declaration=True)
        print("save success")