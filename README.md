# Plot&Print

Kitap ve film yorumlarının paylaşıldığı bir Django web platformu. Kullanıcılar kayıt olup kitap/film arayabilir, detaylarına bakabilir, puan ve yorum ekleyebilir.

🔗 **Canlı site:** https://hilalkoc.pythonanywhere.com

## Özellikler

- Kitap ve film listeleme, arama, kategoriye göre filtreleme
- Sayfalama (pagination)
- Kullanıcı kayıt / giriş / çıkış sistemi
- Yorum ekleme, düzenleme, silme (sadece yorumun sahibi)
- 1-5 arası puanlama ve ortalama puan gösterimi
- Kapak görseli yüklenmemiş kitap/filmler için Wikipedia'dan otomatik görsel çekme
- Admin panelinden içerik ve kategori yönetimi
- Mint-mavi, modern ve responsive tasarım

## Kullanılan Teknolojiler

- **Backend:** Django 5.1
- **Veritabanı:** SQLite
- **Frontend:** Bootstrap 5
- **Diğer:** Wikipedia API (kapak görselleri için), WhiteNoise (statik dosya servisi)

## Proje Yapısı

```
yorumplatformu/      # Django proje ayarları
reviews/              # Ana uygulama (modeller, view'lar, template'ler)
  ├── models.py        # Book, Movie, Category, Review modelleri
  ├── views.py          # Liste, detay, CRUD view'ları
  ├── templates/         # HTML şablonları
  ├── templatetags/       # Wikipedia görsel çekme yardımcı fonksiyonu
  └── management/commands/ # fetch_wiki_images komutu
```

## Yerelde Çalıştırma

1. Depoyu klonla:
   ```bash
   git clone https://github.com/hilalkoc1907/plot-and-print.git
   cd plot-and-print
   ```

2. Sanal ortam oluştur ve aktif et:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Paketleri kur:
   ```bash
   pip install -r requirements.txt
   ```

4. Proje kökünde `.env` dosyası oluştur:
   ```
   SECRET_KEY=kendi-gizli-anahtarin
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

5. Veritabanını hazırla ve süper kullanıcı oluştur:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Sunucuyu başlat:
   ```bash
   python manage.py runserver
   ```

7. Tarayıcıda `http://127.0.0.1:8000` adresini aç.

## Yeni İçerik Eklerken

Admin panelinden (`/admin/`) yeni bir kitap veya film eklendiğinde, kapak görselinin Wikipedia'dan otomatik gelmesi için şu komutu çalıştır:

```bash
python manage.py fetch_wiki_images
```

