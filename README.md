# TKT20019-frisbeegolflaskuri
TKT20019 - Tietokannat ja web-ohjelmointi harjoitustyö

# Sovelluksen kuvaus:
* Sovellukseen pystyy luomaan frisbeegolfratoja, käyttäjät voivat pelata näillä radoilla kierroksia.

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjät pystyvät lisäämään, muokkaamaan ja poistamaan sovellukseen lisättyjä ratoja. Radoilla on x määrä väyliä, jokaiselle väylälle määritetään pituus metreinä ja par. Kaikkien lisäämät radat on kaikkien muokattavissa ja poistettavissa, ajatuksena on käyttäjille yhteinen ratojen tietokanta.

* Käyttäjä voi lisätä sovellukseen kierroksen ja muokkaamaan ja poistamaan itse lisäämiään kierroksia. Kierrokselle voi määrittää ajan, sijainnin ja pelaajien maksimimäärän.

* Käyttäjä näkee sovellukseen lisätyt kierrokset.

* Käyttäjä pystyy etsimään kierroksia radan perusteella. Kierrokset listataan niin että ajallisesti lähin näytetään ensimmäisenä.

* Käyttäjäsivu näyttää käyttäjän lisäämät kierrokset ja montako kierrosta käyttäjä on lisännyt.

* Radoille voi lisätä luokitteluja, tämä tuntuu tämän sovelluksen kohdalla luontevammalta luokittelun kohteelta kuin kierros, joka olisi suorempi vastine sulkapallosovelluksen ilmoitukselle. Esimerkiksi "helppo", "haastava", "vaikea", "avoimia väyliä", "metsää", "puistoa", "korkeuseroja" jne.

* Käyttäjä voi ilmoittautua kierrokselle. Käyttäjä näkee kierroksen tiedot ja ketkä muut pelaajat ovat ilmoittautuneet. Käyttäjä voi muokata ilmoittautumistaan, toisin sanoen perua ilmoittautumisensa kierrokselle.

* Kierrokselle osallistujat voivat merkitä kierrosnäkymässä kierroksen aikana väyläkohtaisia tuloksia. Sovellus näyttää kaikille käyttäjille väyläkohtaiset tulokset ja kierroksen kokonaistuloksen.

* Sovellus vastaa suunnilleen esimerkkisovellusta sulkapalloseura ollen hieman monimutkaisempi. Sovellus nähdäkseni täyttää tällä kuvauksella kaikki perusvaatimukset, mutta lisää yhden tietokohdetason (rata -> kierros -> ilmoittautuminen). Toinen lisäys on kierroksen aikainen tulosseuranta, jonka näkisin suunnilleen vastaavan sitä, jos sulkapallosovelluksessa olisi jonkunlainen tulostenmerkintämahdollisuus. Motivaationa tälle suunnitelmalle oli saada aikaan jotain mitä pystyisin toivottavasti kokeilemaan käytännössä.

* Tietokannan rakenteesta: 7 taulua: käyttäjät, radat, kierrokset, ilmoittautumiset, luokitteluluokat, luokittelut ja luokittelut radoille. Radan tiedot periaatteessa kopioidaan kierrokseen luomishetkellä koska ratojen layoutit muuttuvat suhteellisen usein, toisaalta ajatuksena on että kierroksen tiedoissa valmista rataa voi muokata niin että esim. custom kierros missä heitetään vain osa väylistä on mahdollinen. Kierroksen ja käyttäjien väillä on relaatio. Kierroksen luojan id tallennetaan kierroksen tietoihin, kierrokselle ilmoittautumiset ovat omassa taulukossaan, joka toimii linkkinä kierroksen ja ilmoittautujien välillä. Luokitteluluokat sisältää kaikki luokittelut joita radoille voi antaa, luokittelut kaikki arvot joita luokitteluilla on, ja luokittelut radoille toimii linkkinä luokittelujen ja ratojen välillä.

# Sovelluksen käyttöohje:
* Sovellus vaatii toimiakseen [SQLite](https://www.sqlite.org/download.html) asennuksen sekä [Flask](https://flask.palletsprojects.com/en/stable/) kirjaston asennuksen.

* Sovellus tarvitsee toimiakseen tietokannan, jonka voi luoda ajamalla komennon `sqlite3 database.db < schema.sql` pääkansiossa.

* Komennolla `sqlite3 database.db < init.sql` tietokantaan saa alustettua tarvittavat arvot.

* Sovelluksen voi ajaa suorittamalla komennon `flask run` pääkansiossa. Sovellus on tämän jälkeen saatavilla osoitteessa `http://127.0.0.1:5000`

* Klikkaamalla "Luo tunnus" linkkiä pääsee tunnuksenluontinäkymään, jossa pyydetään käyttäjänimi ja salasana.

* Klikkaamalla "Kirjaudu sisään" linkkiä pääsee kirjautumisnäkymään. Syöttämällä tietokannasta löytyvän tunnuksen ja salasanan pääsee käsiksi sovelluksen kirjautuneen käyttäjän toimintoihin.

* Sovelluksen käyttäjä voi pääsivulla kirjautuneena lisätä ratoja, selata ratoja, lisätä kierroksia (kunhan ainakin yksi rata on lisätty ensin) ja etsiä kierroksia radan tai alkamisajan perusteella

* Klikkaamalla "Lisää rata" linkkiä radalle kysytään ensin nimi, väylien lukumäärä, radan vaikeustaso ja radan tyyppi. Klikkaamalla "Seuraava" radan väylille kysytään par ja pituus jotka on mahdollista jättää vakioarvoihin. Klikkaamalla "Lisää rata" rata lisätään tietokantaan.

* Klikkaamalla "Selaa ratoja" pääsee näkymään, joka listaa kaikki lisätyt radat. Klikkaamalla rataa listassa pääsee näkymään, joka listaa radan tiedot. Ratasivulla "Muokkaa" nappia painamalla pääsee radan muokkausnäkymään ja "Poista" nappia painamalla radan poistonäkymään

* Klikkaamalla "Lisää kierros" pääsee näkymään, jossa voi luoda uuden kierroksen. Kierrokselle tarvitsee valita rata, antaa aloitusaika ja valita pelaajien määrä. Kaikki luodut kierrokset näkyvät listassa etusivulla.

* Klikkaamalla "Etsi kierros" pääsee näkymään, jossa etsiä kierroksia radan nimellä tai päivämäärällä. Vakioarvoilla haku listaa kaikki kierrokset.

* Klikkaamalla "Kirjaudu ulos" linkkiä pääsee kirjautumaan ulos sovelluksesta.

* Klikkaamalla kierrosta pääsee kierrosnäkymään joka listaa kierroksen tietoja. Kierroksen lisännyt käyttäjä voi muokata kierrosta tai poistaa kierroksen. Muut käyttäjät pääsevät ilmoittautumaan kierrokselle kyseisessä näkymässä sivun alaosan painikkeesta. Kierroksen lisännyt käyttäjä on aina oletuksena myös osallistuja kierroksella. Kierroksen ratatietoja voi muokata vapaasti, sillä ei ole yhteyttä tallennettuihin ratoihin kierroksen luomisen jälkeen.

* Klikkaamalla käyttäjän nimeä pääsee käyttäjäsivulle, jossa näkee käyttäjien tietoja, kierrokset jotka käyttäjä on lisännyt ja kierrokset, joilla käyttäjä on ilmoittautunut.