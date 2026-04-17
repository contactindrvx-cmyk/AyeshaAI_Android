[app]
title = Alien AI Chat and Assistant
package.name = alienchat
package.domain = com.raza.alien
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp4,json
version = 1.0

requirements = python3, kivy==2.3.0, pyjnius, android, plyer, hostpython3==3.11.0, urllib3

icon.filename = %(source.dir)s/icon.png
android.presplash_lottie = %(source.dir)s/presplash.json
android.presplash_color = #FFFFFF

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

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
