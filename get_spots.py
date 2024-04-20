import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import csv

today = date.today()

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



all_regions = ["Nord", "Manche", "Bretagne", "loire-atlantique", "Vendee", "charente-maritime", "Gironde", "Landes", "pays-basque", "golfe-lion", "cote-dazur", "corse"]



all_spots = [] 
for region in all_regions :
    all_spots.append(get_spots(region))

headers = ["spot", "ville", "region", "url"]
 
with open('spots.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    # Flatten only one level
    for sublist in all_spots:
        for item in sublist:
            writer.writerow(item)
