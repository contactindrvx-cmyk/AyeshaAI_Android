import os, json, base64
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ کی لائبریریز
if platform == 'android':
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
    # WebView کو Kivy کے اوپر دکھانے کے لیے LayoutParams درکار ہیں
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

    class TTSInitListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
        @java_method('(I)V')
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.callback()

    class JSReceiver(PythonJavaClass):
        __javainterfaces__ = ['android/webkit/ValueCallback']
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
        @java_method('(Ljava/lang/Object;)V')
        def onReceiveValue(self, value):
            if value and str(value) != 'null':
                val = str(value).strip('"').replace('\\\\', '\\').replace('\\"', '"')
                if val and val != "null":
                    self.callback(val)

# 🎥 آپ کا فلوٹنگ ویڈیو ببل کلاس
class FloatingVideoBubble(ButtonBehavior, Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'preview.mp4'  # آپ کی ویڈیو فائل
        self.state = 'pause'         # شروع میں رکا رہے گا
        self.options = {'eos': 'loop'} # بار بار چلے گا جب تک پلے ہے
        self.size_hint = (None, None)
        self.size = (180, 180)       # ببل کا سائز
        self.pos_hint = {'right': 0.95, 'top': 0.95} # سکرین پر جگہ

    # ببل پر ٹچ کرنے پر
    def on_release(self):
        if self.state == 'play':
            self.state = 'pause'
        else:
            self.state = 'play'

# 🚀 مین لے آؤٹ اور ایپ فلو
class AlienAppBase(FloatLayout): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = None
        self.tts_ready = False
        self.wv = None
        
        # ببل کو سکرین پر ایڈ کیا
        self.bubble = FloatingVideoBubble()
        self.add_widget(self.bubble)

        # 1.5 سیکنڈ کے ڈیلے کے بعد پرمیشن مانگے گا تاکہ کریش نہ ہو
        Clock.schedule_once(self.start_app_flow, 1.5)

    def show_toast(self, text):
        if platform == 'android':
            run_on_ui_thread(lambda: Toast.makeText(activity, text, Toast.LENGTH_SHORT).show())()

    def start_app_flow(self, dt):
        if platform == 'android':
            # یہاں SYSTEM_ALERT_WINDOW نہیں ڈالا تاکہ ایپ کریش نہ ہو
            permissions = [
                Permission.RECORD_AUDIO, 
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ]
            request_permissions(permissions, self.permissions_granted)
        else:
            self.init_tts()
            self.load_webview()

    def permissions_granted(self, permissions, grants):
        # پرمیشن ملنے کے بعد آرام سے ہارڈویئر لوڈ کرے گا
        if all(grants):
            self.show_toast("عائشہ ایکٹیویٹ ہو رہی ہے...")
            Clock.schedule_once(lambda dt: self.init_tts(), 0.5)
            Clock.schedule_once(lambda dt: self.load_webview(), 1.0)
            Clock.schedule_interval(self.trigger_js_check, 0.5)
        else:
            self.show_toast("مائیک اور کیمرے کی پرمیشن لازمی ہے!")

    def init_tts(self):
        if platform == 'android':
            try:
                self.tts = TextToSpeech(activity, TTSInitListener(self.on_tts_ready))
            except Exception as e:
                print("TTS Error:", e)

    def on_tts_ready(self):
        self.tts_ready = True
        self.tts.setLanguage(Locale("ur", "PK"))

    @run_on_ui_thread
    def load_webview(self):
        try:
            self.wv = WebView(activity)
            settings = self.wv.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setMediaPlaybackRequiresUserGesture(False) 
            
            self.wv.setWebChromeClient(WebChromeClient())
            email = "alirazasabir007@gmail.com"
            self.wv.loadUrl(f"https://aigrowthbox-ayesha-ai.hf.space?email={email}")
            
            # ہم addContentView استعمال کر رہے ہیں تاکہ ببل بھی نظر آئے اور ویب سائٹ بھی
            activity.addContentView(self.wv, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
        except Exception as e:
            print("WebView Error:", e)

    def trigger_js_check(self, dt):
        if self.wv and platform == 'android':
            run_on_ui_thread(self.execute_js_check)()

    def execute_js_check(self):
        self.wv.evaluateJavascript("getPendingAlienCommands()", JSReceiver(self.handle_js_data))

    def handle_js_data(self, data):
        if not data or data == "null": return
        parts = data.split("###")
        for p in parts:
            if "SPEAK|||" in p:
                text = p.split("|||")[1]
                self.speak_text(text)
            elif "CMD|||CMD_OPEN_GALLERY" in p:
                self.open_gallery()

    def speak_text(self, text):
        if self.tts and self.tts_ready:
            # عائشہ بولے گی تو ببل اینیمیٹ ہوگا
            self.bubble.state = 'play'
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, "1")
            
            # بولنے کی لمبائی کے حساب سے ٹائمر جو ببل کو روکے گا
            duration = len(text) * 0.12 
            Clock.schedule_once(self.stop_bubble_animation, duration)

    def stop_bubble_animation(self, dt):
        self.bubble.state = 'pause'

    def open_gallery(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_file_selected)
        except Exception:
            self.show_toast("گیلری کا ایرر")

    def on_file_selected(self, selection):
        if selection:
            try:
                with open(selection[0], "rb") as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                js = f"window.receiveImageFromAndroid('data:image/jpeg;base64,{img_data}')"
                run_on_ui_thread(lambda: self.wv.evaluateJavascript(js, None))()
            except Exception:
                self.show_toast("تصویر کا ایرر")

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
        
