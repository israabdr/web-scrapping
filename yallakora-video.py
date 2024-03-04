import requests
from bs4 import BeautifulSoup
import csv 

date = input("Please enter a Date in the following format MM/DD/YYYY:")
page = requests.get(f"https://www.yallakora.com/match-center?date={date}")

def main (page):
    src= page.content 
    soup = BeautifulSoup(src, "lxml")
    matches_list = []

    championship = soup.find_all ("div" , {'class' : 'matchCard'})

    def get_match_info(championship):
        championship_title = championship.contents[1].find('h2').text.strip()
        all_matches = championship.contents[3].find_all('li')
        nubmer_of_matches = len(all_matches)
        for i in range (nubmer_of_matches):
            #get teams names
            team_A = all_matches[i].find('div', {'class': 'teamA'}).text.strip()
            team_B = all_matches[i].find('div', {'class': 'teamB'}).text.strip()

            #get score
            match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            #get match time 
            match_time = all_matches[i].find('div', {'class': 'MResult'}).find('span',{'class': 'time'}).text.strip()

            # add match info to matches_details

            matches_list.append({"championnat": championship_title, "premiere_equipe":team_A,"deuxieme_equipe":team_B, "heure_match":match_time, "result0:score":score})
        
        for i in range (len(championship)):
    
            get_match_info(championship[i])
        
        keys = matches_list[0].keys()
        with open('wcraping.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_list)



main(page)