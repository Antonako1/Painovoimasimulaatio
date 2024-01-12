# Painovoimasimulaatio
 
### Kontrollit

| Näppäin | Mitä tekee |
|---------|------------|
| P | Pause |
| O | Lisäpaneeli |
| Mouse 1 pallon päällä | Valitse pallon muokkauspaneeliin |
| R | Restart |
| H | Main menuun |
| F8 | Sammuttaa ohjelman |

### Miten käyttää

Valitse planeetta ja paina "Start simulation".

O:ta painamalla näet lisätietoja, voit lisätä uusia palloja tai muokata edellisiä klikkaamalla niitä ja muokkaamalla niiden tietoja paneelissa.

Enterillä tallenetaan input-kettien tiedot jos niitä muokataan.

12. planeetta on custom planeetta mihin voi syöttää itse planeetan massan ja säteen, joiden perusteella painovoima lasketaan (perusarvot on maapallon massa ja säde).

### Käynnistäminen

```
.\run.bat
```

tai

```
python .\src\start.py
```

### Yleisiä ominaisuuksia
| Ominaisuus | Mikä se on |
|---------|------------|
| Zero gravity | Painovoiman voi ottaa päältä - pois |
| Air resistance | Ilmanvastuksen voi ottaa päältä - pois |
| Ground friction | Maan kitkan voi ottaa päältä - pois |
| Wind speed | Tuulen nopeuden voi ottaa päältä - pois |
| Active ceiling | Katon voi ottaa päältä - pois |
| Ball collisions | Pallojen törmäykset voi ottaa päältä - pois |
| Advanced ball physics | Palloille voi antaa lisä fysiikkaa: Laskelmissa käytetään 3D Ilmanvastuksia ja pallot lyhistyy paineen alla |
| |  |
| Input-kentät | Input-kentät |
| |  |
| Air density | Ilman tiheys (kg/m^3) |
| Ground friction | Kuinka monta prosenttia nopeudesta jää, kun kitkaa käytetään |
| Wind speed | Tuulen nopeus (m/s) |
| Wind direction | Tuulen suunta näytön keskiosasta katsottuna |


### Pallojen ominaisuuksia
| Ominaisuus | Mikä se on |
|---------|------------|
| x-pos | Pallon x-sijainti |
| y-pos | Pallon y-sijainti |
| radius | Pallon säde |
| mass | Massa kiloina |
| ver. vel. | Pystysuuntainen nopeus |
| hor. vel. | Vaakasuuntainen nopeus |
| rigidness | Pallon jäykkyys |
| elasticity | Pallon joustavuus |
| Red | Pallon punainen väri |
| Green | Pallon vihreä väri |
| Blue | Pallon sininen väri |
| Delete | Poistaa pallon |
| Freeze | Jäädyttää pallon |
| |  |
| Throw | Heittää pallon satunnaiseen suuntaan |
| |  |
| Pallon lisäyspaneelin omat | Pallon lisäyspaneelin omat |
| Amount | Kuinka monta palloa lisätään painalluksella |
| Add new balls(s) | Lisää pallon / pallot |


