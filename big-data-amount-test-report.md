# Raportti testauksesta suurella tietomäärällä

* Sovellusta voi testata suurella määrällä dataa luomalla uuden tietokannan komennoilla `sqlite3 mass_test.db < schema.sql` ja `sqlite3 mass_test.db < init.sql` ja sen jälkeen ajamalla datan generointiskriptin komennolla `python seed.py` ja vaihtamalla `config.py` tiedoston `database_name` muuttujan arvoksi `constants.mass_test_db_name`.

* Sovellus testattiin `seed.py`:n arvoilla: `user_count = 1000`, `course_count = 10**5` ja `rounds_count = 10**6`.

* Sovellukseen lisättiin sivutus kutsuihin `m_courses.get_courses`, `m_courses.find_courses`, `m_rounds.get_rounds`, `m_rounds.find_rounds` ja `m_rounds.find_participating_rounds`. Koska ratoja ja kierroksia voi olla sovelluksessa periaatteessa rajaton määrä, oli niitä listaavat kutsut käytännössä pakko sivuttaa ettei sovelluksesta tule käyttökelvotonta sekä UI:n että suorituskyvyn puolesta.

## Suuri datamäärä ilman indeksointia

* Testitietokannan koko vakioarvoilla luotuna on n. 2.6GB.

* Ensimmäiset haut tietokannan luomisen jälkeen kestivät ajoittain huomattavasti pidempään kuin sen jälkeiset, oletettavasti tällä on jotain tekemistä cachetuksen kanssa. En erikseen ilmoita näiden hakujen kestoja, vaan jätän asian yleisen huomion tasolle.

* Etusivun (tekee haut `m_rounds.round_count` ja `m_rounds.get_all_rounds` kierrosten näyttämistä varten) avaus kesti n. 2.1 sekuntia.

* "Etsi ratoja" sivun (tekee haut `m_courses.courses_count` ja `m_courses.get_courses` ratojen näyttämiseksi `datalist` `input`:ssa) avaus kesti n. 0.38 sekuntia. Ratahaun (tekee kaksi hakua, toisessa haetaan sivutetusti hakuparametrit täyttäviä ratoja `m_courses.courses_count` ja `m_courses.find_courses` hauilla, toisessa yllä olevalla tavalla radat input kenttää varten) kesto riippuu hakuparametreista, oletusparametreilla (palauttaa kaikki testiradat) haku kesti n. 0.4 sekuntia, radan nimellä hakeminen syötteellä "course" (palauttaa kaikki testiradat) kesti n. 0.43 sekuntia, väylien lukumäärällä hakeminen syötteellä "18" n. 0.47 sekuntia ja radan tyypillä tai vaikeudella hakeminen n. 0.52 sekuntia.

* "Etsi kierros" sivun (tekee haut `m_courses.courses_count` ja `m_courses.get_courses` ratojen näyttämiseksi `datalist` `input`:ssa) avaus kesti n. 0.38 sekuntia. Kierroshaun (tekee kaksi hakua, toisessa haetaan sivutetusti hakuparametrit täyttäviä kierroksia `m_rounds.round_count` ja `m_rounds.find_rounds` hauilla, toisessa yllä olevalla tavalla radat input kenttää varten) kesto riippuu hakuparametreista, oletusparametreilla  (palauttaa kaikki kierrokset) haku kesti n. 2.7 sekuntia, radan nimellä hakeminen syötteellä "course" (palauttaa kaikki kierrokset) kesti n. 2.9 sekuntia, päivämäärällä hakeminen (saman päivän päivämäärä) n. 2.2 sekuntia ja kierroksen luojan nimellä hakeminen syötteellä "user" (palauttaa kaikki kierrokset) n. 3 sekuntia.

* "Lisää kierros" sivun (tekee haut `m_courses.courses_count` ja `m_courses.get_courses` ratojen näyttämiseksi `select` dropdown-listaelementissä) avaus kesti n. 0.44 sekuntia. Avaus tuntuu kestävän systemaattisesti kauemmin kuin vastaavat haut tekevien "Etsi ratoja" ja "Etsi kierroksia" näkymien kohdalla, todennäköisesti tämä johtuu `select` elementin raskaudesta suhteessa `datalist` `input`:iin.

* Käyttäjäsivun (tekee haut `m_rounds.round_count` ja `m_rounds.find_rounds` kahteen kertaan käyttäjän luomien menneiden ja tulevien kierrosten näyttämiseksi ja `m_rounds.user_participations_count` ja `m_rounds.find_participating_rounds` menneiden ja tulevien kierrosten näyttämiseksi, joille käyttäjä on osallistunut) avaus kesti 210.83 sekuntia.

* Kierrosnäkymän avaaminen (tekee haut `m_rounds.get_round` kierroksen tietojen näyttämiseksi ja `m_results.find_round_results` kierrokselle osallistujien tulosten näyttämiseksi) kesti n. 2.81 sekuntia.


Ylläolevien tulosten pohjalta sovellukseen lisättiin indeksejä, jotka toivottavasti nopeuttavat hakuja suurilla tietomäärillä


## Indeksien kanssa

* Etusivua hidastaa kierroshaku. Kierros viittaa skeemassa käyttäjiin `creator_id INTEGER REFERENCES users` ja `m_rounds.get_all_rounds` hakee käyttäjänimen id:n pohjalta `users` taulusta. Lisätään tämän pohjalta indeksi `CREATE INDEX idx_user_rounds ON rounds (creator_id);` tavoitteena nopeuttaa etusivun avaamista. Indeksin luomisen jälkeen avaukset vievät n. 1.55 sekuntia. Molemmat ovat siis parempia kuin tulokset ennen indeksin luomista.

* `m_rounds.get_all_rounds` haussa yhdistetään osallistumistaulu osallistujien laskemista varten `LEFT JOIN participations ON participations.round_id=rounds.id `. Voimme siis olettaa, että `participations.round_id` indeksointi `CREATE INDEX idx_round_participations ON participations (round_id);` nopeuttaa kierroshakua entisestään. Indeksin luomisen jälkeen etusivun avaus kestää n. sekunnin, eli sivun avaus nopeutui edellisestä. Tulos on heikompi kun joissain aiemmissa testeissä, koska lisäsin tulosten näyttämisen päivämääräjärjestyksessä, tämä tuntuu vievän paljon aikaa.

* Yllä olevat indeksit parantavat kaikkia kierroshakuja tekeviä näkymiä. Esimerkiksi käyttäjäsivun avaus vie nyt n. 0.46s, joka on merkittävä parannus tulokseen ennen indeksejä. Kierroksia, joille käyttäjä osalistuu haetaan kuitenkin vielä `participations.participator_id` perusteella, joten voimme kokeilla parantaisiko indeksi `CREATE INDEX idx_user_participations ON participations (participator_id);` käyttäjäsivun suorituskykyä entisestään. Indeksin lisäämisen jälkeen käyttäjäsivun avausaika on 0.13s, joten saimme indeksistä jälleen merkittävän suorituskykyparannuksen.

* "Etsi kierros" näkymän haku oletusparametreilla on nopeutunut kierroshakuun liittyvien indeksien jälkeen n. 1.7 sekuntiin. Voimme kokeilla lisätä indeksit hakuparametreille ja kokeilla saammeko tästä suorituskykyhyötyä. `CREATE INDEX idx_round_coursenames ON rounds (coursename);` ja `CREATE INDEX idx_round_start_times ON rounds (start_time);` Indeksien lisäämisen jälkeen käyttäjähaun kesto on n. 1.8 sekuntia, päivämäärähaun 1.1 sekuntia ja käyttäjähaku 1.9 sekuntia, jotka ovat verrattain heikkoja tuloksia, mutta parannuksia vertailuarvoon. Veikkaisin, että hitaus johtuu siitä, että hakutulokset järjestetään päivämääräjärjestykseen, tai siitä ettei indekseillä ole yhtä paljon merkitystä `LIKE` vertailun yhteydessä.

* Kierrosnäkymän `m_results.find_round_results` haussa yhdistetään käyttäjätaulu `JOIN users ON users.id=results.player_id` käyttäjien nimien näyttämistä varten. Tulokset haetaan kierroksen id:n perusteella `WHERE round_id=?`. Lisäämällä indeksi `CREATE INDEX idx_user_results ON results (player_id);` avautuminen nopeutui n. 2.7 sekuntiin. Lisäämällä indeksi `CREATE INDEX idx_round_results ON results (round_id);` kierrossivu avautuu välittömästi mitatulla nopeudella 0.0 sekuntia. Huomionarvoista on, että tuloksia on testidatassa niin paljon, että indeksit ovat massiivisia, tietokannan koko kasvoi näiden indeksien lisäämisen yhteydessä n. 2.7 GB:stä n. 4.7 GB:hen.

* Sovelluksen tietokantaan voi lisätä kaikki indeksit komennolla `sqlite3 mass_test.db < indices.sql`.

* Indeksien lisäämisen jälkeen tietokannan koko on n. 4.7GB

## Muita suorituskykyhuomioita

* Käytän "Etsi ratoja" ja "Etsi kierros" näkymissä `datalist` `input` elementtiä ja "Lisää kierros" näkymässä `select` dropdown elementtiä ratojen näyttämiseen, mikä ei ole järkevää testin ratamäärällä, kaikille radoille luodaan tässä tapauksessa oma `option` elementti, joka aiheuttaa merkittäviä suorituskykyongelmia, joka tarkoittaa, ettei mikään näistä sivuista sovellu erityisen hyvin todella suurille datamäärille (sivuhuomiona `datalist` `input` tuntuu toimivan paremmin kuin `select`, mutta nämä eivät ole toistensa korvikkeita). Tilanteeseen ei tietääkseni ole hyvää ratkaisua puhdasta HTML:ää käytettäessä, jos haluaa vastaavan toiminnallisuuden. Koska sovelluksessa ei ole kuitenkaan ns. tositilanteessa tarkoitus olla kymmeniä tuhansia ratoja (esim. suomessa on vähän yli tuhat frisbeegolfrataa) pidän mielummin `select` ja `datalist` `input` elementit käytettävyyden puolesta kuin vaihtaisin ne tavallisiin text input elementteihin.