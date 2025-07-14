# Alpukat-api

Aplikasi **AlpukatKU** adalah aplikasi berbasis web yang menggunakan **FastAPI** dan **TensorFlow Lite** untuk melakukan inferensi pada gambar daun alpukat. Aplikasi ini akan menerima gambar daun alpukat dan memberikan prediksi terkait jenis alpukat berdasarkan model **TensorFlow Lite** yang telah dilatih.

## Fitur

* **Prediksi Gambar**: Upload gambar daun alpukat dan dapatkan prediksi terkait jenis alpukat menggunakan model **TensorFlow Lite**.
* **Informasi Tambahan**: Setelah mendapatkan prediksi, aplikasi juga memberikan informasi lebih lanjut mengenai jenis alpukat tersebut, termasuk manfaatnya.
* **Penggunaan Model TensorFlow Lite**: Model TFLite ringan dan dapat di-deploy di cloud seperti **Render.com**.

## Prasyarat

Sebelum memulai, pastikan Anda sudah memiliki hal-hal berikut:

* **Python 3.8+**: Pastikan Python terinstal di sistem Anda.
* **Git**: Digunakan untuk version control dan deploy ke **Render.com**.
* **Render.com Account**: Untuk meng-host aplikasi Anda secara online.

## Instalasi

Ikuti langkah-langkah berikut untuk menyiapkan aplikasi secara lokal:

### 1. Instalasi Dependensi

Install dependencies yang diperlukan dengan **pip**:

```bash
pip install -r requirements.txt
```

### 2. Menyiapkan Model dan File Label

Pastikan file **`model.tflite`**, **`labels.json`**, dan **`avocado_info.json`** ada di dalam direktori aplikasi. Anda bisa mengonversi model Anda ke format **TFLite** dengan TensorFlow dan memuatnya ke dalam aplikasi ini.

* **`model.tflite`**: Model TensorFlow Lite yang telah dilatih untuk mengklasifikasikan jenis daun alpukat.
* **`labels.json`**: Berisi daftar label kelas yang digunakan dalam model.
* **`avocado_info.json`**: Berisi informasi tambahan tentang masing-masing label.

### 3. Menjalankan Aplikasi Secara Lokal

Untuk menjalankan aplikasi secara lokal di komputer Anda, gunakan **uvicorn**:

```bash
uvicorn main:app --reload
```

Aplikasi akan dapat diakses di `http://127.0.0.1:8000`.

### 4. Mengakses Endpoint Prediksi

Untuk menguji aplikasi, Anda bisa mengakses endpoint prediksi dengan mengirimkan gambar daun alpukat melalui endpoint **`/predict`**. Anda dapat menggunakan alat seperti **Postman** atau **curl** untuk mengirimkan permintaan POST dengan gambar.

Contoh permintaan **curl**:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/your/image.jpg'
```

### 5. Deployment ke Render.com

Render.com adalah platform cloud yang memungkinkan Anda untuk dengan mudah meng-deploy aplikasi **FastAPI**.

#### 5.1 Membuat Aplikasi di Render

1. **Login ke Render.com**.
2. Klik **Create a New Web Service**.
3. Pilih **GitHub** dan sambungkan repositori Anda.
4. Pilih **Python** sebagai bahasa pemrograman.
5. Pastikan Anda sudah menambahkan file **`Procfile`** untuk memberi tahu Render bagaimana cara menjalankan aplikasi.

Isi **`Procfile`** adalah:

```plaintext
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 5.2 Konfigurasi Aplikasi

Render akan otomatis mendeteksi aplikasi Python Anda dan menginstal dependensi dari **`requirements.txt`**. Setelah aplikasi berhasil di-deploy, Render akan memberikan URL untuk mengakses aplikasi Anda secara online.

#### 5.3 Mengakses Aplikasi

Setelah berhasil dideploy, Anda akan menerima URL dari Render untuk mengakses aplikasi Anda secara online. Anda bisa mengirimkan gambar daun alpukat untuk mendapatkan prediksi dari model TFLite yang telah dideploy.

## Struktur Direktori

Berikut adalah struktur direktori aplikasi ini:

```plaintext
Alpukat-api/
│
├── main.py               # File utama aplikasi FastAPI
├── requirements.txt      # Daftar dependensi Python yang diperlukan
├── avocado_info.json     # Informasi tambahan tentang jenis alpukat
├── labels.json           # Daftar label untuk model
├── model.tflite          # Model TensorFlow Lite yang sudah dilatih
├── Procfile              # Digunakan oleh Render.com untuk menjalankan aplikasi
└── README.md             # Dokumen ini
```

## Debugging dan Error Handling

Jika aplikasi tidak berjalan seperti yang diharapkan, pastikan bahwa:

* **Model TFLite** berhasil dimuat.
* **File label** telah diatur dengan benar dan terhubung dengan aplikasi.
* **Gambar yang di-upload** sesuai dengan format yang diharapkan oleh model (224x224 pixels, RGB).

Jika terjadi kesalahan saat memuat model, pastikan bahwa file model dan label berada di lokasi yang tepat dan sudah tersedia.

## Lisensi

Aplikasi ini menggunakan lisensi MIT. Anda dapat menggunakannya, memodifikasinya, dan mendistribusikannya sesuai kebutuhan.
