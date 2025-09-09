import time as t
import random
import haravasto as h

pelitiedot = {
    "voitto" : False,
    "jatketaanpelia" : True,
    "painallukset" : 0,
    "pelialkaa" : 0,
    "peliloppuu" :0
}

def miinoita(pelikentta, vapaat_ruudut, miinat):
    """Asettaa kentälle annetun määrän miinoja satunnaisiin paikkoihin."""
    n = int(miinat)
    for _ in range(n):
        valittu_x, valittu_y = random.choice(vapaat_ruudut)
        while pelikentta[valittu_y][valittu_x] == "x":
            valittu_x, valittu_y = random.choice(vapaat_ruudut)
        pelikentta[valittu_y][valittu_x] = "x"
        vapaat_ruudut.remove((valittu_x, valittu_y))

def laske_miinat(pelikentta):
    """Laskee ruudun ympärillä olevat miinat."""
    kentankorkeus = len(pelikentta)
    kentanleveys = len(pelikentta[0])
    for monikko in jaljella:
        ykord, xkord = monikko[1], monikko[0]
        miinat = 0
        for m in range(-1, 2):
            for n in range(-1, 2):
                uusi_x = xkord + n
                uusi_y = ykord + m
                if 0 <= uusi_x < kentanleveys and 0 <= uusi_y < kentankorkeus:
                    if pelikentta[uusi_y][uusi_x] == 'x':
                        miinat += 1
        pelikentta[ykord][xkord] = str(miinat)

def piirra_kentta():
    """Piirtää miinakentän ruudut näkyviin peli-ikkunaan."""
    h.tyhjaa_ikkuna()
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    for valittu_y, rivike in enumerate(alkukentta):
        for valittu_x, ruutu in enumerate(rivike):
            h.lisaa_piirrettava_ruutu(ruutu, valittu_x * 40, valittu_y * 40)
    h.piirra_ruudut()

def tulvataytto(pelikentta, xkord, ykord):
    """Avaa valitun ruudun ympäriltä turvalliset ruudut."""
    kentankorkeus = len(pelikentta)
    kentanleveys = len(pelikentta[0])
    tuntemattomat = [(xkord, ykord)]
    while tuntemattomat:
        xkord, ykord = tuntemattomat.pop()
        pelikentta[ykord][xkord] = kentta[ykord][xkord]
        if pelikentta[ykord][xkord] == "0":
            for m in range(-1, 2):
                for n in range(-1, 2):
                    uusi_x = xkord + n
                    uusi_y = ykord + m
                    if 0 <= uusi_x < kentanleveys and 0 <= uusi_y < kentankorkeus:
                        if pelikentta[uusi_y][uusi_x] == " ":
                            tuntemattomat.append((uusi_x, uusi_y))

def aloitusikkuna():
    """Luodaan aloitusikkuna, johon palataan pelin päättyttyä."""
    h.tyhjaa_ikkuna()
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    h.lisaa_piirrettava_ruutu("f", 550, 105)
    h.lisaa_piirrettava_ruutu("x", 550, 185)
    h.lisaa_piirrettava_ruutu("1", 550, 265)
    h.piirra_ruudut()
    h.piirra_tekstia("PELAA MIINAHARAVAA!", 95, 400,
                    vari = (255, 95, 0, 255), fontti = "Courier New", koko = 40)
    h.piirra_tekstia(" ALOITA ->", 245, 260,
                    vari = (255, 95, 0, 255), fontti = "Courier New", koko = 32)
    h.piirra_tekstia(" LOPETA ->", 245, 180,
                    vari = (255, 95, 0, 255), fontti = "Courier New", koko = 32)
    h.piirra_tekstia(" TILASTO ->", 235, 100,
                    vari = (255, 95, 0, 255), fontti = "Courier New", koko = 32)
          
def havio():
    "Pelin hävittyä luo ikkunan jota ei voida muokata."
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    for valittu_y, rivike in enumerate(alkukentta):
        for valittu_x, ruutu in enumerate(rivike):
            if kentta[valittu_y][valittu_x] == "x":
                ruutu = "x"
            else:
                ruutu = alkukentta[valittu_y][valittu_x]
            h.lisaa_piirrettava_ruutu(ruutu, valittu_x * 40, valittu_y * 40)
            h.piirra_ruudut()
            h.piirra_tekstia("HÄVISIT PELIN!", leveys * 1.2, korkeus * 20,
                            vari = (255, 95, 0, 255),
                            fontti = "Courier New", koko = leveys * 3.5)
            h.aseta_hiiri_kasittelija(sulje)
            pelitiedot["peliloppuu"] = t.time()
    
def voitto():
    """Peli päättyy voittoon."""
    piirra_kentta()
    h.piirra_tekstia("VOITIT PELIN!", leveys * 1.3, korkeus * 20,
                    vari = (255, 95, 0, 255), fontti = "Courier New", koko = leveys * 3.5)
    pelitiedot["voitto"] = True
    h.aseta_hiiri_kasittelija(sulje)
    pelitiedot["peliloppuu"] = t.time()

def kasittele_pelihiiri(xkoordinaatti, ykoordinaatti, nappi, muokkausnappaimet):
    """Tätä kutsutaan, kun käyttäjä klikkaa hiirellä ikkunaa."""
    xkord, ykord = int(xkoordinaatti / 40), int(ykoordinaatti / 40)
    tulvataytto(alkukentta, xkord, ykord)
    luku = 0
    for i in alkukentta:
        for j in i:
            luku += j.count(" ")
    avaamaton = luku
    if avaamaton == miinojen_lkm:
        alkukentta[ykord][xkord] = kentta[ykord][xkord]
        h.aseta_piirto_kasittelija(voitto)
    else:
        if kentta[ykord][xkord] == "x":
            alkukentta[ykord][xkord] = "x"
            h.aseta_piirto_kasittelija(havio)
        else:
            piirra_kentta()
    pelitiedot["painallukset"] += 1

def kasittele_alkuhiiri(xkord, ykord, nappi, muokkausnappaimet):
    """Kasittelee alkuvalikon hiiren."""
    if 550 <= xkord <= 590 and 105 <= ykord <= 145:
        with open("miinaharava_suoritus.csv") as lue:
            print(lue.read())
    elif 550 <= xkord <= 590 and 185 <= ykord <= 225:
        sulje(xkord, ykord, nappi, muokkausnappaimet)
        pelitiedot["jatketaanpelia"] = False
        sulje(xkord, ykord, nappi, muokkausnappaimet)
    elif 550 <= xkord <= 590 and 265 <= ykord <= 305:
        sulje(xkord, ykord, nappi, muokkausnappaimet)

def peli():
    """Luo pelin ja ikkunan."""
    pelitiedot["voitto"] = False
    pelitiedot["painallukset"] = 0
    miinoita(kentta, jaljella, miinojen_lkm)
    laske_miinat(kentta)
    h.lataa_kuvat("spritet")
    h.luo_ikkuna(leveys * 40, korkeus * 40)
    h.aseta_piirto_kasittelija(piirra_kentta)
    h.aseta_hiiri_kasittelija(kasittele_pelihiiri)
    h.aloita()

def ajan_talletus():
    """Tallettaa ajan tiedostoon."""
    pelinkesto = (pelitiedot["peliloppuu"] - pelitiedot["pelialkaa"]) 
    # https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python
    minuutti = int(pelinkesto // 60)
    sek = int(pelinkesto % 60)
    with open("miinaharava_suoritus.csv", 'a') as lisaa:
        lisaa.write("\n")
        lisaa.write(t.strftime("%d.%m.%y KLO: %H:%M:%S ", t.localtime()))
        lisaa.write(f"\nPelin kesto: {minuutti:02}:{sek:02}\n")
        lisaa.write(f"Siirtoja: {pelitiedot['painallukset']}\n")
        lisaa.write(str(f"Kentän koko: {korkeus} x {leveys} \nMiinoja: {miinojen_lkm}\n"))
        if pelitiedot["voitto"] is True:
            lisaa.write("Lopputulos: VOITTO\n")
        elif pelitiedot["voitto"] is False:
            lisaa.write("Lopputulos: HÄVIÖ\n")

def valikko():
    """Aloitusvalikko, johon myös palataan pelin päätyttyä."""
    h.lataa_kuvat("spritet")
    h.luo_ikkuna(800, 600, (248, 200, 220, 255))
    h.aseta_piirto_kasittelija(aloitusikkuna)
    h.aseta_hiiri_kasittelija(kasittele_alkuhiiri)
    h.aloita()

def sulje(xkoordinaatti, ykoordinaatti, nappi, muokkausnappaimet):
    """Sulkee."""
    h.lopeta()

def kysy_arvoja(kysymys, virheviesti):
    """Kysyy kayttajalta arvoja ja tarkistaa niiden laadun."""
    while True:
        try:
            annettuluku = int(input(kysymys))
            if kysymys == "Anna miinojen määrä: " and annettuluku < 0:
                print(virheviesti)
                continue
            if annettuluku <= 0:
                print(virheviesti)
                continue
        except ValueError:
            print("Anna luku!")
        else:
            return annettuluku

if __name__ == "__main__":
    valikko()
    while pelitiedot["jatketaanpelia"] is True:
        leveys = kysy_arvoja("Anna kentän leveys: ", "Anna positiivinen kokonaisluku!")
        korkeus = kysy_arvoja("Anna kentän korkeus: ", "Anna positiivinen kokonaisluku!")
        miinojen_lkm = kysy_arvoja("Anna miinojen määrä: ", "Anna epänegatiivinen luku!")

        kentta = []
        for rivi in range(korkeus):
            kentta.append([])
            for sarake in range(leveys):
                kentta[-1].append(" ")
        jaljella = []
        for x in range(leveys):
            for y in range(korkeus):
                jaljella.append((x, y))
        alkukentta = []
        for rivi in range(korkeus):
            alkukentta.append([])
            for sarake in range(leveys):
                alkukentta[-1].append(" ")

        pelitiedot["pelialkaa"] = t.time()
        peli()
        ajan_talletus()
        valikko()
        if pelitiedot["jatketaanpelia"] is False:
            break
