from bs4 import BeautifulSoup
from configparser import ConfigParser
import pandas as pd
import requests
import sys

class YahooDataParser:
    
    def __init__(self,ini):
        self.iniconfig = ini
        self.download_data()

    def downloadurl(self,url):
        page = requests.get(url)
        return BeautifulSoup(page.content,'html.parser')
        
    def get_activestocks(self):
        
        names = []
        prices = []
        volume = []
        perchange = []
        change = []
        const = 50
        for i in range(4):
            url = "https://finance.yahoo.com/most-active?count=" +str(const) + "&offset=" +str(i*const)           
            soup = self.downloadurl(url)
            for x in soup.find_all('tr',attrs={'class':"simpTblRow"}):
                names.append(x.find('td',attrs={'aria-label':"Name"}).text)
                volume.append(x.find('td',attrs={'aria-label':"Volume"}).text)
                prices.append(x.find('td',attrs={'aria-label':"Price (Intraday)"}).text)
                perchange.append(x.find('td',attrs={'aria-label':"% Change"}).text)
                change.append(x.find('td',attrs={'aria-label':"Change"}).text)
                
        return pd.DataFrame({'Name':names,'Price':prices,'Change':change,'%Change':perchange,'Volume':volume})
    
    def get_commodities(self):
        
        names = []
        prices = []
        volume = []
        perchange = []
        change = []
        oi = []
        
        url = "https://finance.yahoo.com/commodities"
        soup = self.downloadurl(url)
        res  = soup.find('tbody')
        for x in res.find_all('tr'):   
            names.append(x.find('td',attrs = {'class':"data-col1"}).text)
            volume.append(x.find('td',attrs = {'class':"data-col6"}).text)
            oi.append(x.find('td',attrs = {'class':"data-col7"}).text)
            prices.append(x.find('td',attrs = {'class':"data-col2"}).text)
            change.append(x.find('td',attrs = {'class':"data-col4"}).text)
            perchange.append(x.find('td',attrs = {'class':"data-col5"}).text)
            
        return pd.DataFrame({'Name':names,'Price':prices,'Change':change,'%Change':perchange,'Volume':volume,'OpenInterest':oi})
           
    def get_cryptocurrencydata(self):
        
        names = []
        prices = []
        volume = []
        perchange = []
        change = []
        csupply = []
        const = 50
        for i in range(3):
            url = "https://finance.yahoo.com/cryptocurrencies?count=" +str(const) + "&offset=" +str(i*const)
            soup = self.downloadurl(url)
            res  = soup.find('tbody')
            for x in res.find_all('tr'): 
                names.append(x.find('td',attrs={'aria-label':"Name"}).text)
                volume.append(x.find('td',attrs={'aria-label':"Total Volume All Currencies (24Hr)"}).text)
                prices.append(x.find('td',attrs={'aria-label':"Price (Intraday)"}).text)
                perchange.append(x.find('td',attrs={'aria-label':"% Change"}).text)
                change.append(x.find('td',attrs={'aria-label':"Change"}).text)
                csupply.append(x.find('td',attrs={'aria-label':"Circulating Supply"}).text)
                            
        return pd.DataFrame({'Name':names,'Price':prices,'Change':change,'%Change':perchange,'Volume':volume,'Circulating Supply':csupply})
    
    def get_currencies(self):
        
        names = []
        prices = []
        perchange = []
        change = []
    
        url = "https://finance.yahoo.com/currencies"
        soup = self.downloadurl(url)
        res  = soup.find('tbody')
        for x in res.find_all('tr'):   
            names.append(x.find('td',attrs = {'class':"data-col1"}).text)
            prices.append(x.find('td',attrs = {'class':"data-col2"}).text)
            change.append(x.find('td',attrs = {'class':"data-col3"}).text)
            perchange.append(x.find('td',attrs = {'class':"data-col4"}).text)
            
        return pd.DataFrame({'Name':names,'Price':prices,'Change':change,'%Change':perchange})

    def download_data(self):
        
        if self.iniconfig.get('MAIN','what_scrape') == "Active Stocks":
            data = self.get_activestocks()
            
        elif self.iniconfig.get('MAIN','what_scrape') == "Commodities":
            data = self.get_commodities()
            
        elif self.iniconfig.get('MAIN','what_scrape') == "CryptoCurrency":
            data = self.get_cryptocurrencydata()    
            
        elif self.iniconfig.get('MAIN','what_scrape') == "Currency":
            data = self.get_currencies()
            
        print(data.head(10))

if __name__ == "__main__":
    config = ConfigParser()
    config.read(sys.argv[1])
    ydf = YahooDataParser(config)

