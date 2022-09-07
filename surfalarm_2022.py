import requests
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import pandas as pd

def region_spot(region):
    url = f"https://www.surf-report.com/meteo-surf/france/{region.lower()}"
    response = requests.get(url)
    return response.text

def get_spots(region):
    
    ### This function gets all the spots NAME, TOWN, REGION, URL, for a given region 
    
    # Get the HTML with the previous function
    html = region_spot(region)
    
    # Start the search
    soup = BeautifulSoup(html, "html.parser")
    spots= []
    for spot in soup.find_all("div", class_ ="card forecast list"):
        
        #get the spot town
        spot_town = spot.find("b").string
        
        #get the spot name
        if spot.find("br"):
            spot_name = spot.br.next_sibling
        else:
            spot_name = "No spot name"
        
        #get the URL
        url_end = spot.find("a")["href"]
        url = "https://www.surf-report.com/meteo-surf" + url_end
        
        spots.append([spot_name, spot_town, region, url])
        
    return spots

def douille_datetime_2(day):
    output = "2022-"
    
    # deleting the alphabetical version of day
    
    day = day[5:]
    for char in day:
        if not char.isnumeric():
            day = day[1:]
        else :
            break
    
    # changing the month to a number
    month = day[2:]
    for char in month:
        if not char.isalpha():
            month = month[1:]
        else :
            break
    months_dict = {"Janvier":"01","Fevrier":"02","Mars":"03",
                   "Avril":"04","Mai":"05","Juin":"06",
                   "Juillet":"07","Août":"08","Septembre":"09",
                   "Octobre":"10","Novembre":"11","Décembre":"12"}
    month_num = months_dict[month]

    # 0 padding the day of the date
    day = ''.join(ch for ch in day if ch.isnumeric())
    if len(day) == 1:
        day = "0" + day
    pass

    output = output + month_num + "-" +  day
    
    #return output
    return date.fromisoformat(output)

def spot_to_html(spot_url):
    response = requests.get(spot_url)
    return response.text

def get_spot_data(spot_url):
    
    ### This function will look if a spot has more than 10 stars in 1 day in the next 3 days
    
    # Getting the HTML of the spot with previous function
    spot_html = spot_to_html(spot_url)
    soup = BeautifulSoup(spot_html, "html.parser")
    
    good_days=[]
    
    for day in soup.find_all("div", class_="forecast-tab"):
        
        # Count the number of stars for a day
        stars = len(day.find_all("i", class_="fa fa-star"))
        
        # Look at the forecast of the next 3 days only
        if stars > 9:
            day_date_string = day.find("b").string
            day_date = douille_datetime_2(day_date_string)
            jour = (day_date - today).days
            
            # for waves of next 3 days
            if jour > 0 and jour < 4:
                good_days = good_days + [spot_url, stars, day_date_string]

            #for today's waves:
            #if jour < 1:
            pass
        pass
    return good_days

def region_spots_data(region_liste = ["Nord", "Manche", "Bretagne", "loire-atlantique",
               "Vendee", "charente-maritime", "Gironde", "Landes",
               "pays-basque", "golfe-lion", "cote-dazur", "corse"]):
    
    ### Gives all the spots AND the good spots for a given list of region(s)
    ### Input must be a list -> ['Bretagne'] or ['bretagne', 'nord']
    
    best_liste = []
    spot_liste = []
    
    for region in region_liste:
        region_spot_liste = get_spots(region)
        
        for spot in region_spot_liste:
            spot_liste.append(spot)
            good_spot = get_spot_data(spot[3])
            if good_spot:
                #for day in good_spot:
                best_liste.append(good_spot)
    
    for spot in best_liste:
        while len(spot) > 3:
            best_liste.append(spot[0:3])
            del spot[:3]

    spots_df = pd.DataFrame(np.array(spot_liste), columns=['spot', 'ville', 'region', 'url'])
    best_spots_df = pd.DataFrame(best_liste, columns=['url', 'stars', 'date'])
    
    return spots_df, best_spots_df

all_regions = ["Nord", "Manche", "Bretagne", "loire-atlantique",
               "Vendee", "charente-maritime", "Gironde", "Landes",
               "pays-basque", "golfe-lion", "cote-dazur", "corse"]
           
### This last bit calls the last function that makes the Scrapper work. 
france_spot, france_best = region_spots_data(all_regions)
df = france_best.join(france_spot.set_index('url'), on='url')

### sorting the spots by date and stars
df.sort_values(by=["date", "stars"], axis=0, ascending=[True, False])

### Export with today's name as fils name in 'data' folder
today = date.today()
df.to_csv(f'data/{str(today)}.csv', index=False, sep=",")
