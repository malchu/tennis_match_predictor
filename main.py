import re
import tkinter as tk
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# -------------------------- GUI --------------------------- #
from termcolor import colored

root = tk.Tk()
root.title('Tennis Match Predictor')

canvas1 = tk.Canvas(root, width=700, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Tennis Match Predictor')
label1.config(font=('helvetica', 20))
canvas1.create_window(350, 40, window=label1)

label2 = tk.Label(root, text='Player One:')
label2.config(font=('helvetica', 10))
canvas1.create_window(150, 100, window=label2)

label5 = tk.Label(root, text='Player Two:')
label5.config(font=('helvetica', 10))
canvas1.create_window(550, 100, window=label5)

label3 = tk.Label(root, text='', font=('helvetica', 12))

entry1 = tk.Entry(root)
canvas1.create_window(150, 140, window=entry1)
entry2 = tk.Entry(root)
canvas1.create_window(550, 140, window=entry2)


def getPrediction():

    player_one = entry1.get()
    player_two = entry2.get()

    one = player_one.split()
    two = player_two.split()
    one_code = two_code = age1 = rank1 = points1 = age2 = rank2 = points2 = 0

    html_text = requests.get('https://www.atptour.com/en/rankings/singles').text
    soup = BeautifulSoup(html_text, 'lxml')
    players = soup.find_all('tr', class_ = '')
    for player in players:
        rank = player.find('td', class_ = 'rank-cell border-left-4 border-right-dash-1').text.replace(' ','').strip()
        points = player.find('td', class_ = 'points-cell border-right-dash-1').text.replace(' ','').replace(',','').strip()
        age = player.find('td', class_ = 'age-cell border-left-dash-1 border-right-4').text.replace(' ','').strip()
        name = re.sub(r"(\w)([A-Z])", r"\1 \2", player.find('span', class_ = 'player-cell-wrapper').text.replace(' ','').strip())
        profile = player.find('span', class_ = 'player-cell-wrapper').a['href'].split('/')

        if player_one in name:
            one_code = profile[4]
            age1, rank1, points1 = age, rank, points
        if player_two in name:
            two_code = profile[4]
            age2, rank2, points2 = age, rank, points
        if one_code != 0 and two_code != 0:
            break

    url = "https://www.atptour.com/en/players/atp-head-2-head/" + one[0] + "-" + one[1] + "-vs-" + two[0] + "-" + two[1] + "/" + one_code + "/" + two_code
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    h2h = soup.find('table', class_ = 'h2h-table h2h-table-ytd').text.split()
    events = soup.find('table', class_ = "modal-event-breakdown-table").text.split()

    wins1 = soup.find('div', class_ = 'player-left-wins').find('div', class_ = "players-head-rank").text.strip()
    wins2 = soup.find('div', class_ = 'player-right-wins').find('div', class_ = "players-head-rank").text.strip()
    plays1, plays2 = h2h[24], h2h[26]
    backhand1, backhand2 = h2h[27], h2h[29]
    ytd_wl1, ytd_wl2 = h2h[34].split('/'), h2h[37].split('/')
    ytd_titles1, ytd_titles2 = h2h[38], h2h[41]
    wl1, wl2 = h2h[42].split('/'), h2h[45].split('/')
    career_titles1, career_titles2 = h2h[46], h2h[49]

    win_value1 = int(points1) + (int(wins1))*8000 + (int(ytd_titles1))*70 + (int(career_titles1))*50 + (int(ytd_wl1[0]))*1000 - (int(age1))*10 - (int(rank1)*50)
    win_value2 = int(points2) + (int(wins2))*8000 + (int(ytd_titles2))*70 + (int(career_titles2))*50 + (int(ytd_wl2[0]))*1000 - (int(age2))*10 - (int(rank2)*50)
    total = win_value1 + win_value2
    win_pct = win_value1 / total
    if win_pct < .50:
        print(f"Malchu predicts {player_two} wins with a {int((1-win_pct)*100)}% chance.")
    else:
        print(f"Malchu predicts {player_one} wins with a {int(win_pct*100)}% chance.")

    if win_pct < .50:
        label3.config(text='Malchu predicts ' + player_two + ' will win with a ' + str(int((1-win_pct)*100)) + '% ' + 'chance!')
    else:
        label3.config(text='Malchu predicts ' + player_one + ' will win with a ' + str(int(win_pct*100)) + '% ' + 'chance!')
    canvas1.create_window(350, 240, window=label3)


button1 = tk.Button(text='Predict!', command=getPrediction, bg='blue', fg='white',
                    font=('helvetica', 14, 'bold'))
canvas1.create_window(350, 180, window=button1)

root.mainloop()