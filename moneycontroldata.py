from bs4 import BeautifulSoup
from configparser import ConfigParser
#import logging
import requests
import sys

class MoneyControl:
    def __init__(self,conf,symb):
        self._sym = symb
        self._config = conf
        self._sectordict = eval(self._config['MAPPINGS']['sector_map'])
        self._symbmapping = eval(self._config['MAPPINGS']['sym_map'])
       
    def scrapedata(self):
        url = self._config['MAIN']['base_url'] + "/" + self._sectordict[self._sym] + "/" + self._symbmapping[self._sym] + "/" + self._sym
        
        try:
            page = requests.get(url)
            
        except requests.RequestException as e:
            raise e
            
 #       logging.info("Downloading data for ",self._sym)
        soup = BeautifulSoup(page.text,'html.parser')
        
        bseprice = soup.find('input',attrs={"id":"bprevclose"})["value"]
        nseprice = soup.find('input',attrs={"id":"nprevclose"})["value"]
        
        bseid = soup.find('input',attrs={"id":"bseid"})["value"]
        nseid = soup.find('input',attrs={"id":"nseid"})["value"]
        
        bsedaylow = soup.find('div',attrs={"class":"clearfix lowhigh_band todays_lowhigh_wrap"}).text.split()[0]
        bsedayhigh = soup.find('div',attrs={"class":"clearfix lowhigh_band todays_lowhigh_wrap"}).text.split()[3]
        
        bseyearlow = soup.find('div',attrs={"class":"clearfix lowhigh_band week52_lowhigh_wrap"}).text.split()[0]
        bseyearhigh = soup.find('div',attrs={"class":"clearfix lowhigh_band week52_lowhigh_wrap"}).text.split()[4]
        
        
        bsevwap = soup.find('div',attrs={"class":"disin vt"}).text.split()[1]
        
        nsedaylow = soup.find('div',attrs={"class":"nsert"}).find('div',attrs={"class":"clearfix lowhigh_band todays_lowhigh_wrap"}).text.split()[0]
        nsedayhigh = soup.find('div',attrs={"class":"nsert"}).find('div',attrs={"class":"clearfix lowhigh_band todays_lowhigh_wrap"}).text.split()[3]
        
        nseyearlow = soup.find('div',attrs={"class":"nsert"}).find('div',attrs={"class":"clearfix lowhigh_band week52_lowhigh_wrap"}).text.split()[0]
        nseyearhigh = soup.find('div',attrs={"class":"nsert"}).find('div',attrs={"class":"clearfix lowhigh_band week52_lowhigh_wrap"}).text.split()[4]
        
        
        nsevwap = soup.find('div',attrs={"class":"nsert"}).find('div',attrs={"class":"disin vt"}).text.split()[1]
        print("BSE-ID ",bseid,"NSE-ID ",nseid,"BSE-Price",bseprice,"NSE-Price ",nseprice,"BSE-DayLow ",bsedaylow,"BSE-DayHigh ",bsedayhigh,"BSE-VWAP",bsevwap,"BSE-YearLow",bseyearlow,"BSE-YearHigh ",bseyearhigh,"NSE-DayLow ",nsedaylow,"NSE-DayHigh ",nsedayhigh,"NSE-VWAP",nsevwap,"NSE-YearLow",nseyearlow,"NSE-YearHigh ",nseyearhigh)
               
        
if __name__ == "__main__":
    config = ConfigParser()
    config.read(sys.argv[1])
    m = MoneyControl(config,sys.argv[2])
    m.scrapedata()
    