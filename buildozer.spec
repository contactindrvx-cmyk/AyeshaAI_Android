[app]

# (ایپ کی بنیادی معلومات)
title = Alian AI
package.name = alianai
package.domain = com.raza.alian
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# (لوگو اور سپلیش سکرین کی سیٹنگ - آئیکن غائب نہیں ہوگا)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

# (لائبریریز جو ایپ کو چلانے اور انٹرنیٹ سے جوڑنے کے لیے لازمی ہیں)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, plyer

# (سکرین اور پرمیشنز)
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, RECORD_AUDIO

# (اینڈرائیڈ 16 اور جدید فونز کا آرکیٹیکچر)
android.archs = arm64-v8a
android.allow_backup = True

# (اینڈرائیڈ API سیٹنگز - API 34 سب سے مستحکم ہے)
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b

# (اینڈرائیڈ 16 کے گرافکس کریش کو روکنے کے لیے خصوصی سیٹنگز)
android.meta_data = com.google.android.gms.vision.DEPENDENCIES=barcode, android.max_aspect=2.1
android.copy_libs = 1
android.enable_androidx = True

# (بلڈ کے لیے لازمی اجازتیں)
android.accept_sdk_license = True
android.entrypoint = main.py

[buildozer]

# (لاگ اور وارننگ کنٹرول)
log_level = 2
warn_on_root = 1
