import numpy as np
def generuj_macierz_hadamarda(r):
    if r == 1:
        return np.array([[1, 1], [1, -1]])
    else:
        poprzednia_macierz = generuj_macierz_hadamarda(r - 1)
        return np.block([
            [poprzednia_macierz, poprzednia_macierz],
            [poprzednia_macierz, -poprzednia_macierz]
        ])

def tekst_na_binarne(tekst):
    binarne = ''.join(format(ord(znak), '08b') for znak in tekst)
    return [int(bit) for bit in binarne]
def podziel_na_bloki(kod_binarne, r):
    bloki = []
    for i in range(0, len(kod_binarne), r):
        blok = kod_binarne[i:i + r]
        while len(blok) < r:
            blok.append(0)
        bloki.append(blok)
    return bloki
def koduj_blok(blok, macierz_hadamarda):
    indeks = int("".join(map(str, blok)), 2)
    return macierz_hadamarda[indeks]
def dodaj_bled(zakodowane_bloki, poziom_bledu):
    Z_Bledami = []
    for blok in zakodowane_bloki:
        bled = np.random.choice([-1, 1], size=len(blok), p=[poziom_bledu, 1 - poziom_bledu])
        Z_Bledami.append(blok * bled)
    return Z_Bledami
def dekoduj_blok(otrzymany_blok, macierz_hadamarda):
    odleglosci = np.dot(macierz_hadamarda, otrzymany_blok)
    indeks_max = np.argmax(odleglosci)
    return indeks_max
def dekoduj_wiadomosc(Z_Bledami, macierz_hadamarda, r):
    dekodowane_binarne = []
    for blok in Z_Bledami:
        indeks = dekoduj_blok(blok, macierz_hadamarda)
        binarny_blok = [int(bit) for bit in bin(indeks)[2:].zfill(r)]
        dekodowane_binarne.extend(binarny_blok)
    return dekodowane_binarne
def binarne_na_tekst(kod_binarne):
    znaki = [chr(int("".join(map(str, kod_binarne[i:i + 8])), 2)) for i in range(0, len(kod_binarne), 8)]
    return ''.join(znaki)

if __name__ == "__main__":
    tekst = input("Wprowadź tekst do zakodowania: ")
    r = int(input("Wprowadź wymiar r (np. 2, 3, 4): "))
    poziom_bledu = float(input("Podaj poziom bledu (np. 0.1 dla 10% bledu): "))

    macierz_hadamarda = generuj_macierz_hadamarda(r)
    print("Macierz Hadamarda:")
    print(macierz_hadamarda)

    kod_binarne = tekst_na_binarne(tekst)
    print("\nKod binarny wiadomości:")
    print(kod_binarne)

    bloki = podziel_na_bloki(kod_binarne, r)
    print("\nBloki binarne:")
    print(bloki)

    zakodowane_bloki = [koduj_blok(blok, macierz_hadamarda) for blok in bloki]
    print("\nZakodowane bloki:")
    for blok in zakodowane_bloki:
        print(blok)

    Z_Bledami = dodaj_bled(zakodowane_bloki, poziom_bledu)
    print("\nBloki z bledami:")
    for blok in Z_Bledami:
        print(blok)

    dekodowane_binarne = dekoduj_wiadomosc(Z_Bledami, macierz_hadamarda, r)
    print("\nDekodowane binarne:")
    print(dekodowane_binarne)

    dekodowany_tekst = binarne_na_tekst(dekodowane_binarne)
    print("\nDekodowany tekst:")
    print(dekodowany_tekst)
