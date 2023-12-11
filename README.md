# miniprojekti

![CI Badge](https://github.com/sevonj/miniprojekti/actions/workflows/main.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/sevonj/miniprojekti/graph/badge.svg?token=YENFDFJKT2)](https://codecov.io/gh/sevonj/miniprojekti)


Miniprojekti on täällä


[Backlog](https://tree.taiga.io/project/sevonj-miniprojekti/)

[Codecov](https://app.codecov.io/gh/sevonj/miniprojekti)

[Definition of Done ja tuntikirjaukset](https://tree.taiga.io/project/sevonj-miniprojekti/wiki/home)

### Ohjeet
#### Vaatimukset:
- Python versio 3.10 tai uudempi
- Poetry

#### Asennus:
- Kloonaa tai lataa repositorio
- Avaa projektin juurihakemisto terminaalissa
- Suorita komento `poetry install`

#### Käyttö:
- Avaa projektin juurihakemisto terminaalissa
- Suorita komento `poetry run python src/main.py`

### Arvosteluperusteet

- ryhmän kaikki jäsenet ovat antaneet vertaispalautetta [täältä](https://study.cs.helsinki.fi/stats/courses/ohtu2023/miniproject) ("Create peer review" napin takaa) viimeistään perjantaina 22.12. klo 23:59
    - [ ] Julius
    - [ ] Juho
    - [ ] Miina
    - [ ] Modar
    - [X] Tamás

#### Raportti

"Ryhmä4" nimellä perustettiin ryhmämme. Sovelluksemme on yksinkertainen komentorivi-sovellus jonka avulla pystyy luoda/tuoda/viedä bibliograafisia viitteitä `LaTeX` muodaossa. Taustalla käytetään muutamaa 3rd-party kirjastoa, kuten `pybtex` ja `tabulate`, loput riippuvuuksiamme näkyy [täältä](./pyproject.toml).

##### Sprint 1

Tehtiin Definition of Done ja otettiin käyttöön placeholder yksikkötestit. Alusta lähtien pyrimme modulaarisesti rakentaa ylös sovelluksemme, `app.py` sisälsi sovelluslogiika, `main.py` sisälsi käyttäjä-interaktioon liittyviä asioita. Sovittiin, että noudataan feature-branch:ien käyttöä, jota otimme noin vakavasti, ettei sallittiin PR:in merge:eä niin pitkään kuin jokin moduuli ei sisältänyt pelkästään sinne kuuluvia osia. CI pipeline rakennettu.

Tärkeämmät edistykset sprintin aikana:
- User can add entry
- User can list entries

##### Sprint 2

Otettiin käyttöön pylint, tehtiin HELP funktio joka kuvaa komentojen toimintaa käyttäjälle, muotoiltiin asiakasvaatimusten mukaiseksi listauskomennomme tulosteen. Haku- ja poistotoiminnat tulivat implementoiduksi. Tehtiin ensimmäiset kattavammat yksikkötestit ja luopuimme placeholder yksikkötesteista. Robot Framework:in alustavat testit tuli käyttöönotetuksi.
Tämän jakson aikana törmättiin eri user story:en aikataulutusongelmaan, jossa toinen jäsen teki noin 90% valmiustilaan 1 toiminnan ja joutui odottaa toisen jäsenen tekemän toiminnan valmistumista. Todettiin retrossa, että parikoodaus on hyödyllinen.

Tärkeämmät kohdat sprintin aikana:
- User can filter entries
- User can delete entries

##### Sprint 3

Implementoimme DOI importin linkin kautta, sekä export ja import toiminnat. Eristettiin käyttöliittymään liittyvät asiat `ui.py` moduuliin. Estimme identisten title kenttien lisäämistä. Robot testien siivous.
Tässä sprintissä tehtiin enempää parikoodausta.

<!--oliko RETRO:ssa mitää merkittävää sanottu?-->

Tärkeämmät kohdat:
- DOI perusteella import
- export/import toiminnat

##### Sprint 4

WiP 
<!-- täydennetään jälkikäteen, vaikka perjantai illalla -->

Tärkeämmät kohdat:
- placeholder
- placeholder
