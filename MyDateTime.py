from datetime import datetime,timedelta

class DatetimeUtil():
    def __init__(self,dt=None):
        super().__init__()
        self.dt=dt

    def set_datetimestamp(self,dt):
        self.dt=dt

    def getFormatedDate(self)->str:
        if self.dt is None:self.dt=datetime.now()
        return self.dt.strftime("%Y-%m-%d")

    def getMonthNum(self,dt=datetime.now())->int:     
        if self.dt is None:self.dt=datetime.now()
        return int(self.dt.strftime("%m"))

    def getWeekDayNum(self,dt=datetime.now())->int:  
        if self.dt is None:self.dt=datetime.now()
        return int(self.dt.strftime("%w"))

    def getWeekDayName(self,dt=datetime.now())->str:      
        if self.dt is None:self.dt=datetime.now()
        return self.dt.strftime("%A")

    def getFormatedTime(self,is24Hr=False,seperator=":")->str:              
        if self.dt is None:self.dt=datetime.now()
        return self.dt.strftime("%H{seperate}%M".format(seperate=seperator) if is24Hr else "%I{seperate}%M %p".format(seperate=seperator))
    
    def getFormatedTimeWithSeconds(self,is24Hr=False,seperator=":")->str:   
        if self.dt is None:self.dt=datetime.now()
        return self.dt.strftime("%H{seperate}%M{seperate}%S".format(seperate=seperator) if is24Hr else "%I{seperate}%M{seperate}%S %p".format(seperate=seperator))
    
    def getYear(self,isFull=False,dt=datetime.now())->int:        
        if self.dt is None:self.dt=datetime.now()
        return int(self.dt.strftime("%Y" if isFull else "%y"))

    def getMonthName(self,isFull=False,dt=datetime.now())->str:   
        if self.dt is None:self.dt=datetime.now()
        return self.dt.strftime("%B" if isFull else "%b")
    
    def getDatetime(self)->datetime:
        if self.dt is None:self.dt=datetime.now()
        return self.dt

    def getNextDay(self,num_days=1):
        if self.dt is None:self.dt=datetime.now() 
        return DatetimeUtil(self.dt+timedelta(days=num_days))

    def getPreviousDay(self,num_days=-1):
        if self.dt is None:self.dt=datetime.now() 
        return DatetimeUtil(self.dt+timedelta(days=num_days))
