[app]
title = Ayesha AI
package.name = ayeshaai
package.domain = com.raza.ayesha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

requirements = python3, kivy==2.3.0, pyjnius, android

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

# آف لائن انٹیلیجنس کے لیے پرمیشنز
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE

android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b

android.enable_androidx = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
