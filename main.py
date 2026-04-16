import os
import sqlite3
import socket
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ گرافکس فکس (کریش روکنے کے لیے)
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    run_on_ui_thread = lambda x: x

class AyeshaAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # فیچر 2: لوکل میموری کی تجوری تیار کرنا
        self.setup_local_memory()
        
        # کریش روکنے کا کمال: 1 سیکنڈ کا انتظار تاکہ ایپ سیٹل ہو جائے
        Clock.schedule_once(self.start_ayesha_brain, 1)

    def setup_local_memory(self):
        # یہ SQLite آپ کے موبائل میں یوزر کا ڈیٹا سیو کرے گی
        try:
            self.conn = sqlite3.connect('ayesha_local_memory.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS memory (data_key TEXT PRIMARY KEY, data_value TEXT)''')
            self.conn.commit()
            print("[Ayesha Memory] Database Ready!")
        except Exception as e:
            pass

    def start_ayesha_brain(self, dt):
        # فیچر 4: آف لائن انٹیلیجنس اور انٹرنیٹ چیک
        if self.check_internet():
            self.create_webview()
        else:
            # انٹرنیٹ نہ ہونے پر رومن اردو کا پیار بھرا پیغام (تاکہ فونٹ کا کریش نہ آئے)
            msg = "Raza Bhai, Mera internet se raabta toot gaya hai.\nAyesha is waiting for signals..."
            lbl = Label(text=msg, halign="center", font_size="18sp")
            self.add_widget(lbl)

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    @run_on_ui_thread
    def create_webview(self):
        if platform == 'android':
            webview = WebView(activity)
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setMediaPlaybackRequiresUserGesture(False)
            
            webview.setWebViewClient(WebViewClient())
            webview.setWebChromeClient(WebChromeClient())
            
            # فیچر 1: کلین انٹرفیس (فالتو ہیڈر غائب کرنے والا ڈائریکٹ لنک)
            webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            
            activity.setContentView(webview)

class AlianAI(App):
    def build(self):
        return AyeshaAppBase()

if __name__ == '__main__':
    AlianAI().run()
