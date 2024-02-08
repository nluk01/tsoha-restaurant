# Ravintolasovellus

Projektin tarkoituksena on kehittää ravintolasovellus, joka näyttää tietyn alueen ravintolat.

## Käyttäjäroolit

- **Peruskäyttäjä:** Tavallinen käyttäjä, joka voi rekisteröityä, kirjautua sisään ja ulos.

- **Ylläpitäjä:** Sovelluksen ylläpitäjä, joka voi lisätä ja poistaa ravintoloita, muokata ravintoloiden tietoja ja hallita käyttäjien antamia arvioita.

## Toiminnot

- Käyttäjä voi rekisteröityä ja kirjautua sisään ja ulos.
- Käyttäjä voi hakea ravintoloita tietyn sanan perusteella niiden kuvauksista.
- Peruskäyttäjä voi lukea ravintolan arvioita, ja antaa itse arvioita ravintoloille tekstikommenttien tai 1-5 numeroskaalan avulla.
- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä muokata ravintoloiden tietoja.
- Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voidaan luokitella.
- Ravintola voi kuulua yhteen tai useampaan ryhmään, ja ylläpitäjä voi määrittää tämän.
- Ylläpitäjä voi määrittää, mitä tietoja ravintolasta näytetään.

### Sovelluksen testaus

Sovellusta voi testata:
1. Kloonaa tämän sovelluksen repositorio koneellesi ja mene juurikansioon

2. Luo .env-tiedosto ja lisää sinne:
- DATABASE_URL=postgresql:///thlu
- SECRET_KEY="kirjoita joku numerosarja"

3. Aktivoi virtuaaliympäristö terminaalissa komennoilla:
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

4. Määritä tietokannan taulukot terminaalissa komennoilla:
- psql< tables.sql

5. Käynnistä sovelluks komennolla flask run

## Tekemättä olevat toiminnot

- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa käyttäjän syöttämä sana.
- Ylläpitäjä voi määrittää mitä kaikkia tietoja ravintolasta näytetään.
- Ylläpitäjä voi poistaa käyttäjän antaman arvion.

