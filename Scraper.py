import requests as re
from bs4 import BeautifulSoup
from MyDateTime import DatetimeUtil
import time
import logging
# 'Logs/'+
logging.basicConfig(filename=__name__+'.log', filemode='a', format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO)
logger = logging.getLogger()

date=DatetimeUtil()

class Scraper:
    def __init__(self,):
        super().__init__()
    
    def set_request_header(self,REQUEST_HEADER):    self.REQUEST_HEADER=REQUEST_HEADER
    def set_search_page_api(self,SEARCH_API):       self.SEARCH_API=SEARCH_API
    def set_main_url(self,MAIN_URL):                self.MAIN_URL=MAIN_URL
    def set_database_header(self,DB_HEADER):        self.HEADER_FOR_DATA=DB_HEADER
    def set_dict_value_change(self, dictChange):    self.CHANGE_VALUE_DICT=dictChange

    def scrape_cars_list(self,page_number):
        while True:
            try:
                page=re.get(self.SEARCH_API.format(page_number=str(page_number)),headers=self.REQUEST_HEADER)
                if page.status_code!=200:
                    logger.warning("For page#{} STATUS CODE : {}".format(page_number,page.status_code))
            except re.exceptions.ConnectionError as error:
                time.sleep(23)
                logger.exception('MAIN URL Connection Error, Trying Again')
            finally:
                # Scraping done smoothly break the loop
                break
        pageParser=BeautifulSoup(page.content,'html.parser')
        return pageParser.find('div',class_='aparador').find('ul',recursive=False).findAll('li',recursive=False)

    def scrape_car_detail_from_search_result(self,row) -> dict:
        dataDict={}
        dataDict['Title']=row.find('div',class_='box-titol').text.strip()
        dataDict['URL_LINK']=self.MAIN_URL+row.find('a')['href']
        dataDict['REF_NO']=dataDict['URL_LINK'].split('/')[5]  
        dataDict['Price']=row.find('div',class_='uk-float-right').text.replace('Consultar preu','').replace('.','').strip()
        dataDict['FAVORITS']=row.find('i',class_='uk-icon-star').parent.getText().strip()
        dataDict['Visits']=row.find('i',class_='uk-icon-eye').parent.getText().replace('VISITES','').strip().split(' ')[-1].replace('.','')

        if row.find('span',class_='uk-badge uk-badge-danger') is not None:      dataDict['Preu_Ara']=row.find('span',class_='uk-badge uk-badge-danger').text.replace('Preu abans:','').replace('.',',').strip()
        if row.find('span',class_='uk-badge uk-badge-success') is not None:     dataDict['Preu_Abans']=row.find('span',class_='uk-badge uk-badge-success').text.replace('Preu ara:','').replace('.',',').strip()
        
        premium_tag=row.find('span',{'class':'uk-text-bold','style':'color: #622e2e'})

        if premium_tag is not None and "PREMIUM" in premium_tag.getText():
            dataDict['Premium']='Yes'

        return dataDict

    def scrape_car_profile_information(self,dataDict):
        while True:
            try:
                link=dataDict['URL_LINK']
                carPage=re.get(link,headers=self.REQUEST_HEADER)
                if carPage.status_code!=200: 
                    logger.warning("For page:{} STATUS CODE : {}".format(link,carPage.status_code))
            except re.exceptions.ConnectionError as error:
                logger.info(dataDict['URL_LINK'])
                logger.exception('Connection Error, Trying Again')
                continue
            finally:
                break

        carParser=BeautifulSoup(carPage.content,'html.parser')

        rightDiv=carParser.find('div',class_='uk-width-1-1 uk-width-small-1-1 uk-width-medium-1-3 uk-width-large-1-3')
        dataDict['Company_Name']=rightDiv.find('span',class_='uk-text-primary uk-text-bold uk-text-uppercase').text

        for tablerow in carParser.findAll('td',class_='uk-width-1-3'):
            key=tablerow.text.strip()
            value=tablerow.findNext('td',class_='uk-width-3-3 uk-text-bold')

            if key in self.HEADER_FOR_DATA:
                if key in self.CHANGE_VALUE_DICT.keys():key=self.CHANGE_VALUE_DICT[key]
                dataDict[key]=value.text.strip().replace('"','')
        
        if carParser.find('i',class_='uk-icon-diamond'):dataDict['Premium']='Yes'
        
        profile_page_ref_no=carParser.find('div',class_='uk-float-right uk-width-1-2').text.replace('REF:','').strip()
        if profile_page_ref_no != dataDict['REF_NO']:
            logger.exception("CRITICAL ERROR - REF # doesn't match. search:{} & profile:{}".format(profile_page_ref_no,dataDict['REF_NO']),error)
            
        dataDict['REF_NO']=profile_page_ref_no
        footer=carParser.find('div',class_='box-footer')
        dataDict['MODIFCATION_TIME_SITE']=footer.find('div',class_='uk-float-right').text.strip().split('  ')[0].replace('MODIFICAT:','').strip()

        dataDict['FIRST_APPEARED']=date.getFormatedDate()
        dataDict['IS_AVAILABLE']='Yes'

        #remove extra Tags from description
        # [tag.extract() for tag in carParser.find('div',class_='uk-block').findAll(['h2','span','p','em'],recursive=False)]
        dataDict['Description']=carParser.find('div',class_='uk-block').text.strip().replace('"','\'')
        if 'Quilometres' in dataDict:
            dataDict['Quilometres']=int(dataDict['Quilometres'].replace('Km.','').replace('.',',').strip())

        return dataDict
