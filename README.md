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
* Sovellus tarvitsee toimiakseen tietokannan, jonka voi luoda ajamalla komennon `sqlite3 database.db < schema.sql` pääkansiossa.

* Komennolla `sqlite3 database.db < init.sql` tietokantaan saa alustettua tarvittavat arvot.

* Sovelluksen voi ajaa suorittamalla komennon `flask run` pääkansiossa. Sovellus on tämän jälkeen saatavilla osoitteessa `http://127.0.0.1:5000`

* Klikkaamalla "Luo tunnus" linkkiä pääset tunnuksenluontinäkymään, jossa pyydetään käyttäjänimi ja salasana.

* Klikkaamalla "Kirjaudu sisään" linkkiä pääset kirjautumisnäkymään. Syöttämällä tietokannasta löytyvän tunnuksen ja salasanan pääset käsiksi sovelluksen kirjautuneen käyttäjän toimintoihin.

* Sovelluksen käyttäjä voi pääsivulla kirjautuneena lisätä ratoja, selata ratoja, lisätä kierroksia (kunhan ainakin yksi rata on lisätty ensin) ja etsiä kierroksia radan tai alkamisajan perusteella