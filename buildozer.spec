[app]
# (str) Title of your application
title = Ayesha AI

# (str) Package name
package.name = ayeshaai

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,xml,mp4

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# یہاں ہم نے وہی لائبریریاں رکھی ہیں جو آپ کے کوڈ کے لیے ضروری ہیں
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,chardet,idna

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, CAMERA

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version to use
android.build_tools_version = 31.0.0

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any build tools issues.
android.accept_sdk_license = True

# (list) Architecture to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
