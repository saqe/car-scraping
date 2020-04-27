from MySQLDBHandler import MySQLDBHandler
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CarDatabaseHandler:    
    def __init__(self,host,user,passwd,database):
        super().__init__()
        self.db=MySQLDBHandler(_host_=host,_user_=user,_passwd_=passwd,_database_=database)
        if self.db.is_connected():
            print("Ready to start")
        self.LIST_OF_REF_NUM_AVAILABLE=set(self.db.fetch_many_first("SELECT REF_NO FROM cars where IS_AVAILABLE='Yes';"))
        self.LIST_OF_REF_NUM_NOT_AVAILABLE=set(self.db.fetch_many_first("SELECT REF_NO FROM cars where IS_AVAILABLE='No';"))

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

    # @not developed
    def updatePreExistData(self, dataDict):
        pass
        # for key in ['FAVORITS','Visits','Price','Premium','Preu_Ara','Preu_Abans']:
        #     if key not in dataDict.keys():continue
        #     value=str(dataDict[key])
        #     link_ref=dataDict['URL_LINK'].split('/')[5]

            # Check if its the key is already same, don't track the changes
            # if not ifDatabaseValueMatch(link_ref,key,value):
            #     self.updateDatabaseValueForRefNo(link_ref,key,value)
            #     if key not in ['FAVORITS','Visits']:
            #         logger.info('For REF_NOlink_ref:#'++' is changed for <'+key+'> to '+str(value))

    def get_db_value_match_for_ref_no(self,ref_no,key,value) -> str:
        SELECT_GET_VALUE="SELECT {key} FROM cars where REF_NO={ref_no} and {key}={value} ;'".format(key=key,ref_no=ref_no,value=value)
        result=self.db.fetch_one(SELECT_GET_VALUE)[0]
        return str(result)

    
    # @Tested 
    def getAvailableCarsRefNoList(self) -> list:
        return self.db.fetch_many("SELECT REF_NO FROM cars where IS_AVAILABLE='Yes';")
    

    def logRefChanges(self,ref_no,change_type,value):
        TRACK_SQL_INSERT_QUERY="INSERT INTO TrackChanges ( car_ref_id , change_type , change_value ) VALUES ( {},'{}','{}');".format(ref_no,change_type,value)
        self.db.query(TRACK_SQL_INSERT_QUERY)
        logger.info("Data added inside TrackChanges",ref_no,change_type,value)

    def putCarAvailablityDown(self,ref_num)-> bool:
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Change Status and Last removed value too
        self.updateDatabaseValueForRefNo(self,ref_num=ref_num,key='IS_AVAILABLE',value='No',is_track_required=True)
        self.updateDatabaseValueForRefNo(self,ref_num=ref_num,key='LAST_REMOVED',value=current_date)
    
    def putCarAvailablityUP(self,ref_num)-> bool:
        self.updateDatabaseValueForRefNo(self,ref_num=ref_num,key='IS_AVAILABLE',value='Yes',is_track_required=True)

    def updateDatabaseValueForRefNo(self,ref_num,key,value,is_track_required=False):
        SQL_UPDATE_DATA_QUERY='UPDATE cars SET {key} = "{value}" WHERE REF_NO = {ref_no};'.format(key=key,value=value,ref_no=ref_num)

        try:        self.db.query.execute(SQL_UPDATE_DATA_QUERY)
        except:     logger.error('@changeCarDatabaseValue UPDATE Car => {} '.format(SQL_UPDATE_DATA_QUERY))

        if is_track_required:                   self.logRefChanges(ref_num,key,value)
        if key not in ['FAVORITS','Visits']:    logger.info('{ref_num} is UPDATED for key:{key} and value:{value}'.format(ref_num=ref_num,key=key,value=value))


    def update_already_exists_car_values(self,dataDict):
        
            
