import os
import sqlite3
import socket
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ گرافکس اور کریش فکس
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    # اینڈرائیڈ کلاسز
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
else:
    run_on_ui_thread = lambda x: x

class AlienAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. لوکل میموری (SQLite) سیٹ اپ
        self.setup_local_memory()
        
        # 2. فلوٹنگ ببل (Overlay) پرمیشن چیک - 1 سیکنڈ ڈیلے کے ساتھ
        if platform == 'android':
            Clock.schedule_once(self.check_overlay_permission, 1)
        
        # 3. عائشہ کا دماغ (Hugging Face Interface) - 2 سیکنڈ ڈیلے کے ساتھ
        Clock.schedule_once(self.start_alien_brain, 2)

    def setup_local_memory(self):
        try:
            self.conn = sqlite3.connect('alien_local_memory.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (key TEXT PRIMARY KEY, value TEXT)''')
            self.conn.commit()
            print("[Alien AI] Local Memory Ready!")
        except Exception as e:
            print(f"Memory Error: {e}")

    def check_overlay_permission(self, dt):
        if platform == 'android':
            if not Settings.canDrawOverlays(activity):
                intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
                intent.setData(Uri.parse("package:" + activity.getPackageName()))
                activity.startActivity(intent)
            else:
                self.setup_floating_bubble()

    def setup_floating_bubble(self):
        # presplash.mp4 کو ببل کے ساتھ جوڑنے کا فنکشن
        print("[Alien AI] Bubble Permission Granted. Ready for presplash.mp4 overlay.")

    def start_alien_brain(self, dt):
        # 4. آف لائن انٹیلیجنس چیک
        if self.check_internet():
            self.create_webview()
        else:
            msg = "Raza Bhai, Alien AI ka internet se raabta toot gaya hai.\nSabar karein..."
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
            
            # عائشہ کا کلین انٹرفیس لنک
            webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            
            activity.setContentView(webview)

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
    
