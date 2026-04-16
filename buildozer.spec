[app]
title = Alian AI
package.name = alianai
package.domain = com.raza.alian
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
orientation = portrait
fullscreen = 0

# --- تمام ضروری لائبریریز یہاں شامل ہیں ---
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, plyer

# --- اینڈرائیڈ سیٹنگز ---
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b
android.archs = arm64-v8a
android.permissions = INTERNET, RECORD_AUDIO
android.enable_androidx = True
android.accept_sdk_license = True
android.entrypoint = main.py

[buildozer]
log_level = 2
warn_on_root = 1
