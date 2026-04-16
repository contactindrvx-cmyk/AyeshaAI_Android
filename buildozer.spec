[app]
title = Ayesha AI
package.name = ayeshaai
package.domain = com.raza.ayesha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# لوگو کی سیٹنگ - جو آپ نے icon.png رکھا ہے
icon.filename = %(source.dir)s/icon.png

# ضروری ریکوائرمنٹس جو آپ نے کہی تھیں
requirements = python3, kivy==2.3.0, kivymd==1.2.0, google-generativeai, requests, urllib3, certifi, charset-normalizer, idna

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

# انٹرنیٹ کی اجازت (تاکہ عائشہ بات کر سکے)
android.permissions = INTERNET, RECORD_AUDIO

# اینڈرائیڈ کی سیٹنگز
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
