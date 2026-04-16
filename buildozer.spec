[app]
title = Alian AI
package.name = alianai
package.domain = com.raza.alian
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
icon.filename = %(source.dir)s/icon.png

# --- Requirements (پائتھن 3.11 ہٹا کر صرف python3 کر دیا ہے) ---
requirements = python3, kivy==2.3.0, kivymd==1.2.0, google-generativeai, requests, certifi, urllib3, charset-normalizer, idna, plyer

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

# پرمیشنز
android.permissions = INTERNET, RECORD_AUDIO

# --- سٹیبل اینڈرائیڈ سیٹنگز (API 34) ---
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.ndk_api = 21
android.skip_update = False
android.accept_sdk_license = True
android.entrypoint = main.py

[buildozer]
log_level = 2
warn_on_root = 1
