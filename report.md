# Raportti

- ryhmän kaikki jäsenet ovat antaneet vertaispalautetta [täältä](https://study.cs.helsinki.fi/stats/courses/ohtu2023/miniproject) ("Create peer review" napin takaa) **viimeistään perjantaina 22.12. klo 23:59**
    - [ ] Juho Paananen
    - [ ] Julius Sevon
    - [ ] Miina Saromaa
    - [ ] Mudar Algayal
    - [X] Tamás Tóth

"Ryhmä4" nimellä perustettiin ryhmämme. Sovelluksemme on yksinkertainen komentorivi-sovellus jonka avulla pystyy luoda/tuoda/viedä bibliograafisia viitteitä `LaTeX` muodaossa. Taustalla käytetään muutamaa 3rd-party kirjastoa, kuten `pybtex` ja `tabulate`, loput riippuvuuksiamme näkyy [täältä](./pyproject.toml).

## Mikä sujui projektissa hyvin, mitä pitäisi parantaa seuraavaa kertaa varten

Kun toi "Assembler" hajosi alussa, turhaan meni aikaa manual aikatauluttamiseen satunnaisesti arvottujen ryhmäjäsenten kanssa.

## Mitä asioita opitte, mitä asioita olisitte halunneet oppia, mikä tuntui turhalta

Opimme Taigan, feautre branch:ien käytön, sekä parikoodaamisen arvoa.

Tuntui vähän ikävältä parikoodamisen yhteisten kommittien säätäminen, joten luovutettiin ideasta ja jakeltiin mieluummin USER STORY:en TASK:it 1-1 per nenä ja tehtiin asiat vuorotelleen, kun kuitenkin molemmat oli kärryllä. 

## Sprintien läpikäynti

<!--
    Kerrataan jokaisen sprintin aikana kohdatut ongelmat (prosessiin-, projektityöskentelyyn- ja teknisiin asioihin liittyvät)
-->

Simuloitiin työpaikan ympäristö ja harrastettiin Scrum:in toiminnat tässä 4 viikon aikana, jokaisen Sprintimme pituus oli 1 viikko, jäsenet kulutti suunnilleen 6 tuntia/nenä/sprintti. Ensimmäistä Sprintiä lukuunottamatta pidettiin retrospektiivi Sprintien lopussa. Alla käydään läpi yksittäisten jaksojen sisällöt/tapahtumat.

### Sprint 1

Tehtiin Definition of Done ja otettiin käyttöön placeholder yksikkötestit. Alusta lähtien pyrimme modulaarisesti rakentaa ylös sovelluksemme, `app.py` sisälsi sovelluslogiika, `main.py` sisälsi käyttäjä-interaktioon liittyviä asioita. Sovittiin, että noudataan feature-branch:ien käyttöä, jota otimme noin vakavasti, ettei sallittiin PR:in merge:eä niin pitkään kuin jokin moduuli ei sisältänyt pelkästään sinne kuuluvia osia. CI pipeline rakennettu.

Tärkeämmät edistykset sprintin aikana:
- User can add entry
- User can list entries

### Sprint 2

Otettiin käyttöön pylint, tehtiin HELP funktio joka kuvaa komentojen toimintaa käyttäjälle, muotoiltiin asiakasvaatimusten mukaiseksi listauskomennomme tulosteen. Haku- ja poistotoiminnat tulivat implementoiduksi. Tehtiin ensimmäiset kattavammat yksikkötestit ja luopuimme placeholder yksikkötesteista. Robot Framework:in alustavat testit tuli käyttöönotetuksi.
Tämän jakson aikana törmättiin eri user story:en aikataulutusongelmaan, jossa toinen jäsen teki noin 90% valmiustilaan 1 toiminnan ja joutui odottaa toisen jäsenen tekemän toiminnan valmistumista. Todettiin retrossa, että parikoodaus on hyödyllinen.

Tärkeämmät kohdat sprintin aikana:
- User can filter entries
- User can delete entries

### Sprint 3

Implementoimme DOI importin linkin kautta, sekä export ja import toiminnat. Eristettiin käyttöliittymään liittyvät asiat `ui.py` moduuliin. Estimme identisten title kenttien lisäämistä. Robot testien siivous.
Tässä sprintissä tehtiin enempää parikoodausta.

<!--oliko RETRO:ssa mitää merkittävää sanottu?-->

Tärkeämmät kohdat:
- DOI perusteella import
- export/import toiminnat

### Sprint 4

Tässä jaksossa tapahtui loppuviimeistely, suurin osa muutoksista koski makuasiat, kuten formatoinnit.
<!-- täydennetään jälkikäteen, vaikka perjantai illalla -->

Tärkeämmät kohdat:
- Improved author and title formatting
- User can edit entries
