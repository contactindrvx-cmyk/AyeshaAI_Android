# --- عائشہ AI اینڈرائیڈ ایپ (Kivy WebView) ---
import kivy
from kivy.app import App
from kivy.uix.webview import WebView
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import os

# ہگنگ فیس پر آپ کی عائشہ کا ڈائریکٹ لنک
# یہاں اپنا صحیح لنک لکھیں (مثلاً https://huggingface.co/spaces/YOUR_USER_NAME/YOUR_SPACE_NAME)
AYESHA_HF_LINK = "https://huggingface.co/spaces/YOUR_USER_NAME/YOUR_SPACE_NAME"

class AyeshaApp(App):
    def build(self):
        # ایپ کا ٹائٹل اور آئیکن
        self.title = "Ayesha AI"
        self.icon = "icon.png"
        
        # ونڈو کو فل اسکرین کریں (No Header)
        Window.fullscreen = 'auto'
        Window.clearcolor = (0.04, 0.05, 0.07, 1) # گہرا کالا رنگ

        # مین لے آؤٹ
        self.layout = FloatLayout()

        # ویب ویو کنٹینر
        # یہ عائشہ کو لوڈ کرے گا اور اس کا ڈیزائن ویسا ہی رکھے گا جیسا آپ نے بنایا ہے
        self.webview = WebView(url=AYESHA_HF_LINK)
        self.layout.add_widget(self.webview)

        return self.layout

    def on_start(self):
        # ایپ شروع ہوتے ہی کچھ ایکسٹرا پرمیشنز چیک کریں
        print("Ayesha AI is starting...")

    def on_pause(self):
        # جب ایپ بیک گراؤنڈ میں جائے تو آواز بند نہ ہو (Foreground Service)
        return True

    def on_resume(self):
        # جب ایپ دوبارہ کھلے تو ویب ویو کو ریفریش کریں
        pass

if __name__ == '__main__':
    AyeshaApp().run()
  
