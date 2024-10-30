# Envanter Takip Uygulaması

Bu uygulama, kullanıcıların envanterlerini yönetmelerini sağlar. Ürün ekleme, düzenleme, silme işlemlerini yapabilir; satış ve stok takibi ile analizler sağlayabilirsiniz.

## Özellikler

- **Ürün Yönetimi**: Ürünleri ekleme, düzenleme, silme.
- **Kategori Yönetimi**: Ürünlerin kategorilere göre gruplandırılması.
- **Satış Yönetimi**: Satış yapma ve satış detaylarını inceleme.
- **Analizler**: Satış ve envanter verilerine göre finansal analizler.
- **Kullanıcı Oturumu**: Kullanıcı bazlı envanter ve satış işlemleri.

## Gereksinimler

Uygulamayı çalıştırmak için aşağıdaki gereksinimler yüklenmiş olmalıdır:

- Python 3.13.0
- Django 5.1.2
- Django ORM ile SQLite (varsayılan)
- İlgili bağımlılıklar için `requirements.txt` dosyasını kullanın:

```bash
pip install -r requirements.txt
```

## Kurulum

1. **Projeyi klonlayın:**

    ```bash
    git clone <repo-url>
    cd <project-directory>
    ```

2. **Gerekli bağımlılıkları yükleyin:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Veritabanını sıfırlayın:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Süper kullanıcı oluşturun:**

    ```bash
    python manage.py createsuperuser
    ```

5. **Geliştirme sunucusunu başlatın:**

    ```bash
    python manage.py runserver
    ```

6. **Tarayıcıda açın:** 

    ```
    http://127.0.0.1:8000
    ```

## Kullanım

### Ürün Yönetimi

- **Ürün Ekleme**: Yeni bir ürün eklemek için **Ürün Ekle** seçeneğini kullanın.
- **Ürün Düzenleme**: Bir ürünü güncellemek için **Düzenle** seçeneğini kullanın.
- **Ürün Silme**: Ürünü tamamen kaldırmak için **Sil** seçeneğini kullanın.

### Satış Yönetimi

- **Satış Yapma**: Stoktan ürün seçip miktar belirleyerek satış yapabilirsiniz.
- **Satış Takibi**: Satışların geçmişi **Satış Listesi** sayfasında görülebilir.

### Analizler

**Analizler** sayfasında finansal durumunuzu görüntüleyebilirsiniz:
- **Toplam Gelir ve Kar-Zarar** 
- **Kategori Bazında Dağılım**
- **Aylık ve Günlük Kar Oranı**
- **Stok Durumu ve Düşük Stok Bildirimleri**

### Kullanıcı Oturumu

- Giriş yaparak kendi envanterinize özel işlemler yapabilir ve analizlerinizi görüntüleyebilirsiniz.
- Yönetici olarak süper kullanıcı girişi ile diğer kullanıcıların envanter bilgilerini yönetebilirsiniz.
```
