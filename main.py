import os, json, base64
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.label import Label
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
        
        # ایک سادہ ٹیکسٹ دکھائیں تاکہ پتا چلے ایپ زندہ ہے
        self.add_widget(Label(text="Alien AI Loading...", pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        # 2 سیکنڈ کا انتظار تاکہ سسٹم سیٹ ہو جائے
        Clock.schedule_once(self.check_permissions, 2)

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
            self.show_toast("پرمیشنز مل گئیں۔ اب لوڈ کر رہے ہیں...")
            Clock.schedule_once(self.start_everything, 1)
        else:
            self.show_toast("ایپ کو تمام پرمیشنز کی ضرورت ہے!")

    def start_everything(self, dt=None):
        # 1. پہلے ٹیکسٹ ٹو سپیچ (TTS) لوڈ کریں
        self.init_tts()
        
        # 2. پھر ویڈیو ببل لوڈ کریں (صرف اگر فائل موجود ہو)
        if os.path.exists('preview.mp4'):
            try:
                self.bubble = Video(source='preview.mp4', state='pause', options={'eos': 'loop'})
                self.bubble.size_hint = (None, None)
                self.bubble.size = (200, 200)
                self.bubble.pos_hint = {'right': 0.95, 'top': 0.95}
                self.add_widget(self.bubble)
            except Exception as e:
                print(f"Video Error: {e}")
        
        # 3. آخر میں ویب ویو لوڈ کریں
        Clock.schedule_once(self.load_webview, 1)

    def init_tts(self):
        # (پرانا TTS لاجک یہاں محفوظ ہے)
        if platform == 'android':
            try:
                self.tts = TextToSpeech(activity, None) 
                # نوٹ: لسنر کو سادہ رکھا ہے تاکہ کریش نہ ہو
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
            
            # ویب ویو کو سکرین پر ایڈ کریں
            activity.addContentView(self.wv, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
            
            # ویب ویو کے آنے کے بعد ببل کو دوبارہ اوپر لانے کی کوشش
            if self.bubble:
                self.bubble.parent.remove_widget(self.bubble)
                self.add_widget(self.bubble)
                
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
    
