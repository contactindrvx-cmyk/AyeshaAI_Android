[app]
title = Ayesha AI
package.name = ayesha.ai.assistant
package.domain = okara.punjab
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml,mp4
icon.filename = icon.png
presplash.filename = presplash.mp4
version = 1.0.0
requirements = python3,kivy

# --- ورژن فکس کرنے کا اہم حصہ ---
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.build_tools_version = 31.0.0
android.accept_sdk_license = True
android.fullscreen = 1
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
