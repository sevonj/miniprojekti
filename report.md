# Raportti

Ryhmän kaikki jäsenet ovat antaneet vertaispalautetta [täältä](https://study.cs.helsinki.fi/stats/courses/ohtu2023/miniproject) ("Create peer review" napin takaa) **viimeistään perjantaina 22.12. klo 23:59**
- [X] Juho Paananen
- [ ] Julius Sevon
- [X] Miina Saroma
- [ ] Mudar Algayal
- [X] Tamás Tóth

Ryhmämme nimettiin dynaamisesti "Ryhmä4". Sovelluksemme on yksinkertainen komentorivi-sovellus jonka avulla pystyy luoda/tuoda/viedä bibliograafisia viitteitä `LaTeX` muodossa (`*.bib` laajennuksella). Taustalla hyödynnetään muutamaa kirjastoa, kuten `pybtex`. Täyden kuvan riippuvuuksistamme saa [täältä](./pyproject.toml).

## Mikä sujui projektissa hyvin, mitä pitäisi parantaa seuraavaa kertaa varten

Kun toi "Assembler" hajosi alussa, turhaan meni aikaa manuaaliseen aikatauluttamiseen satunnaisesti arvottujen ryhmäjäsenten kanssa. Tämä aiheutti melkoisesti päänvaivaa projektin sujuvan etenemisen takaamiseksi.

## Mitä asioita opitte, mitä asioita olisitte halunneet oppia, mikä tuntui turhalta

Opimme Taigan, feature branch:ien käytön, sekä parikoodaamisen arvoa.

Yhteisten kommittien säätäminen tuntui hieman vaivalloiselta, joten luovuimme ideasta ja jaoimme mieluummin USER STORY:en TASK:it 1-1 per nenä ja tehtiin asiat vuorotelleen, kun kuitenkin molemmat oli kärryllä. 

## Sprintien läpikäynti

<!--
    Kerrataan jokaisen sprintin aikana kohdatut ongelmat (prosessiin-, projektityöskentelyyn- ja teknisiin asioihin liittyvät)
-->

Simuloitiin työelämän ympäristöä ja toimimme Scrum:in mukaisesti 4 viikon ajan. Jokaisen Sprintimme pituus oli yksi viikko, jonka aikana tiimiläisillä oli työtunteja käytössään suunnilleen 6 tuntia/henkilö. Ensimmäistä Sprintiä lukuunottamatta pidettiin retrospektiivi Sprintien lopussa. Alla käydään läpi yksittäisten jaksojen sisällöt/tapahtumat.

### Sprint 1

Tehtiin Definition of Done ja otettiin käyttöön placeholder yksikkötestit. Alusta lähtien pyrimme rakentamaan sovelluksemme modulaarisesti, `app.py` sisälsi sovelluslogiikan, `main.py` sisälsi käyttäjä-interaktioon liittyviä asioita. Sovittiin, että noudatetaan feature-branch:ien käyttöä. Pidimme tästä tiukasti kiinni, emmekä sallineet PR:in merge:eä ennen kuin mergettävä branch oli DOD mukainen. Pyrimme huolehtimaan myös, että kuhunkin moduuliin sisällytettiin ainoastaan siihen kuuluvia osia. CI pipeline rakennettu.

Tärkeämmät edistykset sprintin aikana:
- User can add entry
- User can list entries

### Sprint 2

Otimme käyttöön pylint:in, teimme HELP funktion, joka kuvaa komentojen toimintaa käyttäjälle sekä muotoilimme listauskomentomme tulosteen asiakasvaatimuksen mukaiseksi. Implementoimme haku- ja poistotoiminnot. Teimme ensimmäiset kattavammat yksikkötestit ja luovuimme placeholder yksikkötesteistä. Otimme käyttöön Robot Framework:in alustavat testit.
Tämän jakson aikana törmäsimme eri user story:en aikataulutusongelmaan, jossa toinen jäsen teki noin 90% valmiustilaan yhden toiminnon ja joutui odottamaan toisen jäsenen vastuulla olleen toiminnon valmistumista. Todettiin retrossa, että daily scrum, kommunikaation parantaminen ja parikoodaus olisivat hyödyllisiä.

Tärkeämmät kohdat sprintin aikana:
- User can search entries
- User can delete entries

### Sprint 3

Implementoimme DOI importin linkin kautta, sekä export ja import toiminnot. Eristettiin käyttöliittymään liittyvät asiat `ui.py` moduuliin. Estimme identisten title kenttien lisäämisen. Robot testien siivous.
Tässä sprintissä tehtiin enemmän parikoodausta ja parannettiin kommunikaatiota. Sprintin retrossa totetisimme, että kommunikaatio oli parantunut mm. daily scrumien seurauksena. Totesimme, että jatkamme niitä ja panostamme myös odottelun (hukka) vähentämiseen reagoimalla mahdollisimman nopeasti Pull Request:hin

Tärkeämmät kohdat:
- DOI perusteella import
- export/import toiminnat

### Sprint 4

Tämä sprintti sisälti paljon loppuviimeistelyä, kuten formatointeja ja sovelluksen yksityiskohtien hienosäätöjä. Törmäsimme uudeelleen aikataulutusongelmaan, joka ilmeni siten, että kaksi feature branchia sisälsi samat (main haaraan) yhdistämättömät commitit. Tämä tarjosi toisaalta ihan mielenkiintoisen oppimiskokemuksen merge conflictin ratkaisemisesta.

Tärkeämmät kohdat:
- Improved author and title formatting
- User can edit entries
