from MySQLDBHandler import MySQLDBHandler
from MyDateTime import DatetimeUtil
import logging

logger = logging.getLogger(__name__+'.log')
logging.basicConfig(level=logging.WARNING,format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s')
date=DatetimeUtil()
class CarDatabaseHandler:    
    def __init__(self,host,user,passwd,database):
        super().__init__()
        self.db=MySQLDBHandler(_host_=host,_user_=user,_passwd_=passwd,_database_=database)
        if self.db.is_connected():
            print("Ready to start")
        self.LIST_OF_REF_NUM_AVAILABLE=set(self.db.fetch_many_first("SELECT REF_NO FROM cars where IS_AVAILABLE='Yes';"))
        self.LIST_OF_REF_NUM_NOT_AVAILABLE=set(self.db.fetch_many_first("SELECT REF_NO FROM cars where IS_AVAILABLE='No';"))

    # @tested 
    def getAvailableCarsRefNoListFromDatabase(self) -> list:        return self.db.fetch_many("SELECT REF_NO FROM cars where IS_AVAILABLE='Yes';")
    # @tested
    def get_list_of_available_ref_no(self)-> list:      return self.LIST_OF_REF_NUM_AVAILABLE
    # @tested
    def get_list_of_not_available_ref_no(self)-> list:  return self.LIST_OF_REF_NUM_NOT_AVAILABLE
    # @tested
    def is_ref_num_available(self,ref_no)->bool:        return True if int(ref_no) in self.LIST_OF_REF_NUM_AVAILABLE else False
    # @tested
    def is_ref_num_not_available(self,ref_no)->bool:    return True if int(ref_no) in self.LIST_OF_REF_NUM_NOT_AVAILABLE else False
    # @tested
    def is_ref_num_exist(self,ref_no) -> bool:          return True if self.is_ref_num_available(ref_no) or self.is_ref_num_not_available(ref_no) else False
    
    def get_db_value(self,ref_no,key) -> str:           return str(self.db.fetch_one("SELECT {key} FROM cars where REF_NO={ref_no};".format(key=key,ref_no=ref_no))[0])
    
    def is_database_value_match(self,ref_num,key,value):
        return self.get_db_value(ref_num,key)==value

    def logRefChanges(self,ref_no,change_type,value):
        TRACK_SQL_INSERT_QUERY="INSERT INTO TrackChanges ( car_ref_id , change_type , change_value ) VALUES ( {},'{}','{}');".format(ref_no,change_type,value)
        self.db.query(TRACK_SQL_INSERT_QUERY)
        logger.info("Data added inside TrackChanges",ref_no,change_type,value)

    def putCarAvailablityDown(self,ref_num)-> bool:
        # Change Status and Last removed value too
        self.updateDatabaseValueForRefNo(ref_num=ref_num,key='IS_AVAILABLE',value='No',is_track_required=True)
        self.updateDatabaseValueForRefNo(ref_num=ref_num,key='LAST_REMOVED',value=date.getFormatedDate())
    
    def putCarAvailablityUP(self,ref_num)-> bool:
        self.updateDatabaseValueForRefNo(ref_num,key='IS_AVAILABLE',value='Yes',is_track_required=True)

    def updateDatabaseValueForRefNo(self,ref_num,key,value,is_track_required=False):
        SQL_UPDATE_DATA_QUERY='UPDATE cars SET {key} = "{value}" WHERE REF_NO = {ref_no};'.format(key=key,value=value,ref_no=ref_num)

        try:        self.db.query(SQL_UPDATE_DATA_QUERY)
        except Exception as error:     
            logger.error('@changeCarDatabaseValue UPDATE Car => {} '.format(SQL_UPDATE_DATA_QUERY),error)
            input()

        if is_track_required:                   self.logRefChanges(ref_num,key,value)
        if key not in ['FAVORITS','Visits']:    logger.info('{ref_num} is UPDATED for key:{key} and value:{value}'.format(ref_num=ref_num,key=key,value=value))


    def update_already_exists_car_values(self,dataDict):
        ref_num=dataDict['REF_NO']
        for key in ['FAVORITS','Visits','Price','Premium','Preu_Ara','Preu_Abans']:
            if key not in dataDict.keys():
                logger.info(str(key)+" was used as a key inside @update_already_exists_car_values")
                continue
            value=str(dataDict[key])

            # Check if its the key is already same, don't track the changes
            if not self.is_database_value_match(ref_num,key,value):
                self.updateDatabaseValueForRefNo(ref_num,key,value)
            
            if key not in ['FAVORITS','Visits']: 
                logger.info('For REF# {ref_num} is changed for <{key}> to {value}'.format(ref_num=ref_num,key=key,value=value))
            

    def insert_new_car(self,rowDict):
        print("New Car received")
        # for key,value in rowDict.items():rowDict[key]='"'+value.replace('"','')+'"'
        # SQL_INSERT_QUERY='INSERT INTO cars( %s ) VALUES ( %s );' % (', '.join(rowDict.keys()),', '.join(rowDict.values()))
        # try:
        
        # except :
        #     logger.error('SQL QUERY Error @writeNewCarRow')
        #     logger.info(SQL_INSERT_QUERY)
        #     print(SQL_INSERT_QUERY)
        # mydb.commit()
        # # Track changes of newly added cars too.
        # for key in ['Price']:
        #     trackChanges(rowDict['REF_NO'],key,rowDict[key],is_new=True)
        # logger.info(str(rowDict['REF_NO'])+" is inserted")