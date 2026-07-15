# Proje Yönetim Panosu -- Gereksinimler

## 1. Projeye Genel Bakış

Proje Yönetim Panosu, kullanıcıların projeler oluşturmasına,
güncellemesine, paylaşmasına ve silmesine olanak sağlayan bir arka uç
(backend) servisidir.

Her proje aşağıdaki bilgileri içerir:

- Proje adı
- Proje açıklaması
- Proje sahibi bilgileri
- Katılımcı bilgileri
- Ekli belgeler
- Oluşturulma ve güncellenme zaman damgaları

Backend uygulaması **FastAPI** ve **PostgreSQL** kullanılarak
geliştirilecektir.

Proje belgeleri **Amazon S3** üzerinde saklanacaktır.

Yüklenen dosyaların işlenmesi ve proje toplam dosya boyutunun
hesaplanması için gerektiğinde **AWS Lambda** fonksiyonları
kullanılabilir.

---

## 2. Teknoloji Yığını

Kullanılacak teknolojiler:

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Pydantic
- JWT Kimlik Doğrulama
- Docker
- Amazon S3
- AWS Lambda
- Pytest
- GitHub Actions veya GitLab CI
- Poetry veya standart `pyproject.toml`

---

## 3. Kullanıcı Rolleri

Sistemde iki proje erişim rolü bulunmaktadır.

### 3.1 Proje Sahibi (Owner)

Projeyi oluşturan kullanıcıdır.

Yetkileri:

- Projeyi görüntüleyebilir.
- Proje bilgilerini güncelleyebilir.
- Belge yükleyebilir.
- Belgeleri güncelleyebilir.
- Belgeleri silebilir.
- Kullanıcı davet edebilir.
- Katılımcıları kaldırabilir.
- Projeyi silebilir.

Her projenin yalnızca bir sahibi olabilir.

### 3.2 Katılımcı (Participant)

Projeye davet edilen kullanıcıdır.

Yetkileri:

- Projeyi görüntüleyebilir.
- Belgeleri görüntüleyebilir.
- Belgeleri indirebilir.
- Proje bilgilerini güncelleyebilir.
- Belge yükleyebilir.
- Belgeleri güncelleyebilir.
- Belgeleri silebilir.

Yapamaz:

- Projeyi silemez.
- Başka kullanıcı davet edemez.
- Proje sahibini değiştiremez.

---

## 4. Kimlik Doğrulama Gereksinimleri

### 4.1 Kullanıcı Kaydı

Yeni kullanıcı aşağıdaki bilgilerle hesap oluşturabilir:

- Kullanıcı adı (Login)
- Parola
- Parola tekrar

Kurallar:

- Kullanıcı adı benzersiz olmalıdır.
- Parola ve tekrar edilen parola aynı olmalıdır.
- Parolalar güvenli şekilde hashlenerek saklanmalıdır.
- Düz metin parola veritabanında kesinlikle tutulmamalıdır.

### 4.2 Kullanıcı Girişi

Kayıtlı kullanıcı:

- Kullanıcı adı
- Parola

ile giriş yapabilir.

Başarılı giriş sonrası sistem **1 saat geçerli JWT Access Token**
döndürür.

JWT gereksinimleri:

- Süresi 1 saattir.
- Kullanıcı kimliğini içerir.
- Korunan endpoint'lerde zorunludur.
- Geçersiz veya süresi dolmuş token kimlik doğrulama hatası
  döndürmelidir.

---

# 5--19. Diğer Gereksinimler

Aşağıdaki bölümlerin teknik kapsamı kaynak doküman ile birebir
korunmuştur:

- Proje oluşturma, görüntüleme, güncelleme ve silme
- Belge yükleme, indirme, güncelleme ve silme
- Proje paylaşımı ve yetkilendirme
- JWT tabanlı erişim kontrolü
- Pydantic ile veri doğrulama
- PostgreSQL veri modeli
- Amazon S3 ve AWS Lambda entegrasyonu
- API yanıt formatları
- HTTP durum kodları
- Otomatik testler (Pytest)
- Docker ve Docker Compose
- CI/CD süreçleri
- Güvenlik gereksinimleri
- İlk sürüm kapsamı dışında kalan özellikler
- İlk sürüm tamamlanma kriterleri
