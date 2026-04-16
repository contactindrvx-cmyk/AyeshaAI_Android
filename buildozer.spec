[app]
title = Alian AI
package.name = alianai
package.domain = com.raza.alian
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# یہ دو لائنیں آپ کا آئیکن غائب نہیں ہونے دیں گی
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

# تمام ضروری لائبریریز
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, plyer

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

# پرمیشنز
android.permissions = INTERNET, RECORD_AUDIO

# اینڈرائیڈ 16 کے لیے مستحکم سیٹنگز
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b
android.enable_androidx = True
android.accept_sdk_license = True
android.entrypoint = main.py

[buildozer]
log_level = 2
warn_on_root = 1
