class RoleDM():
    def __init__(self):        
        self.DM_InValue="0"
        self.DM_OutValue="0"
        self.AllDMDic={}
        self.DMDic={}        


    def Add(self,id,content):
        if id in self.AllDMDic:
            return 
        count=len(self.DMDic)    
        if count<10:            
            self.AllDMDic[id]=content
            self.DMDic[id]=content