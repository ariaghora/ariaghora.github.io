class Persegi:
    def __init__(self, panjang_sisi):
        self._panjang_sisi = panjang_sisi

    @property
    def panjang_sisi(self):
        return self._panjang_sisi

    @panjang_sisi.setter
    def panjang_sisi(self, panjang_sisi):
        if panjang_sisi < 0:
            raise ValueError("Panjang sisi tidak boleh bernilai negatif")
        self._panjang_sisi = panjang_sisi

    def hitung_luas(self):
        return self.panjang_sisi**2


persegi = Persegi(10)

print(f"Panjang sisi mula-mula: {persegi.panjang_sisi}")
print(f"Luas persegi mula-mula: {persegi.hitung_luas()}")

print()

persegi.panjang_sisi = 30
print(f"Panjang sisi sekarang: {persegi.panjang_sisi}")
print(f"Luas persegi sekarang: {persegi.hitung_luas()}")

print()

persegi.panjang_sisi = -10
print(f"Panjang sisi sekarang: {persegi.panjang_sisi}")
print(f"Luas persegi sekarang: {persegi.hitung_luas()}")
