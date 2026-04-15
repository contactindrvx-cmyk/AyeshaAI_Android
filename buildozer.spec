[app]
title = Ayesha AI
package.name = ayesha.ai.assistant
package.domain = okara.punjab
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml,mp4
icon.filename = icon.png
# presplash کو فی الحال ہٹا دیتے ہیں تاکہ بلڈ ہلکی ہو اور کامیاب ہو جائے
# presplash.filename = presplash.mp4
version = 1.0.0

# صرف ضروری چیزیں رکھیں تاکہ سسٹم کنفیوز نہ ہو
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,chardet,idna

android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.build_tools_version = 31.0.0
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
