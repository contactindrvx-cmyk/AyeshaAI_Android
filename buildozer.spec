[app]
# (str) Title of your application
title = Alien AI Chat and Assistant

# (str) Package name
package.name = alienchat

# (str) Package domain
package.domain = com.raza.alien

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,mp4

# (str) Application versioning
version = 1.0

# 🚀 (list) Application requirements
# یہاں plyer اور hostpython کے ورژن فکس کر دیے ہیں تاکہ کریش نہ ہو
requirements = python3, kivy==2.3.0, pyjnius, android, plyer, hostpython3==3.11.0

# (str) Presplash and Icon
presplash.filename = %(source.dir)s/icon.png
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Fullscreen or not
fullscreen = 0

# 🔒 (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, SYSTEM_ALERT_WINDOW, GET_ACCOUNTS, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# 📱 (int) Target Android API
# 33 سب سے زیادہ سٹیبل ہے کریشز روکنے کے لیے
android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b

# *** لائسنس کی منظوری ***
android.accept_sdk_license = True

# (str) Java source folder
android.add_src = java_src

# (bool) Enable AndroidX
android.enable_androidx = True

# (list) Android architectures
android.archs = arm64-v8a

[buildozer]
# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if run as root
warn_on_root = 1
