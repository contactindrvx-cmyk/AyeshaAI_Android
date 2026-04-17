[app]
# ایپ کا نام جو موبائل پر نظر آئے گا
title = Alien AI Chat and Assistant

# پیکیج کی تفصیلات
package.name = alienchat
package.domain = com.raza.alien

# سورس فائلیں
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp4,json
version = 1.0

# ضروری لائبریریاں
requirements = python3, kivy==2.3.0, pyjnius, android, plyer, hostpython3==3.11.0, urllib3

# آپ کا پریمیم ہاتھ والا لوگو (جو آپ نے کراپ کیا تھا)
icon.filename = %(source.dir)s/icon.png

# لوڈنگ سکرین (اینیمیشن) کی سیٹنگز
android.presplash_lottie = %(source.dir)s/presplash.json
android.presplash_color = #FFFFFF

# سکرین کی سیٹنگز
orientation = portrait
fullscreen = 0

# تمام ضروری پرمیشنز
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# ⚠️ کریش سے بچنے کے لیے ضروری میٹا ڈیٹا اور تھیم
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version
android.entrypoint_theme = @style/Theme.AppCompat.NoActionBar

# اینڈرائیڈ بلڈ سیٹنگز (جدید ترین ای پی آئی کے مطابق)
android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
