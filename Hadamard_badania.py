import numpy as np
from Hadamard import generuj_macierz_hadamarda, tekst_na_binarne, podziel_na_bloki, koduj_blok, dodaj_bled, dekoduj_wiadomosc, binarne_na_tekst

def przeprowadz_badania(liczba_testow=1000):
    r = 8

    macierz_hadamarda = generuj_macierz_hadamarda(r)

    poziomy_bledu = [0.1, 0.2, 0.3, 0.4]
    wyniki = {bled: 0 for bled in poziomy_bledu}

    for bled in poziomy_bledu:
        poprawne = 0
        for _ in range(liczba_testow):
            liczba = np.random.randint(0, 256)
            binarna = format(liczba, '08b')
            bloki = podziel_na_bloki([int(bit) for bit in binarna], r)

            zakodowane_bloki = [koduj_blok(blok, macierz_hadamarda) for blok in bloki]
            Z_Bledami = dodaj_bled(zakodowane_bloki, bled)
            dekodowane_binarne = dekoduj_wiadomosc(Z_Bledami, macierz_hadamarda, r)
            dekodowana_liczba = int("".join(map(str, dekodowane_binarne[:8])), 2)

            if dekodowana_liczba == liczba:
                poprawne += 1  

        wyniki[bled] = poprawne / liczba_testow

    return wyniki

if __name__ == "__main__":
    wyniki_badan = przeprowadz_badania()
    print("\n=== Wyniki badań ===")
    for bled, skutecznosc in wyniki_badan.items():
        print(f"Poziom bledu: {bled*100:.0f}%, Skuteczność dekodowania: {skutecznosc*100:.2f}%")