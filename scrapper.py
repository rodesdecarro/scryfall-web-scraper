import requests
import datetime
import csv
from bs4 import BeautifulSoup
from time import sleep

print("Starting Scryfall web scrapper...")

# Get current time
now = datetime.datetime.now()

# Define the header of our file
header = [
    "set_abbreviation",
    "set_card_count",
    "set_release_date",
    "card_number",
    "card_name",
    "card_mana_cost",
    "card_type",
    "card_rarity",
    "card_artist",
    "card_price_usd",
    "card_price_eur",
    "card_price_tix",
]

# Create a new csv file
filePath = f'mtg-price-set.csv'
print(f"Creating {filePath} file...")
with open(filePath, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

# First, get all the available sets
print(f"Fetching https://scryfall.com/sets...")
sets_page = requests.get("https://scryfall.com/sets")
sets_soup = BeautifulSoup(sets_page.content, features="html.parser")

# Get the table with the sets and select all the rows
sets_tr = sets_soup.find("table", {"id": "js-checklist"}).tbody.find_all("tr")
print(f"{len(sets_tr)} sets retieved.")

# Build a list with all the sets
sets = []

for set_tr in sets_tr:
    # Get all the columns from the row
    set_td = set_tr.find_all("td")
    # First column has the abbreviation of the set and the href of the set
    set_abbreviation = set_td[0].small.text
    set_link = set_td[0].a["href"]
    # Second column has the number of cards in the set
    set_card_count = set_td[1].a.text
    # Third column has the release date of the set
    set_release_date = set_td[2].a.text
    # Last column contains the languages in which the set has been released
    set_language = set_td[3].span.a.text if set_td[3].span and set_td[3].span.a else ""
    # Filter out not published sets, sets with less than 100 cards and sets not in english
    if (
        now > datetime.datetime.strptime(set_release_date, "%Y-%m-%d")
        and int(set_card_count) >= 100
        and set_language == "en"
    ):
        sets.append(
            {
                "abbreviation": set_abbreviation,
                "link": set_link,
                "card_count": set_card_count,
                "release_date": set_release_date,
            }
        )


set_counter = 0
set_count = len(sets)
print(f"{set_count} sets filtered.")

# For each set...
for set in sets:
    # Before requesting the website, add a 100 ms delay
    sleep(0.1)
    # Request the list of cards from the set
    set_counter = set_counter + 1
    print(f'({set_counter}/{set_count}) Fetching {set["link"]}...')
    set_page = requests.get(set["link"] + "?as=checklist")
    set_soup = BeautifulSoup(set_page.content, features="html.parser")

    # Get the table with the cards and select all the rows
    cards_tr = set_soup.find("table", {"id": "js-checklist"}).tbody.find_all("tr")
    print(f"{len(cards_tr)} cards retrieved.")

    # Build a list with the cards for the set
    cards = []

    for card_tr in cards_tr:
        # Get all the columns from the row
        card_td = card_tr.find_all("td")
        # First column is the set
        # card_set_abbreviation = card_td[0].a.abbr.text
        # Second column contains the number of the card in the set
        card_number = card_td[1].a.text if card_td[1].a else ""
        # Third column contains the name of the card
        card_name = card_td[2].a.text if card_td[2].a else ""
        # Fourth column contains the mana cost
        card_mana_cost = str.strip(card_td[3].a.text) if card_td[3].a else ""
        # Fifth column contains the type of card
        card_type = str.strip(card_td[4].a.text) if card_td[4].a else ""
        # Sixth, we get the rarity
        card_rarity = card_td[5].a.abbr.text if card_td[5].a else ""
        # Seventh column contains the language
        # card_language = card_td[6].a.abbr.textif card_td[6].a else ""
        # Next, we have the artist of the card
        card_artist = card_td[7].a.text if card_td[7].a else ""
        # Last three columns have the price, en USD, EUR and TIX
        card_price_usd = card_td[8].a.text if card_td[8].a else ""
        card_price_eur = card_td[9].a.text if card_td[9].a else ""
        card_price_tix = card_td[10].a.text if card_td[10].a else ""
        # Add the card into the list
        cards.append(
            {
                "number": card_number,
                "name": card_name,
                "mana_cost": card_mana_cost,
                "type": card_type,
                "rarity": card_rarity,
                "artist": card_artist,
                "price_usd": card_price_usd,
                "price_eur": card_price_eur,
                "price_tix": card_price_tix,
            }
        )

    # Write the cards from the set in the output file
    with open(filePath, "a", newline="", encoding="utf-8") as f:
        for card in cards:
            writer = csv.writer(f)
            writer.writerow(
                [
                    set["abbreviation"],
                    set["card_count"],
                    set["release_date"],
                    card["number"],
                    card["name"],
                    card["mana_cost"],
                    card["type"],
                    card["rarity"],
                    card["artist"],
                    card["price_usd"],
                    card["price_eur"],
                    card["price_tix"],
                ]
            )

print("Done!")