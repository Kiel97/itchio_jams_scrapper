import argparse
from datetime import datetime

from bs4 import BeautifulSoup
import requests

URL = "https://itch.io/jams"

def main():
    parser = argparse.ArgumentParser("Get all jams available on itch.io")
    parser.add_argument('--html', help="Print website's prettified html only", action='store_true')
    parser.add_argument('--no-links', help="Don't save link to game jam's page", action='store_true')
    parser.add_argument('--no-count', help="Don't save joined count value", action='store_true')
    args = parser.parse_args()

    html = requests.get(URL)

    soup = BeautifulSoup(html.text, "html.parser")

    if args.html:
        with open("html_"+str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+".txt", 'w') as f:
            f.write(soup.prettify())
            return

    jams = []
    jam_cells = soup.find_all("div", {"class": "jam_cell"})
    
    for jam in jam_cells:
        info = jam.text.rstrip(")").rsplit("(", 1)
        
        if args.no_count:
            info = [info[0]]
            
        if not args.no_links:
            for anchor in jam.find_all('a'):
                info.append("https://itch.io" + anchor['href'])
                
        jams.append(info)

    #jams.sort(key=lambda x: int(x[1].split()[0].replace(',','')))

    with open("jams_"+str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+".txt", 'w') as f:
        for jam in jams:
            f.write(" - ".join(jam)+"\n")

if __name__ == "__main__":
    main()