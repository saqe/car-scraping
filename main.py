from CarDatabaseHandler import CarDatabaseHandler
from Scraper import Scraper
import os
import logging
from dotenv import load_dotenv
load_dotenv()


REQUEST_HEADER={
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'upgrade-insecure-requests': '1',
  'Host': os.getenv('REQUEST_HOST'),
  'Cookie':os.getenv('REQUEST_COOKIES'),
  'user-agent': os.getenv('REQUEST_USER_AGENT')
}

HEADER_FOR_DATA=['Marca', 'Gamma', 'Model', 'Versió', 'Color Exterior','Quilòmetres', 'Price', 'Preu Ara', 'Preu Abans', 'Potencia (CV)', 'Canvi','Tracció','Color Interior','Combustible','Data Primera Matriculació','Data Fabricació', 'Disponibilitat','Estat','Premium','Vists', 'FAVORITS','Company Name','Motor','Cubicatge','Potencia (KW)','Par Motor (NM)']

CHANGE_VALUE_DICT={
  'Versió':'Versio',
  'Quilòmetres':'Quilometres',
  'Potencia (CV)':'Potencia_CV',
  'Tracció':'Traccio',
  'Color Exterior':'Color_Exterior',
  'Color Interior':'Color_Interior',
  'Potencia (KW)':'Potencia_KW',
  'Par Motor (NM)':'Par_Motor_NM',
  'Data Primera Matriculació':'Data_Primera',
  'Data Fabricació':'Data_Fabricacio',
}

cars_db=CarDatabaseHandler(
    host=os.getenv('DATABASE_HOST'),
    user=os.getenv('DATABASE_USER'),
    passwd=os.getenv('DATABASE_PASS'),
    database=os.getenv('DATABASE_NAME'))

scraper=Scraper()
scraper.set_request_header(REQUEST_HEADER)
scraper.set_search_page_api(os.getenv('SEARCH_API'))
scraper.set_main_url(os.getenv('BASE_URL'))
scraper.set_database_header(HEADER_FOR_DATA)
scraper.set_dict_value_change(CHANGE_VALUE_DICT)

set_of_car_available_today=set()

logging.basicConfig(filename=__name__+'.log', filemode='a', format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO)
logger = logging.getLogger()


for page_number in range(1,115):
    print(page_number)
    list_of_cars=scraper.scrape_cars_list(page_number)
    for car in list_of_cars:
        dataDict=scraper.scrape_car_detail_from_search_result(car)
        ref_no=int(dataDict['REF_NO'])
        set_of_car_available_today.add(ref_no)

        if cars_db.is_ref_num_exist(ref_no):
            #If REF_NO Exists but the availbility status was DOWN.
            if cars_db.is_ref_num_not_available(ref_no):
                print(ref_no," is up again")
                cars_db.putCarAvailablityUP(ref_no)
                logger.info(str(ref_no)+' is available again, Refreshing Values in database')
                dataDict=scraper.scrape_car_profile_information(dataDict)
            cars_db.update_already_exists_car_values(dataDict)
            continue
        dataDict=scraper.scrape_car_profile_information(dataDict)
        cars_db.insert_new_car(dataDict)