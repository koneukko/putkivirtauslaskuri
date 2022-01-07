#! /usr/bin/env python3

# Tama on putkivirtauslaskuri, joka ensin laskee annettujen lahtoarvojen perusteella puuttuvat lahtoarvot ja kitkahaviokertoimen.

import math

def laske_f(epsilon, D_putki, Reiska, iteraatiot):
    #Onko laminaarista tai transistiovaiheessa

    if Reiska <= 2300:
        laskettu_f = 64/Reiska
    
    elif Reiska < 4000:
        laskettu_f = "transistio"
        #Transistiovaiheessa ei voida laskea tarkasti

    else:
        #Kaytetaan Haalandin eksplisiittista aproksimaatiota
        #kitkahaviakertoimen laskentaan. Talla saadaan alustava aproksimaatio.
        pinnankarheus = epsilon/D_putki
        print(pinnankarheus)
        kaarisulut = (pinnankarheus/3.7)**1.11
        hakasulut = kaarisulut+ 6.9/Reiska
        valitulos = -1.8*math.log10(hakasulut)
        #Tassa on nyt alkuarvaus f:n iteroimista varten.
        #Seuraavaksi iteroidaan Colebrookin kaavalla oikeampi vastaus
        #kayttaen Newtonin menetelmaa.
        x = valitulos
        f = 0
        A = pinnankarheus/3.7
        B = 2.51/Reiska
        
        for i in range(1, iteraatiot):
            f = x + 2*math.log10(A+B*x)
            f_pilkku = 1+ 2*((B/math.log(10))/(A+B*x))
            x = x -f/f_pilkku
        
        laskettu_f = x**-2

    return laskettu_f

def kysy_arvot():
    #Nimensa mukainen funktio, osa arvoista piti muuttaa luvuiksi jo tassa
    #virheenkasittely puuttuu!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    tilavuusvirta = input("Syota tahan tilavuusvirta (m^3/s):\n")
    putken_halkaisija = input("Syota tahan putken halkaisija (mm):\n")
    kineettinen_viskositeetti = float(input("Syota tahan nesteen kineettinen viskositeetti (cSt):\n"))
    kineettinen_viskositeetti = kineettinen_viskositeetti * 10**(-4)
    pinnankarheus = input("Syota tahan putken pinnankarheus (mm):\n")
    iteraatiot_lkm = input("Maarita iteraatiokertojen maara kokonaislukuna(3 on vakioarvo\n")
    return tilavuusvirta, putken_halkaisija, kineettinen_viskositeetti, pinnankarheus, iteraatiot_lkm



def main():
    print("Tama laskuri laskee Darcyn haviokertoimen ja siita annettujen parametrien avulla eri juttuja kunhan kerkian koodata")
    
    #kysytaan lahtoarvot ja muutetaan ne SI-yksikoiksi
    arvo_lista = kysy_arvot()
    Q = float(arvo_lista[0])
    D = (float(arvo_lista[1]))*10**-3
    v_kin = arvo_lista[2]
    eps = (float(arvo_lista[3]))*10**-3
    n = int(arvo_lista[4])
    #Lasketaan Reynoldisn luku lahtoarvoista
    Re = (4*Q)/(math.pi*v_kin*D)
    #Lasketaan kitkahaviokeroin ja printataan se yhdessa Reynoldsin luvun kanssa.
    f= laske_f(eps, D, Re, n)
    print("f=", f, "Re=", Re)
    #Kehitettavaa tulevaisuudessa: Laskuria voidaan laajentaa laskemaan suoraan helppoja putkivirtaustilanteita.
    #Puuttuu kysely siita mita halutaan tehda (pelkka haviokerroin, putkiston painehavio, pumpulta vaadittu teho, putken halkaisija eli kolme tapausta ja pumpun optimointia.)
main()
