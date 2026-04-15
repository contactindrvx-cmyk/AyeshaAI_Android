[app]
# (ایپ کی بنیادی معلومات)
title = Ayesha AI
package.name = ayesha.ai.assistant
package.domain = okara.punjab

# (فائلیں اور آئیکن)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml,mp4
icon.filename = icon.png
# لوڈنگ اسکرین کے لیے ویڈیو
presplash.filename = presplash.mp4

# (ورژن)
version = 1.0.0

# (پرمیشنز)
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE

# (اینڈرائیڈ سیٹنگز)
android.api = 33
android.minapi = 21
android.fullscreen = 1

# (لائبریریاں)
requirements = python3,kivy

[buildozer]
log_level = 2
warn_on_root = 1
