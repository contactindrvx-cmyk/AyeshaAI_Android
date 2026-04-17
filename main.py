import os, json, base64, sys, traceback
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ کی مخصوص لائبریریز کا سیٹ اپ
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
        self.is_started = False
        
        # 1. ایرر دکھانے والا لیبل (اگر کچھ خراب ہوا تو یہ بتائے گا)
        self.error_label = Label(
            text="", 
            color=(1, 0, 0, 1), 
            halign="center", 
            font_size='14sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        self.add_widget(self.error_label)

        # 2. ایپ کا لوگو (icon.png) دکھائیں
        self.logo = Image(
            source='icon.png', 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, 
            size_hint=(0.5, 0.5)
        )
        self.add_widget(self.logo)

        # 1.5 سیکنڈ بعد پرمیشن کا عمل شروع کریں
        Clock.schedule_once(self.check_permissions, 1.5)
        
        # اگر 5 سیکنڈ تک کچھ نہ ہوا تو زبردستی ایپ چلانے کی کوشش کریں
        Clock.schedule_once(self.force_start, 5.0)

    def show_error_on_screen(self, error_text):
        """اگر ایپ میں کوئی ایرر آئے تو اسے سکرین پر دکھانے کے لیے"""
        self.error_label.text = f"ALIEN ERROR:\n{error_text}"

    def check_permissions(self, dt):
        try:
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
        except Exception as e:
            self.show_error_on_screen(f"Permission Crash: {str(e)}")

    def on_permissions_result(self, permissions, grants):
        # پرمیشن ملنے کے بعد اگلا مرحلہ
        self.start_everything()

    def force_start(self, dt):
        # اگر ایپ ابھی تک لوگو پر فریز ہے تو اسے دھکا دیں
        if not self.is_started:
            self.start_everything()

    def start_everything(self, dt=None):
        if self.is_started: return
        self.is_started = True
        
        # لوگو ہٹا دیں
        if self.logo in self.children:
            self.remove_widget(self.logo)

        try:
            self.init_tts()
            self.load_webview()
            # فلوٹنگ ببل کو تھوڑا سا ٹھہر کر لوڈ کریں
            Clock.schedule_once(self.load_bubble, 2.5)
        except Exception as e:
            self.show_error_on_screen(f"Start Error: {str(e)}")

    def load_bubble(self, dt):
        """فلوٹنگ ویڈیو ببل کو لوڈ کرنا"""
        if os.path.exists('preview.mp4'):
            try:
                self.bubble = Video(source='preview.mp4', state='pause', options={'eos': 'loop'})
                self.bubble.size_hint = (None, None)
                self.bubble.size = (200, 200)
                self.bubble.pos_hint = {'right': 0.95, 'top': 0.95}
                self.add_widget(self.bubble)
            except Exception as e:
                print(f"Video Error: {e}")

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
            # عائشہ کا ہگنگ فیس سرور لنک
            self.wv.loadUrl(f"https://aigrowthbox-ayesha-ai.hf.space?email={email}")
            
            # ویب ویو کو اینڈرائیڈ ویو میں ایڈ کرنا
            activity.addContentView(self.wv, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
            
            # ہر 1 سیکنڈ بعد ویب سائٹ سے کمانڈز چیک کریں
            Clock.schedule_interval(self.check_commands, 1)
        except Exception as e:
            # اگر ویب ویو لوڈ نہ ہو سکے تو سکرین پر ایرر آئے گا
            self.show_error_on_screen(f"WebView Error: {str(e)}")

    def check_commands(self, dt):
        if self.wv and platform == 'android':
            run_on_ui_thread(lambda: self.wv.evaluateJavascript("getPendingAlienCommands()", None))()

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
    
