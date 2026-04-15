[app]
title = Ayesha AI
package.name = ayeshaai
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml,mp4
version = 1.0.0
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,chardet,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, RECORD_AUDIO, CAMERA
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
