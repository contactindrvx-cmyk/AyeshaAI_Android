import os, json, base64
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ کی مخصوص لائبریریز
if platform == 'android':
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
        from android.permissions import request_permissions, Permission
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient') # نیا اضافہ
        WebChromeClient = autoclass('android.webkit.WebChromeClient')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        Locale = autoclass('java.util.Locale')
        Toast = autoclass('android.widget.Toast')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    except Exception as e:
        print(f"Android imports failed: {e}")

class AlienAppBase(FloatLayout): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = None
        self.wv = None
        self.bubble = None
        self.is_started = False
        
        # 1. لوگو دکھائیں
        self.logo = Image(source='icon.png', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.5, 0.5))
        self.add_widget(self.logo)

        # 1 سیکنڈ بعد پرمیشن کا عمل شروع کریں
        Clock.schedule_once(self.check_permissions, 1.0)
        
        # بائی پاس: اگر 5 سیکنڈ تک کچھ نہ ہوا تو زبردستی ایپ چلائیں
        Clock.schedule_once(self.force_start, 5.0)

    def show_toast(self, text):
        if platform == 'android':
            run_on_ui_thread(lambda: Toast.makeText(activity, text, Toast.LENGTH_SHORT).show())()

    def check_permissions(self, dt):
        if platform == 'android':
            permissions = [
                Permission.RECORD_AUDIO, 
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE
            ]
            request_permissions(permissions, self.on_permissions_result)
        else:
            self.start_everything()

    def on_permissions_result(self, permissions, grants):
        self.start_everything()

    def force_start(self, dt):
        if not self.is_started:
            self.start_everything()

    def start_everything(self, dt=None):
        if self.is_started: return
        self.is_started = True
        
        # لوگو ہٹا دیں
        if self.logo in self.children:
            self.remove_widget(self.logo)

        self.init_tts()
        self.load_webview()
        # ببل کو لوڈ ہونے دیں
        Clock.schedule_once(self.load_bubble, 3.0)

    def load_bubble(self, dt):
        if os.path.exists('preview.mp4'):
            try:
                self.bubble = Video(source='preview.mp4', state='pause', options={'eos': 'loop'})
                self.bubble.size_hint = (None, None)
                self.bubble.size = (200, 200)
                self.bubble.pos_hint = {'right': 0.95, 'top': 0.95}
                self.add_widget(self.bubble)
            except: pass

    def init_tts(self):
        if platform == 'android':
            try: self.tts = TextToSpeech(activity, None) 
            except: pass

    @run_on_ui_thread
    def load_webview(self, dt=None):
        try:
            self.wv = WebView(activity)
            settings = self.wv.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True) # ہگنگ فیس کے لیے ضروری
            settings.setDatabaseEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setMixedContentMode(0) # 0 = ALWAYS_ALLOW
            
            # زبردستی ایپ کے اندر ہی لنک کھولنے کے لیے
            self.wv.setWebViewClient(WebViewClient())
            self.wv.setWebChromeClient(WebChromeClient())
            
            email = "alirazasabir007@gmail.com"
            url = f"https://aigrowthbox-ayesha-ai.hf.space?email={email}"
            self.wv.loadUrl(url)
            
            # ویب ویو کو سکرین پر دکھائیں
            activity.addContentView(self.wv, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
            
            # اگر ببل پہلے لوڈ ہو گیا تھا تو اسے اوپر لے آئیں
            if self.bubble:
                self.bubble.parent.remove_widget(self.bubble)
                self.add_widget(self.bubble)
                
            Clock.schedule_interval(self.check_commands, 1)
        except Exception as e:
            self.show_toast(f"Loading Error: {str(e)}")

    def check_commands(self, dt):
        if self.wv and platform == 'android':
            run_on_ui_thread(lambda: self.wv.evaluateJavascript("getPendingAlienCommands()", None))()

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
    
