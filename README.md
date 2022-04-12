# scryfall-web-scraper
Scraper de la web https://scryfall.com/ per l'assignatura de Tipologia i cicle de vida de les dades de la UOC.

Per executar el codi, és necessari instal·lar les següents llibreries:
```
pip install beautifulsoup4
pip install requests
```

L'execució de l'script no necessita de cap paràmetre i es pot cridar així:
```
python scrapper.py
```

L'script recull el llistat de cartes de totes les col·leccions disponibles a https://scryfall.com/sets, que compleixen les següents condicions:
- La data de publicació de la col·lecció no és a futur.
- La col·lecció ha estat publicada en anglès.
- La col·lecció té 100 cartes o més.

El fitxer generat és un csv amb els següents camps:
- set_abbreviation: Identificador de la col·lecció on es troba la carta.
- set_card_count: Nombre de cartes en la col·lecció.
- set_release_date: Data de publicació de la col·lecció.
- card_number: Nombre de la carta dins de la col·lecció.
- card_name: Nom de la carta.
- card_mana_cost: Cost de jugar de la carta, en la notació tradicional de MTG.
- card_type: Tipus de carta.
- card_rarity: Raresa de la carta.
- card_artist: Dibuixant de la carta.
- card_price_usd: Preu en USD de la carta, segons TCGPlayer.
- card_price_eur: Preu en EUR de la carta, segons Cardmarket.
- card_price_tix: Preu en TIX de la carta, segons Cardhoarder.
