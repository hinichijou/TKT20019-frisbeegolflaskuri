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

* Tietokannan rakenteesta: 8 taulua: käyttäjät, radat, kierrokset, tulokset, ilmoittautumiset, luokitteluluokat, luokittelut ja luokittelut radoille. Radan tiedot periaatteessa kopioidaan kierrokseen luomishetkellä koska ratojen layoutit muuttuvat suhteellisen usein, toisaalta ajatuksena on että kierroksen tiedoissa valmista rataa voi muokata niin että esim. custom kierros missä heitetään vain osa väylistä on mahdollinen. Kierroksen ja käyttäjien väillä on relaatio. Kierroksen luojan id tallennetaan kierroksen tietoihin, kierrokselle ilmoittautumiset ovat omassa taulukossaan, joka toimii linkkinä kierroksen ja ilmoittautujien välillä. Luokitteluluokat sisältää kaikki luokittelut joita radoille voi antaa, luokittelut kaikki arvot joita luokitteluilla on, ja luokittelut radoille toimii linkkinä luokittelujen ja ratojen välillä. Jokaisen väylän tulos on tallennettu tulostauluun ja viittaa kierrokseen johon se liittyy, kuin myös pelaajaan, jonka tulos on kyseessä. Tämä tarkoittaa, että kierrokseen liittyvät tulokset poistetaan, jos kierros poistetaan, mikä ei välttämättä olisi tarpeellista, mutta päädyin kuitenkin viittausyhteyteen näiden välillä.

# Sovelluksen käyttöohje:
* Sovellus vaatii toimiakseen [Python](https://www.python.org/downloads/)asennuksen, [SQLite](https://www.sqlite.org/download.html) asennuksen sekä [Flask](https://flask.palletsprojects.com/en/stable/) kirjaston asennuksen.

* Pythonille on suositeltavaa luoda virtuaaliympäristö ajamalla komento (`python -m venv venv` Windowsille, `python3 -m venv venv` Linuxille) projektikansiossa. Virtuaaliympäristö aktivoidaan komennolla (`venv\Scripts\activate.bat` Windowsille, `source venv/bin/activate` Linuxille).

* Sovellus tarvitsee toimiakseen tietokannan, jonka voi luoda ajamalla komennon `sqlite3 database.db < schema.sql` pääkansiossa.

* Komennolla `sqlite3 database.db < init.sql` tietokantaan saa alustettua tarvittavat arvot.

* Komennolla `sqlite3 database.db < indices.sql` tietokantaan voi luoda indeksit, tämä on vapaaehtoista, koska pienillä tietomäärillä testatessa indekseillä ei ole juurikaan merkitystä, mutta määritettyjä indeksejä voi toki halutessaan testata.

* Sovelluksen voi ajaa suorittamalla komennon `flask run` pääkansiossa. Sovellus on tämän jälkeen saatavilla osoitteessa `http://127.0.0.1:5000`

* Klikkaamalla "Luo tunnus" linkkiä pääsee tunnuksenluontinäkymään, jossa pyydetään käyttäjänimi ja salasana.

* Klikkaamalla "Kirjaudu sisään" linkkiä pääsee kirjautumisnäkymään. Syöttämällä tietokannasta löytyvän tunnuksen ja salasanan pääsee käsiksi sovelluksen kirjautuneen käyttäjän toimintoihin.

* Sovelluksen käyttäjä voi pääsivulla kirjautuneena lisätä ratoja, selata ratoja, lisätä kierroksia (kunhan ainakin yksi rata on lisätty ensin) ja etsiä kierroksia radan tai alkamisajan perusteella

* Klikkaamalla "Lisää rata" linkkiä radalle kysytään ensin nimi, väylien lukumäärä, radan vaikeustaso ja radan tyyppi. Klikkaamalla "Seuraava" radan väylille kysytään par ja pituus jotka on mahdollista jättää vakioarvoihin. Klikkaamalla "Lisää rata" rata lisätään tietokantaan.

* Klikkaamalla "Selaa ratoja" pääsee näkymään, joka listaa kaikki lisätyt radat. Klikkaamalla rataa listassa pääsee näkymään, joka listaa radan tiedot. Ratasivulla "Muokkaa" nappia painamalla pääsee radan muokkausnäkymään ja "Poista" nappia painamalla radan poistonäkymään

* Klikkaamalla "Lisää kierros" pääsee näkymään, jossa voi luoda uuden kierroksen. Kierrokselle tarvitsee valita rata, antaa aloitusaika ja valita pelaajien määrä. Kaikki luodut kierrokset näkyvät listassa etusivulla.

* Klikkaamalla "Etsi kierros" pääsee näkymään, jossa etsiä kierroksia radan nimellä tai päivämäärällä. Vakioarvoilla haku listaa kaikki kierrokset.

* Klikkaamalla "Kirjaudu ulos" linkkiä pääsee kirjautumaan ulos sovelluksesta.

* Klikkaamalla kierrosta pääsee kierrosnäkymään joka listaa kierroksen tietoja. Kierroksen lisännyt käyttäjä voi muokata kierrosta tai poistaa kierroksen. Muut käyttäjät pääsevät ilmoittautumaan kierrokselle kyseisessä näkymässä kierrokselle ilmoittautuneiden pelaajien alla olevasta painikkeesta. Kierroksen lisännyt käyttäjä on aina oletuksena myös osallistuja kierroksella. Kierroksen ratatietoja voi muokata vapaasti, sillä ei ole yhteyttä tallennettuihin ratoihin kierroksen luomisen jälkeen.

* Klikkaamalla "Aloita kierros" painiketta kierrosnäkymässä pääsee väylänäkymään, jossa pystyy lisäämään oman tuloksensa kullekkin väylälle. Painikkeen pitäisi olla näkyvillä vain kierrokselle osallistuville pelaajille. Toiminnallisuus oli viime hetken lisäys ennen kolmatta välipalautusta, näkymässä pystyy käytännössä vain lähettämään tuloksia tietokantaan mutta niitä ei vielä näytetä missään. Ajatuksena olisi lisätä väylätulokset sekä väylänäkymään että kierrosnäkymään, mahdollisesti jollain tavalla käyttäjänäkymään ja mahdollisesti myös jonkinlainen kierroksen yhteenvetonäkymä, kun kaikille väylillä on lisännyt tulokset.

* Klikkaamalla käyttäjän nimeä pääsee käyttäjäsivulle, jossa näkee käyttäjien tietoja, kierrokset jotka käyttäjä on lisännyt ja kierrokset, joille käyttäjä on ilmoittautunut.

# Tietoturvatestaus:

* Sovelluksen XSS-aukon käsittelyä voi testata kokeilemalla eri inputteihin (esim. rekisteröintisivu, loginsivu, radan nimi) esimerkiksi syöttettä `<script>alert("HAX");</script>`. Flaskin sivupohjien pitäisi aina escapeta käyttäjäsyötteet, jolloin koodia ei suoriteta selaimessa vaikka se tietokantaan pääsisikin. Tarkoituksena olisi vielä lisätä sallittujen merkkien tarkistus käyttäjäsyötteille, jolloin ongelmaa ei pitäisi edes teoriassa syntyä, mutta en ole tätä vielä toteuttanut.

* Repositorion `tests` kansiosta löytyy tiedosto `csrf_test.html`, jolla voi testata, että csrf-aukko on paikattu. Kun tiedoston avaa selaimessa ja lomakkeen lähettää, se lähettää routeen `/delete_course/1` requestin, jonka ei kuitenkaan pitäisi mennä läpi, koska requestissa ei ole mukana csrf tokenia. Tällä hetkellä testi on kirjoitettu vain kyseiselle routelle, mutta aukko pitäisi olla samaan tapaan paikattu kaikissa post routeissa, jotka vaativat kirjautumista.

# (Vapaaehtoinen) testaus suurella tietomäärällä:
* Halutessaan sovellusta voi testata suurella määrällä dataa luomalla uuden tietokannan komennoilla `sqlite3 mass_test.db < schema.sql` `sqlite3 mass_test.db < init.sql` ja `sqlite3 mass_test.db < indices.sql` ja sen jälkeen ajamalla datan generointiskriptin komennolla `python seed.py` ja vaihtamalla `config.py` tiedoston `database_name` muuttujan arvoksi `constants.mass_test_db_name`. Päätin luoda tietokannat eri nimillä, jotta pystyisin helposti vaihtelemaan erilaisia tietokantoja testaamista varten, nimiä voi toki halutessaan myös koodissa suhteellisen helposti muuttaa.

* `seed.py` luo vakioarvoilla n. 2 gigan kokoisen tietokannan, halutessaan muuttujia `user_count`, `course_count` ja `round_count` muokkaamalla saa generoitua pienemmän tietomäärän jos tämä tuntuu liian suurelta.

* Sovelluksen muokkaaminen soveltuvaksi suurelle tietomäärälle on vielä kesken, osa näkymistä on sivutettu ja osa tarpeellisista indekseistä luotu, mutta ei välttämättä vielä kaikkia. Sovelluksessa on radoille dropdown valikoita, jotka toimivat todella huonosti erittäin suurilla ratamäärillä, mutta tämä on ongelma jota en välttämättä aio korjata, koska sovelluksessa ei ole tarkoitus olla tuhansia ratoja ja pidän dropdowneista käytettävyyden puolesta.

# (Vapaaehtoinen) pylint:
* Halutessaan sovelluksen koodin tyyliä voi arvioida [Pylintillä](https://pylint.readthedocs.io/en/stable/index.html).

* Asenna pylint komennolla `pip install pylint`.

* Komento `pylint *.py` tarkastaa kaikki päähakemistossa olevat Python-tiedostot ja tulostaa niistä raportin komentoriville.

* Repositoriossa on custom pylint tiedosto `pylintrc`, johon on tehty joitain muutoksia vakioasetuksiin. Varoitukset C0114, C0115, C0116, R1705 ja R1710 on disabloitu, jotta raportit näyttäisivät hyödyllisempiä varoituksia, halutessaan asetuksia voi säätää kyseisestä tiedostosta.