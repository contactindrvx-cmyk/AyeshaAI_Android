import os, json, base64
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
        from android.permissions import request_permissions, Permission
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        WebView = autoclass('android.webkit.WebView')
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
        
        # 1. لوگو دکھائیں (Alien AI Loading کی جگہ)
        self.logo = Image(source='icon.png', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.5, 0.5))
        self.add_widget(self.logo)

        # 1.5 سیکنڈ بعد پرمیشن مانگیں
        Clock.schedule_once(self.check_permissions, 1.5)

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
        if all(grants):
            self.show_toast("Permissions Granted. Starting Ayesha...")
            Clock.schedule_once(self.start_everything, 1)
        else:
            self.show_toast("Permissions Required to run!")

    def start_everything(self, dt=None):
        # پرمیشن ملنے کے بعد لوگو غائب کریں
        if self.logo in self.children:
            self.remove_widget(self.logo)

        self.init_tts()
        # پہلے ویب ویو لوڈ کریں
        self.load_webview()
        
        # اور 2 سیکنڈ بعد آرام سے ببل لائیں تاکہ کریش نہ ہو
        Clock.schedule_once(self.load_bubble, 2.5)

    def load_bubble(self, dt):
        if os.path.exists('preview.mp4'):
            try:
                self.bubble = Video(source='preview.mp4', state='pause', options={'eos': 'loop'})
                self.bubble.size_hint = (None, None)
                self.bubble.size = (200, 200)
                self.bubble.pos_hint = {'right': 0.95, 'top': 0.95}
                self.add_widget(self.bubble)
            except Exception as e:
                print(f"Video Bubble Error: {e}")

    def init_tts(self):
        if platform == 'android':
            try:
                self.tts = TextToSpeech(activity, None) 
            except: pass

    @run_on_ui_thread
    def load_webview(self, dt=None):
        try:
            self.wv = WebView(activity)
            self.wv.getSettings().setJavaScriptEnabled(True)
            self.wv.getSettings().setDomStorageEnabled(True)
            self.wv.setWebChromeClient(WebChromeClient())
            
            email = "alirazasabir007@gmail.com"
            self.wv.loadUrl(f"https://aigrowthbox-ayesha-ai.hf.space?email={email}")
            
            activity.addContentView(self.wv, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
            
            Clock.schedule_interval(self.check_commands, 1)
        except Exception as e:
            self.show_toast(f"WebView Error: {e}")

    def check_commands(self, dt):
        if self.wv and platform == 'android':
            run_on_ui_thread(lambda: self.wv.evaluateJavascript("getPendingAlienCommands()", None))()

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
    
