from datetime import datetime

class MyDateTime:
    def getDate(self)->str:
        return datetime.now().strftime("%Y-%m-%d")
    
    def getTime(self,is24Hr=False,seperator=":")->str:
        return datetime.now().strftime("%H{seperate}%M".format(seperate=seperator) if is24Hr else "%I{seperate}%M %p".format(seperate=seperator))
    
    def getTimeWithSeconds(self,is24Hr=False,seperator=":")->str:
        return datetime.now().strftime("%H{seperate}%M{seperate}%S".format(seperate=seperator) if is24Hr else "%I{seperate}%M{seperate}%S %p".format(seperate=seperator))
    
    def getYear(self,isFull=False)->int:
        return int(datetime.now().strftime("%Y" if isFull else "%y"))
    
    def getMonthName(self,isFull=False)->str:
        return int(datetime.now().strftime("%B" if isFull else "%b"))
    
    # def getMonthNum(self)->int:
    #     return 