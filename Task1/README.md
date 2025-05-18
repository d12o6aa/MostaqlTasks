# YouTube Playlist Video Checker 🎬

هذا المشروع مبني باستخدام Python وFlask ويستخدم YouTube Data API للبحث عن قوائم التشغيل التي تحتوي على فيديو معين من خلال ID الفيديو.

---

## 🚀 كيف يعمل المشروع؟

- تدخل ID الفيديو على واجهة الويب.
- يبحث المشروع عن عنوان الفيديو.
- يبحث عن قوائم تشغيل تحتوي على هذا الفيديو.
- يعرض لك النتائج (اسم قائمة التشغيل، صاحبها، ورابطها).

---

## 🧾 المتطلبات

- Python 3.7 أو أعلى
- YouTube Data API Key من Google
- اتصال إنترنت

---

## 🛠️ خطوات تشغيل المشروع

### 1. تحميل المشروع
- قم بفك الضغط عن الملف `youtube_playlist_checker.zip` أو استنساخه من GitHub.

### 2. فتح المشروع في الطرفية (Terminal)
```bash
cd youtube_playlist_checker

```

### 3. إنشاء بيئة افتراضية (اختياري لكن يُفضل)
```bash
python -m venv venv
# تشغيل البيئة الافتراضية
source venv/bin/activate        # على Linux/macOS
venv\Scripts\activate           # على Windows
```

### 4. تثبيت التبعيات
```bash
pip install -r requirements.txt
```

### 5. تعديل مفتاح API (مهم)
افتح ملف `app.py` وابدل السطر التالي:
```python
API_KEY = 'YOUR_API_KEY'
```
بمفتاحك الشخصي من Google Console (الخطوات أسفل).

### 6. تشغيل المشروع
```bash
python app.py
```
ثم افتح متصفحك على:
```
http://127.0.0.1:5000
```

---

## 🔑 خطوات الحصول على YouTube Data API Key من Google Console

1. افتح موقع Google Cloud Console:  
    [https://console.cloud.google.com/](https://console.cloud.google.com/)

2. أنشئ مشروع جديد:  
    - اضغط على **Select Project → New Project**.  
    - اختر اسمًا للمشروع واضغط "Create".

3. فعّل YouTube Data API v3:  
    - من القائمة الجانبية: **APIs & Services → Library**.  
    - ابحث عن **YouTube Data API v3** واضغط "Enable".

4. أنشئ مفتاح API:  
    - **APIs & Services → Credentials → Create Credentials → API Key**.  
    - انسخ المفتاح الناتج.

5. ضع المفتاح في ملف `app.py` بدلًا من `YOUR_API_KEY`.

---

## 📦 ملفات المشروع

```plaintext
youtube_playlist_checker/
│
├── app.py                  ← الكود الرئيسي
├── requirements.txt        ← ملف التبعيات
├── README.md               ← ملف الشرح
├── templates/
│   ├── index.html          ← واجهة إدخال الفيديو
│   └── result.html         ← صفحة النتائج
```

---

## 📌 ملاحظات

- لو الـ API Key اتجاوز الحصة اليومية، يجب الانتظار أو طلب زيادة من Google.
- لا تنشر مفتاحك للعامة.
- يمكنك تخزين النتائج في CSV لاحقًا لتسريع عمليات البحث وتفادي التكرار.

---

## 📞 الدعم

لو عندك أي استفسار أو طلب تعديل على المشروع، تقدر تتواصل معى
بالتوفيق! 🌟
```
