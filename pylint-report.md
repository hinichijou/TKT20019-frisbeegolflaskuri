# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0302: Too many lines in module (1229/1000) (too-many-lines)
app.py:861:4: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
************* Module m_rounds
m_rounds.py:108:0: R0911: Too many return statements (8/6) (too-many-return-statements)

------------------------------------------------------------------
Your code has been rated at 9.97/10 (previous run: 9.97/10, +0.01)
```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

## Liikaa rivejä moduulissa

Raportissa on seuraava ilmoitus liittyen moduulin rivien määrään:

```
app.py:1:0: C0302: Too many lines in module (1229/1000) (too-many-lines)
```

C0302 ilmoitus annetaan, jos moduulissa on yli 1000 riviä koodia, perusteena se, että liian suuri rivimäärä heikentää luettavauutta ja IDE:n suorituskykyä. Vaikka tämä pitää varmasti paikkaansa, on 1000 rivin rajooitus loppupeleissä mielivaltainen, enkä näe suurta eroa siinä onko moduulissa 1000 vai 1229 riviä koodia, joten jätän ilmoituksen huomiotta. Koodia voisi varmasti jakaa edelleen useampaan moduuliin, mutta pidän nykyistä jakoa jokseenkin perusteltavana tämän projektin tarpeisiin, eniten liipaisimella olisi syötteiden tarkistukseen liittyvä koodi, jonka voisi melko luontevasti jakaa omaan moduuliinsa.

## Enumeraten käyttö sen sijaan, että iteroi rangen len:in pohjalta

Raportissa on seuraava ilmoitus liittyen listan iterointiin:

```
app.py:861:4: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
```

C0200 ilmoitus annetaan, koska iteroin listan sen pituuden pohjalta ja viittaan arvoihin indeksin perusteella, sen sijaan, että käyttäisin enumeratea, joka palauttaa indeksin ja arvon indeksin kohdassa suoraan. Päätin tehdä näin koska etsin listasta poistettavaa indeksiä, jonka jälkeen break:aan ulos for-ehtolausekkeesta. Mielestäni, jos listasta poistaa jotain on miellyttävämpää olla iteroimatta listaa samalla, yleensä käyttäisin enumeratea listan iteroimiseen. Parempi olisi tietysti aina olla poistamatta listasta iteroitaessa, mutta tässä tapauksessa en näe siitä haittaakaan.

## Liian monta returnia

Raportissa on seuraava ilmoitus liittyen liian suureen returnien määrään funktiossa:

```
m_rounds.py:108:0: R0911: Too many return statements (8/6) (too-many-return-statements)
```

R0911 annetaan, jos yhdessä funktiossa on yli 6 returnia. Kyseinen funktio sisältää suhteellisen siistin match case -rakenteen, joten ilmoitus on mielestäni täysin turha. Vastaavissa tilanteissa voisi toki käyttää esim. dictionarya tai jotain vastaavaa, mutta ratkaisun paremmuus on mielestäni puhdas makuasia.

## pylintrc konfiguraation selitys

Projektissa on pylintrc tiedosto, johon on tehty muutoksia, jotta pylint antaisi hyödyllisempiä raportteja, sen sijaan, että mahdollisesti hyödyllisiä ilmoituksia joutuisi etsimään ilmoitusten seasta, joita ei ole aikeissa korjata. Seuraavassa selitys konfiguraatioon tehdyistä muutoksista.

Seuraava muutos asettaa luokkamuuttujille custom regex:in, joka sallii snake_case ja UPPER_CASE muuttujat.

```
class-const-rgx=[a-z]+(?:_[a-z]+)*|[A-Z]+(?:_[A-Z]+)*
```

Tein muutoksen siksi, että halusin käyttää UPPER_CASE muuttujanimiä enumeille ja muille snake_case tyyliä. Syynä se, että pidän tätä selkeänä, eikä pylintin tyyliohjeet ole mitään kiveen hakattuja tauluja, joita tulisi noudattaa. Pidän kuitenkin varoitusta ihan hyödyllisenä, tällä ratkaisulla esimerkiksi camelCase-muuttujista saa varoituksen.

Seuraava muutos asettaa vakioiden tyyliksi snake_case, vakiona olevan UPPER_CASE:n sijaan.

```
const-naming-style=snake_case
```

Syynä muutokseen puhtaasti se, että olen tämän tyyliseen nimeämiseen tottunut. Mielestäni kyseessä on jälleen mielipideasia, tärkeämpää on mielestäni projektin sisäinen yhtenäisyys, kuin se mikä tyyli tarkalleen on, tästä syystä muutujat varmasti ovatkin konfiguroitavissa.

Seuraava muutos asettaa rivin maksimipituudeksi 120 vakiona olevan 100 sijaan.

```
max-line-length=120
```

Rivin maksimipituudet ovat puhtaasti mielipideasioita, ja mielestäni käy järkeen käyttää ruututilaa jos sitä on käytettävissä. Vakio 100 on hyvin kapeille ikkunoille, 120:kin on mielestäni vielä tiivis. line-length on mielestäni hyödyllinen ilmoitus, mutta tarkka rivipituus on mielipidekysymys, kunhan projektin sisällä tyyli on yhtenäinen.

Seuraavassa lisätään disabloituihin ilmoituksiin ilmoitukset koodeilla: C0114, C0115, C0116, R1705 ja R1710

```
disable=raw-checker-failed,
        ...
# Disable missing docstring warning as they aren't required
        C0114,
        C0115,
        C0116,
# Disable no-else-return. Style follows the example videos and readability is up to preference
        R1705,
# Disable inconsistent-return-statements. Style follows the example videos and readability is up to preference. The warning
# is caused by a situation where we now the method has to be GET or POST and a None return would be redundant.
        R1710
```

Yllä olevat kommentit jo jossain määrin selittävät disabloinnin syitä. Alla syitä avattu kuitenkin hieman tarkemmin.

Ilmoitukset C0114, C0115 ja C0116 ovat docstring-ilmoituksia. Nämä ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja. Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja.

R1705 on if-else rakenteisiin liittyvä ilmoitus. Ilmoitus ilmaisee että tilanteet, kuten:

```python
if ehto:
    return a
else:
    return b
```

olisi tyylikkäämpää kirjoittaa muodossa:

```python
if ehto:
    return a

return b
```

Kyseessä on kuitenkin loppupeleissä makuasia, ja intention esittäminen koodissa on mielestäni tärkeää. Mielestäni ensimmäisen vaihtoehdon lukee niin, että on olemassa kaksi samanarvoista polkua, joista toiseen päädytään, kun taas jälkimmäinen näyttää siltä, että on "peruspolku" return b, josta saatetaan poiketa jos ehto täyttyy. Mielestäni molemmat ovat täysin hyväksyttäviä tyylejä ja koodaaja voi itse päättää kumpi on tilanteeseen selkeämpi ja paremmin tarkoitusta ilmaiseva.

R1710 on funktion palautusarvoihin liittyvä ilmoitus. Ilmoitus annetaan tilanteissa kuten:

```python
@app.route("/route", methods=["GET", "POST"])
def do_things():
    if request.method == "GET":
        return a

    if request.method == "POST":
        return b
```

sen sijaan, että palautusarvo määritettäisiin myös tilanteelle, jossa "GET" tai "POST" ei toteudu:

```python
@app.route("/route", methods=["GET", "POST"])
def do_things():
    if request.method == "GET":
        return a

    if request.method == "POST":
        return b

    return c
```

Applikaation routeissa käytännössä tällainen tilanne ei ole kuitenkaan mahdollinen, koska funktion dekoraattorissa on vaatimus, että metodin tulee olla `GET` tai `POST`. Niinpä tässä tapauksessa ei ole riskiä, että funktio ei jossain tilanteessa palauttaisi arvoa. Olen disabloinut ilmoituksen, koska se tulee jatkuvasti applikaation routeista, mutta se on kuitenkin periaatteessa hyödyllinen muissa paikoissa, joten ajan pylintin ajoittain myös ilman virheen disablointia.
