# Sudah ada NumPy, kenapa pakai Pandas?

Pemula di ranah ilmu data, _machine learning_ (ML), dan sejenisnya, seringkali kebingungan dengan banyakanya perkakas dan pustsaka yang akan dipelajari.
Paling sering saya temui adalah mereka yang kebingungan menentukan kapan harus menggunakan NumPy, kapan harus menggunakan Pandas.
Apalagi keduanya sama-sama bisa dipakai sebagai input untu pustaka seperti scikit-learn (sklearn).
Tutorial ML sklearn yang menggunakan NumPy tidak kalah banyaknya dengan yang menggunakan Pandas.

# NumPy

<div class="col col-30">
<img src="https://numpy.org/images/logo.svg" width="200px"/>
</div>

<div class="col col-70">

Fitur utama dari NumPy (yang kepanjangannya adalah _numerical python_) adalah n-dimensional array (ndarray).
NumPy diimplementasikan dalam bahasa C dengan optimasi yang [sangat intensif](https://numpy.org/doc/stable/user/whatisnumpy.html#why-is-numpy-fast), sehingga memiliki performa yang baik.
NumPy didesain untuk memenuhi kebutuhan pemrosesan data numerik (walau tetap bisa menyimpan data non numerik).
NumPy dibundel dengan banyak fungsi-fungsi aritmatika untuk ndarray, termasuk aljabar linear, trigonometri, optimasi, dan sebagainya.
Oleh karena itu, NumPy cocok digunakan saat kita memiliki data numerik dan homogen.

</div>

# Pandas

<div class="col col-30">
<img src="https://pandas.pydata.org/static/img/pandas_white.svg" width="200px" style="background-color:#130754; padding: 10px 10px"/>
</div>

<div class="col col-70">

Struktur data yang merupakan punggawa dari Pandas adalah dataframe & series.
Dataframe terhimpun dari kumpulan series (kolom).
Pandas banyak digunakan saat data berbentuk tabular dengan tipe data yang heterogen.
Jadi, ia sangat ramah tidak hanya pada data integer dan float, namun juga string dan tipe lainnya.
Pandas dibuat di atas NumPy.
Pada suatu dataframe Pandas `x`, jika kita memanggil `x.values`, maka kita akan memperoleh nilai-nilainya saja dalam bentuk ndarray NumPy 2 dimensi.

</div>

# Kapan yang satu lebih baik dari lainnya?

> Tentu saja, menurut saya.

## NumPy
- Saat membutuhkan array dengan dimensi yang fleksibel dan jenis data homogen (bayangkan, anda bekerja dengan vektor, matriks, dan tensor berisi angka-angka)
- Saat membutuhkan operasi aritmatik yang melibatkan array (terlebih untuk yang berdimensi lebih dari 2): _fourier transform_, perkalian matriks, _eigendecomposition_, dsb.

## Pandas
- Saat data berorientasi tabel dan jenis datanya heterogen (bayangkan, anda bekerja dengan tabel-tabel seperti pada SQL yang berisi _field-field_ dengan tipe data berbeda)
- Saat membutuhkan operasi tabular yang intensif: _joining_, _merging_, manipulasi index dan kolom, pembersihan data, transformasi data, dsb.
- Saat menginginkan indeks dan nama kolom yang tidak harus integer.