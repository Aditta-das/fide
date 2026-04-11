from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
from fastapi.responses import RedirectResponse

app = FastAPI(title="FIDE DATA FETCHER")


@app.get("/")
def home():
    return RedirectResponse(url="/docs")


@app.get("/top_players")
def top_players(limit: int = 100):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        url = "https://ratings.fide.com/a_top.php?list=open"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table_selector = ".top_recors_table"
        table = soup.select_one(table_selector)
        rows: list = table.find_all("tr")
        rows.pop(0)
        top_players = []
        for i, row in enumerate(rows):
            if i+1 <= limit:
                raw_row = []
                for column in row.find_all("td"):
                    raw_data = column.get_text().replace(u'\xa0', '')
                    raw_row.append(raw_data)
                    player_url = column.find("a")
                    if player_url: 
                        raw_row.append(player_url["href"].split("/")[-1])
                top_players.append({
                  "rank": raw_row[0],
                  "name": raw_row[1],
                  "fide_id": raw_row[2],
                  "country": raw_row[3].strip(),
                  "rating": raw_row[4],
                })
        return top_players

    except Exception as e:
        return {
            "error": str(e)
        }

@app.get("/top_women_players")
def top_women_players(limit: int = 100):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        url = "https://ratings.fide.com/a_top.php?list=women"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table_selector = ".top_recors_table"
        table = soup.select_one(table_selector)
        rows: list = table.find_all("tr")
        rows.pop(0)
        top_women_players = []
        for i, row in enumerate(rows):
            if i+1 <= limit:
                raw_row = []
                for column in row.find_all("td"):
                    raw_data = column.get_text().replace(u'\xa0', '')
                    raw_row.append(raw_data)
                    player_url = column.find("a")
                    if player_url: 
                        raw_row.append(player_url["href"].split("/")[-1])
                top_women_players.append({
                  "rank": raw_row[0],
                  "name": raw_row[1],
                  "fide_id": raw_row[2],
                  "country": raw_row[3].strip(),
                  "rating": raw_row[4],
                })
        return top_women_players

    except Exception as e:
        return {
            "error": str(e)
        }



@app.get("/top_country_players")
def top_country_players(limit: int = 100, country: str = "BAN", gender: str = 'M'):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://ratings.fide.com/"
        }        
        url = f"https://ratings.fide.com/a_top_var.php?continent=&country={country}&rating=&gender={gender}&age1=&age2=&period=&period2="
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        rows: list = soup.find_all("tr")
        rows.pop(0)
        top_country_players = []
        for i, row in enumerate(rows):
            if i+1 <= limit:
                raw_row = []
                for column in row.find_all("td"):
                    raw_data = column.get_text().replace(u'\xa0', '')
                    raw_row.append(raw_data)
                    player_url = column.find("a")
                    if player_url: 
                        raw_row.append(player_url["href"].split("/")[-1])
                top_country_players.append({
                  "rank": raw_row[0],
                  "name": raw_row[1],
                  "fide_id": raw_row[2],
                  "country": raw_row[3].strip(),
                  "rating": raw_row[4],
                })
        return top_country_players

    except Exception as e:
        return {
            "error": str(e)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
