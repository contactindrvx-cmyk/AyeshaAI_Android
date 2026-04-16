[app]
title = Alian AI
package.name = alianai
package.domain = com.raza.alian
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
icon.filename = %(source.dir)s/icon.png

# لائبریریز
requirements = python3==3.11.0, kivy==2.3.0, kivymd==1.2.0, google-generativeai, requests, certifi, urllib3, charset-normalizer, idna, plyer

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

# پرمیشنز
android.permissions = INTERNET, RECORD_AUDIO

# --- اینڈرائیڈ 16 (API 36) کے لیے سیٹنگز ---
android.api = 36
android.minapi = 24
android.sdk = 36
android.ndk = 26b
android.ndk_api = 24
android.skip_update = False
android.accept_sdk_license = True
android.entrypoint = main.py

[buildozer]
log_level = 2
warn_on_root = 1
