[app]
title = Ayesha AI
package.name = ayeshaai
package.domain = com.raza.ayesha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# آپ کا آئکن
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

# لائبریریز (اب صرف بنیادی چیزیں اور pyjnius چاہیے)
requirements = python3, kivy==2.3.0, pyjnius, android

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

# مائیک اور انٹرنیٹ کی پرمیشن
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS

# اینڈرائیڈ 16 کی سٹیبل سیٹنگز
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b

android.enable_androidx = True
android.accept_sdk_license = True
# یاد رہے کہ android.entrypoint ہم نے نہیں لکھنا

[buildozer]
log_level = 2
warn_on_root = 1
