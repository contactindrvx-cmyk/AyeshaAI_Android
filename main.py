import os, json, base64
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ مخصوص کلاسز لوڈ کرنا
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

    # 🔊 آواز کے لیے لسنر
    class TTSInitListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
        @java_method('(I)V')
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.callback()

    # 🔗 جاوا سکرپٹ سے ڈیٹا لینے والا ریسیور
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

class AlienAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = None
        self.tts_ready = False
        self.wv = None
        # ایپ کھلنے کے 2 سیکنڈ بعد پرمیشنز مانگے گا تاکہ کریش نہ ہو
        Clock.schedule_once(self.start_app_flow, 2)

    def show_toast(self, text):
        if platform == 'android':
            run_on_ui_thread(lambda: Toast.makeText(activity, text, Toast.LENGTH_SHORT).show())()

    def start_app_flow(self, dt):
        if platform == 'android':
            request_permissions([
                Permission.RECORD_AUDIO, 
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ], self.permissions_granted)
        else:
            self.load_webview()

    def permissions_granted(self, permissions, grants):
        # پرمیشن ملنے کے بعد ہارڈویئر اور ویب سائٹ لوڈ کریں
        self.init_tts()
        self.load_webview()

    def init_tts(self):
        try:
            self.tts = TextToSpeech(activity, TTSInitListener(self.on_tts_ready))
        except:
            print("TTS Initialization failed")

    def on_tts_ready(self):
        self.tts_ready = True
        self.tts.setLanguage(Locale("ur", "PK"))
        self.show_toast("عائشہ کا سپیکر تیار ہے!")

    @run_on_ui_thread
    def load_webview(self):
        self.wv = WebView(activity)
        settings = self.wv.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        self.wv.setWebChromeClient(WebChromeClient())
        
        # آپ کی ماسٹر ای میل کے ساتھ ہگنگ فیس کا لنک
        email = "alirazasabir007@gmail.com"
        self.wv.loadUrl(f"https://aigrowthbox-ayesha-ai.hf.space?email={email}")
        activity.setContentView(self.wv)
        
        # ہر آدھے سیکنڈ بعد چیک کرے گا کہ عائشہ نے کچھ بولا تو نہیں
        Clock.schedule_interval(self.check_commands, 0.5)

    @run_on_ui_thread
    def check_commands(self, dt):
        if self.wv:
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
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, "1")

    def open_gallery(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_file_selected)
        except:
            self.show_toast("گیلری کھولنے میں مسئلہ ہے")

    def on_file_selected(self, selection):
        if selection:
            try:
                with open(selection[0], "rb") as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                js = f"window.receiveImageFromAndroid('data:image/jpeg;base64,{img_data}')"
                run_on_ui_thread(lambda: self.wv.evaluateJavascript(js, None))()
            except:
                self.show_toast("تصویر لوڈ نہیں ہو سکی")

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
    
