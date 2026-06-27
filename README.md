# Analisis Persepsi Publik Program Makan Bergizi Gratis (MBG)
### ABSA (Aspect-Based Sentiment Analysis) + Topic Modeling pada Komentar Publik Digital

> Portofolio data mining & NLP — memetakan persepsi publik terhadap Program MBG melalui komentar publik di media digital, dan membandingkannya dengan klaim evaluasi resmi pemerintah.

---

## FASE 1 — Problem Framing & Scoping

### 1. Latar Belakang
Program Makan Bergizi Gratis (MBG) adalah salah satu program prioritas pemerintah yang menyasar jutaan siswa di seluruh Indonesia. Pada Mei 2026, Badan Gizi Nasional (BGN) meluncurkan aplikasi internal "Reviu MBG" yang melibatkan guru dan kepala posyandu untuk menilai kualitas makanan secara langsung di lapangan. Hasil awal evaluasi resmi menunjukkan tingkat kelayakan makanan di atas 99%.

Namun, secara paralel, program ini juga diwarnai sorotan publik yang kontras: kasus keracunan massal di beberapa daerah (termasuk temuan kontaminasi boraks dan E. coli), serta polemik anggaran transformasi IT yang disebut menyentuh angka triliunan rupiah. Kesenjangan antara **klaim evaluasi resmi** dan **persepsi publik di media digital** inilah yang menjadi titik tolak penelitian ini — sebuah celah yang belum banyak digali secara sistematis menggunakan pendekatan data science.

### 2. Problem Statement
**Bagaimana persepsi publik terhadap pelaksanaan Program Makan Bergizi Gratis (MBG) tergambar dari komentar publik di media digital, dan aspek apa yang paling dominan disorot dibandingkan klaim evaluasi resmi pemerintah?**

### 3. Research Questions
| # | Pertanyaan |
|---|---|
| RQ1 | Aspek apa yang paling sering dibahas publik terkait MBG (rasa, kebersihan, distribusi, anggaran/korupsi, respons pemerintah, dll)? |
| RQ2 | Bagaimana sentimen publik terhadap masing-masing aspek tersebut (positif/negatif/netral)? |
| RQ3 | Apakah sentimen berubah signifikan sebelum vs sesudah pemberitaan kasus keracunan/skandal anggaran mencuat? |
| RQ4 | Seberapa besar kesenjangan antara narasi publik (dominan negatif/skeptis di aspek tertentu) vs klaim evaluasi resmi BGN (>99% "layak")? |
| RQ5 (*stretch*) | Apakah ada perbedaan pola sentimen/aspek antar wilayah atau antar sumber video berita? |

### 4. Tujuan & Output
Menghasilkan pipeline data mining → NLP end-to-end (scraping → cleaning → ABSA → topic modeling → sintesis) yang menjawab RQ1–RQ4 secara terukur (tabel/chart), dengan insight yang bisa "dibaca" sebagai bentuk literasi data terhadap isu publik — bukan sekadar latihan teknis.

### 5. Scope & Batasan
- **In scope**: komentar publik di video YouTube (kanal berita: Kompas, CNN Indonesia, Tempo, Antara, dll) yang membahas Program MBG, periode ±6 bulan terakhir (mencakup sebelum & sesudah skandal mencuat).
- **Out of scope**: data internal pemerintah (dashboard Reviu MBG tidak publik), tidak menyimpulkan kebenaran/kesalahan kebijakan, tidak menyebut identitas pribadi komentator dalam laporan akhir.
- **Stance penelitian**: netral — tujuannya memetakan persepsi, bukan menghakimi program.

### 6. Unit of Analysis & Sumber Data
Satu komentar YouTube = satu unit analisis. Sumber: komentar publik pada video berita YouTube terkait MBG (data publik, tidak memerlukan login).

### 7. Success Criteria
Tiap RQ punya jawaban kuantitatif + visual; pipeline reproducible; insight bisa dikemas jadi narasi LinkedIn/blog yang punya nilai literasi data, bukan cuma demo teknis.

### 8. Catatan Etika
- Hanya menggunakan data publik (komentar YouTube yang dapat diakses tanpa login).
- Username/author di-anonimkan (hash atau drop) sebelum publikasi laporan.
- Scraping dilakukan dengan rate-limit wajar, tidak membebani server.
- Penelitian bersifat akademik/portofolio, netral secara politik, dan tidak dimaksudkan untuk menyerang pihak manapun.

### 9. Pipeline & Status
| Fase | Deskripsi | Status |
|---|---|---|
| 1 | Problem framing & scoping | ✅ |
| 2 | Data collection (scraping komentar YouTube) | ✅ — 6.401 komentar dari 67 video |
| 3 | Data cleaning & preprocessing | 🔄 *sedang dikerjakan* |
| 4 | EDA | ⬜ |
| 5 | ABSA (Aspect-Based Sentiment Analysis) | ⬜ |
| 6 | Topic Modeling (BERTopic/LDA) | ⬜ |
| 7 | Sintesis temuan (RQ1–RQ4) | ⬜ |
| 8 | Packaging untuk portofolio | ⬜ |

---

## FASE 2 — Data Collection (Scraping Komentar YouTube)

Pipeline fase 2 dipecah jadi **2 langkah** dengan satu checkpoint manual di tengah, supaya tidak buang waktu scraping komentar dari video yang ternyata tidak relevan.

### Langkah A — Cari video relevan (`search_videos.py`)
Mencari video YouTube berdasarkan kata kunci terkait MBG (otomatis, tanpa API key, pakai library `scrapetube`), lalu menyimpan daftar video (judul, video_id, channel, kata kunci) ke `data/raw/video_list.csv`.

### ⏸️ Checkpoint manual
Buka `data/raw/video_list.csv`, review judul-judulnya, **hapus baris yang tidak relevan** (misal video yang muncul karena kata kunci ambigu), simpan sebagai `data/raw/video_list_filtered.csv`.

### Langkah B — Scrape komentar (`scrape_comments.py`)
Membaca `video_list_filtered.csv`, lalu scrape komentar tiap video (pakai library `youtube-comment-downloader`, juga tanpa API key), simpan ke `data/raw/comments_raw.csv`.

**Hasil aktual:** 70 video ditemukan → dikurasi manual jadi 67 video relevan → **6.401 komentar** terkumpul.

### Cara jalankan
```bash
pip install -r requirements.txt

python scripts/search_videos.py
# -> review & filter data/raw/video_list.csv secara manual jadi video_list_filtered.csv

python scripts/scrape_comments.py
```

### Catatan teknis
- Kedua library (`scrapetube`, `youtube-comment-downloader`) bekerja dengan mem-parsing struktur internal YouTube (bukan API resmi), jadi **bisa sewaktu-waktu berhenti berfungsi** jika YouTube mengubah strukturnya — kalau error, cek versi terbaru library di PyPI/GitHub dulu.
- `MAX_COMMENTS_PER_VIDEO` di script dibatasi (default 300) untuk menjaga waktu eksekusi & sopan terhadap server — naikkan kalau perlu dataset lebih besar.
- Kata kunci pencarian sudah disusun untuk menangkap variasi temporal (sebelum/sesudah skandal) — penting untuk menjawab RQ3.

---

## FASE 3 — Data Cleaning & Preprocessing

### Pendekatan: dual-text, bukan single cleaning pass
Script `03_clean_comments.py` menghasilkan **2 versi teks bersih** dari tiap komentar, bukan cuma 1:

| Kolom | Karakteristik | Dipakai untuk |
|---|---|---|
| `text_light` | Lowercase, URL/mention/hashtag/emoji dibuang, slang dinormalisasi, **stopword & struktur kalimat tetap dipertahankan** | Embedding (BERTopic), context window ABSA — keduanya butuh kalimat alami, bukan kata acak |
| `text_bow` | `text_light` dikurangi stopword | Ekstraksi kata kunci topik (CountVectorizer di BERTopic / LDA klasik) |

### Aturan khusus: negasi tidak dianggap stopword
Kata seperti *tidak, bukan, jangan, gak, nggak* **sengaja dipertahankan** meski ada di daftar stopword default Sastrawi — karena kata itu membalik polaritas sentimen ("makanan **tidak** layak" beda total artinya dari "makanan layak"). Krusial untuk ABSA di fase 5.

### Spam/copy-paste detection
Komentar dengan teks identik yang muncul ≥5 kali di seluruh dataset ditandai sebagai kandidat spam/copypasta dan disimpan terpisah di `data/processed/spam_candidates.csv` — **bukan langsung dihapus**, karena reaksi singkat yang sama ("Setuju!", "Stop MBG") secara organik juga wajar muncul berulang dari orang berbeda. Perlu direview manual.

### Keterbatasan kamus slang
`resources/slang_dictionary.csv` adalah starter dictionary (~60 entri), fokus ke normalisasi ejaan informal → formal (misal "gk" → "tidak"), **bukan** penggabungan sinonim yang mengubah makna kata. Bahasa komentar YouTube sangat variatif (termasuk gaya "alay" — angka mengganti huruf, dst.), jadi kamus ini perlu diperluas secara iteratif: jalankan script, cek sampel `text_light`, tambahkan slang yang belum tertangani, lalu jalankan ulang.

### Cara jalankan
```bash
python scripts/clean_comments.py
```

### Yang perlu dicek setelah run
- Berapa % komentar ditandai `is_short` (kemungkinan kurang informatif untuk topic modeling)?
- Berapa komentar masuk `spam_candidates.csv` — beneran spam atau reaksi organik berulang?
- Spot-check kolom `text_light` — apakah masih banyak slang yang belum ternormalisasi?