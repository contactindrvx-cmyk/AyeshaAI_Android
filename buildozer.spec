[app]
title = Alien AI Chat and Assistant
package.name = alienchat
package.domain = com.raza.alien
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp4
version = 1.0

# سیف موڈ Requirements
requirements = python3, kivy==2.3.0, pyjnius, android, plyer, hostpython3==3.11.0, urllib3

presplash.filename = %(source.dir)s/icon.png
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, GET_ACCOUNTS, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True
android.add_src = java_src
android.enable_androidx = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
