import os
from kivy.app import App
from kivy.uix.webview import WebView
from kivy.core.window import Window

class AyeshaAI(App):
    def build(self):
        # ہگنگ فیس کا وہ یو آر ایل جو ہم نے پہلے استعمال کیا تھا
        # اسے 'WebView' کے ذریعے لوڈ کریں گے تاکہ کوئی ایرر نہ آئے
        url = "https://raza-ayesha-ai.hf.space" 
        webview = WebView(url=url, enable_javascript=True, enable_plugins=True)
        return webview

if __name__ == "__main__":
    AyeshaAI().run()
    
