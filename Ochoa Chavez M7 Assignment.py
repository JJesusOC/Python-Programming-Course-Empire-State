'''
This program retrieves Premier League soccer matches using a public API.
Parses JSON data returned by the API and displays a list of randomized matches with
the name of the teams (whos home and away), the score, and date. 
Originally I wanted to do recent matches, but the given the limitations of the API and current 
break, it returned no matches.
'''

import requests
import random

# API endopoint where we get Premier League matches from the 2024/2025 season
URL = "https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id=4328&s=2024-2025"


# Gets matches from the 24/25 season from TheSportsDB API
# Handles randomization of results and displays details. 
def get_matches():
    matches = []

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        matches = data.get("events", [])
    # Handles errors
    except requests.exceptions.RequestException as e:
        print("ConnectionError!")
        print("Reason:", e)
        return


    # This tells us if there is no match data from API
    if not matches:
        print("No past soccer matches available.")
        return

    print("Past Premier League Matches")
    print("---------------------------")

    # Allows for the results to be randomized
    random.shuffle(matches)

    for match in matches[:10]:

        # This is in place if there is missing data from API
        league = match.get("strLeague", "League not listed")
        home = match.get("strHomeTeam", "Home team unavailable")
        away = match.get("strAwayTeam", "Away team unavailable")
        date = match.get("dateEvent", "Date not provided")
        home_score = match.get("intHomeScore")
        away_score = match.get("intAwayScore")

        # If the data is available, this displays the values
        score = (
            f"{home_score} - {away_score}"
            if home_score is not None and away_score is not None
            else "Score not available")
        print(f"\nLeague: {league}")
        print(f"Match: {home} vs {away}")
        print(f"Date: {date}")
        print(f"Final Score: {score}")


if __name__ == "__main__":
    get_matches()

