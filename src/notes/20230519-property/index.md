# Tentang dekorator `@property` di Python

Pada paradigma pemrograman berorientasi objek (PBO), saat berurusan dengan atribut suatu *object*, jamak ditemui penggunaan *method getter* dan *setter* (kadang disebut *accessor* dan *mutator method*[^1]).
Khususnya, ini sering ditemui saat kita bekerja dengan *data class* (kelas yang hanya digunakan untuk menyimpan data saja dan minim fungsionalitas) dan membutuhkan validasi saat meng-*assign* nilai atribut.

Misal, kita mempunyai kelas `Persegi` dengan atribut `panjang_sisi`. Kita perlu melakukan validasi saat user menentukan nilai `panjang_sisi` agar, misalnya, menghindari nilai negatif. Saat itulah *setter* (dan *getter*) dapat digunakan.

## Kelas tanpa *getter* dan *setter*
Berikut contoh kelas sederhana, tanpa *getter* dan *setter*, di mana atribut dapat diakses user secara langsung.

```python
class Persegi:
    def __init__(self, panjang_sisi):
        self.panjang_sisi = panjang_sisi

    def hitung_luas(self):
        return self._panjang_sisi**2


persegi = Persegi(10)

print(f"Panjang sisi mula-mula: {persegi.panjang_sisi}")
print(f"Luas persegi mula-mula: {persegi.hitung_luas()}")
```

Di bagian kode lain, jika kita ingin memperbarui panjang sisi persegi, kemudian mencetak ulang luasnya. 
Mudah saja:

```python
persegi.panjang_sisi = 30

print(f"Panjang sisi sekarang: {persegi.panjang_sisi}")
print(f"Luas persegi sekarang: {persegi.hitung_luas()}")
```

Dari sisi sintaks, cara ini cukup menyenangkan mata karena sederhana.
Namun, user bisa saja memasukkan nilai negatif untuk panjang sisi, sementara nilai negatif untuk panjang sisi tidaklah masuk akal.
Sementara itu, dengan membiarkan akses langsung, kita tidak punya mekanisme validasi.
Di program yang lebih kompleks, penentuan data yang tidak sesuai dengan harapan kelak dapat menimbulkan masalah tersendiri.

Alih-alih mengizinkan user langsung mengakses atribut, kita bisa menyediakan *method setter* untuk memperbarui panjang sisi, namun disertai pengecekan untuk antisipasi nilai tak diinginkan.

## Kelas dengan *getter* dan *setter*

Modifikasi pertama adalah mengubah nama atribut `panjang_sisi` dengan membubuhkan *underscore* di awal nama.
Pemberian *underscore* adalah konvensi komunitas Python untuk menunjukkan bahwa `_panjang_sisi` adalah **atribut terproteksi (_protected attribute_)**.
Atribut tersebut hanya dapat diakses melalui perantara saja (dalam hal ini *setter* dan *getter*, bila ada).

> Atribut terproteksi (*protected attribute*) adalah atribut yang tidak untuk diakses/diubah dari luar kelas. Ini hanya kesepakatan saja. User tetap bisa mengakses `persegi._panjang_sisi` dan interpreter tidak akan memberi pesan error.

Setelah itu, implementasikan *setter* (`set_panjang_sisi`) yang disertai pengecekan nilai negatif.
Kita perlu juga mengimplementasikan *getter* (`get_panjang_sisi`) untuk mengizinkan user mengakses panjang sisi (karena atribut `_panjang_sisi` sekarang sudah protected, dan sesuai kesepakatan, tidak untuk diakses langsung).

```python
class Persegi:
    def __init__(self, panjang_sisi):
        self._panjang_sisi = panjang_sisi

    def get_panjang_sisi(self):
        return self._panjang_sisi

    def set_panjang_sisi(self, panjang_sisi):
        if panjang_sisi < 0:
            raise ValueError("Panjang sisi tidak boleh bernilai negatif")
        self._panjang_sisi = panjang_sisi

    def hitung_luas(self):
        return self._panjang_sisi**2

```

Setelah kelas diperbarui, cara user memberi nilai sisi persegi juga berubah sebagai berikut:

```python
persegi.set_panjang_sisi(-10)

print(f"Panjang sisi sekarang: {persegi.get_panjang_sisi()}")
print(f"Luas persegi sekarang: {persegi.hitung_luas()}")
```

Dengan demikian, saat nilai negatif digunakan sebagai argumen untuk setter, `ValueError` *exception* akan dibangkitkan.

> Sebagian dari kita (termasuk saya) tidak menyukai pola *getter* dan *setter* yang digunakan secara eksplisit.
> Keduanya membuat kode menjadi "berisik", tidak idiomatik, tidak *pythonic*, [dan jahat jika digunakan tidak pada tempatnya](https://www.yegor256.com/2014/09/16/getters-and-setters-are-evil.html).

## Solusi: dekorator `@property`

Python menyediakan dekorator `@property`. Dengan dekorator ini, kita bisa melakukan validasi saat set nilai suatu atribut, dan melakukan format/kalkulasi (jika dibutuhkan) saat mengakses nilai atribut tersebut.
Ini mirip dengan penggunaan *setter* dan *getter*, namun lebih "alami" karena kita seolah-olah langsung berinteraksi dengan atribut tersebut.

Berikut ini pembaruan kelas dengan melibatkan property.

```python
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
        return self._panjang_sisi**2
```

Kemudian, berikut ini cara menggunakannya:

```python
# memanggil method setter persegi.panjang_sisi(30) di balik layar.
# Seolah melakukan assignment biasa, padahal di balik layar terjadi
# proses pengecekan nilai.
persegi.panjang_sisi = 30  

print(f"Panjang sisi: {persegi.panjang_sisi}")
print(f"Luas persegi: {persegi.hitung_luas()}")

print()

# memanggil method setter persegi.panjang_sisi(-10). Karena negatif,
# maka exception akan dibangkitkan.
persegi.panjang_sisi = -10  

print(f"Panjang sisi: {persegi.panjang_sisi}")
print(f"Luas persegi: {persegi.hitung_luas()}")
```

Secara personal, saya menyukai pendekatan ini karena setidaknya dua hal:

- **_Readability_**: Sintaks akan menjadi relatif lebih bersih.
- **_Simplicity_**: Kita dapat mengakses atribut layaknya sebuah atribut seperti biasanya, tanpa memanggil getter dan setter secara eksplisit. Kita cukup secara alami menetapkan (via operator *assignment* ("=")) atau mengambil sebuah nilai (akses langsung dengan operator dot (`"."`)), sekaligus dapat membubuhkan logika tambahan saat menentukan dan mengakses nilai.

[^1]: https://en.wikipedia.org/wiki/Method_(computer_programming)#Accessor,_mutator_and_manager_methods