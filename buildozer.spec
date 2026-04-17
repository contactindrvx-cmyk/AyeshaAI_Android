[app]

# (str) Title of your application
title = Alien AI Chat

# (str) Package name
package.name = alienchat

# (str) Package domain (needed for android/ios packaging)
package.domain = com.raza.alien

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (اس میں mp4 لازمی ہے)
source.include_exts = py,png,jpg,kv,atlas,mp4

# (str) Application versioning (یہ وہ لائن ہے جس کا ایرر آ رہا تھا)
version = 1.0

# (list) Application requirements
requirements = python3, kivy==2.3.0, pyjnius, android

# (str) Presplash and Icon
presplash.filename = %(source.dir)s/icon.png
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Fullscreen or not
fullscreen = 0

# (list) Permissions (مائیک، ببل اور اکاؤنٹ کے لیے)
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, SYSTEM_ALERT_WINDOW, GET_ACCOUNTS

# (int) Target Android API
android.api = 34

# (int) Minimum API
android.minapi = 24

# (int) Android SDK and NDK
android.sdk = 34
android.ndk = 25b

# (str) Java source folder (مائیک الرٹ ختم کرنے کے لیے)
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
