class RoleJoin():
    def __init__(self):        
        self.GameStartValue ="0"
        self.GUID_JoinValue="0"
        self.GUID_Join_OutValue="0"
        self.AllJoinDic={}
        self.JoinDic={}        


    def Join(self,id,nick):
        if id in self.AllJoinDic:
            return 
        count=len(self.JoinDic)    
        if count<10:            
            self.AllJoinDic[id]=nick
            self.JoinDic[id]=nick