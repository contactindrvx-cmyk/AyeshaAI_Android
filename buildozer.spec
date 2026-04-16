[app]
title = Alien AI
package.name = alienchat
package.domain = com.raza.alien
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp4
requirements = python3, kivy==2.3.0, pyjnius, android
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, ACCESS_NETWORK_STATE, SYSTEM_ALERT_WINDOW, GET_ACCOUNTS
android.api = 34
android.minapi = 24
android.add_src = java_src
android.archs = arm64-v8a
