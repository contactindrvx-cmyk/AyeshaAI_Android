[app]
title = Ayesha AI
package.name = ayeshaai
package.domain = com.raza.ayesha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
icon.filename = %(source.dir)s/icon.png

# --- یہ حصہ بہت اہم ہے، اسے پکا کریں ---
requirements = python3, kivy==2.3.0, kivymd==1.2.0, google-generativeai, requests, urllib3, certifi, charset-normalizer, idna
# ----------------------------------------

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

# --- یہ پرمیشنز لازمی ہونی چاہئیں ---
android.permissions = INTERNET, RECORD_AUDIO
# -----------------------------------

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
