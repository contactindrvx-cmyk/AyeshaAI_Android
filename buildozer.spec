[app]

# (str) Title of your application (اینڈ والا مسئلہ فکسڈ ہے)
title = Alien AI Chat and Assistant

# (str) Package name
package.name = alienchat

# (str) Package domain (needed for android/ios packaging)
package.domain = com.raza.alien

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (اس میں mp4 لازمی ہے)
source.include_exts = py,png,jpg,kv,atlas,mp4

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3, kivy==2.3.0, pyjnius, android

# (str) Presplash of the application (لوڈنگ سکرین پر آپ کا لوگو)
presplash.filename = %(source.dir)s/icon.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations (landscape, sensorPortrait, etc.)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, SYSTEM_ALERT_WINDOW

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) App theme, default is ok for Kivy-based app
android.apptheme = "@android:style/Theme.NoTitleBar"

# *** یہ سب سے اہم لائن ہے جو جاوا فولڈر کو جوڑے گی ***
android.add_src = java_src

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
