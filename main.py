import os, json, base64
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    from android.permissions import request_permissions, Permission
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    WebView = autoclass('android.webkit.WebView')
    # گیلری کے لیے ویب کلائنٹ
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    
    Toast = autoclass('android.widget.Toast')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')
    Context = autoclass('android.content.Context')

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
                # جاوا سکرپٹ سے آنے والے ڈیٹا کو صاف کرنا
                val = str(value).strip('"').replace('\\\\', '\\').replace('\\"', '"')
                if val and val != "null":
                    self.callback(val)
else:
    run_on_ui_thread = lambda x: x

class AlienAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = None
        self.tts_ready = False
        self.wv = None
        if platform == 'android':
            # تمام ضروری پرمیشنز
            request_permissions([
                Permission.RECORD_AUDIO, 
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            self.tts = TextToSpeech(activity, TTSInitListener(self.on_tts_ready))
            Clock.schedule_once(self.load_webview, 2)

    def on_tts_ready(self):
        self.tts_ready = True
        self.tts.setLanguage(Locale("ur", "PK"))
        self.show_toast("عائشہ کا سپیکر تیار ہے!")

    def show_toast(self, text):
        run_on_ui_thread(lambda: Toast.makeText(activity, text, Toast.LENGTH_SHORT).show())()

    @run_on_ui_thread
    def load_webview(self, dt=0):
        self.wv = WebView(activity)
        settings = self.wv.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setDatabaseEnabled(True)
        
        # پلس (+) بٹن (گیلری) چلانے کے لیے یہ لائن ضروری ہے
        self.wv.setWebChromeClient(WebChromeClient())
        
        # آپ کی ماسٹر ای میل اور ہگنگ فیس کا لنک
        email = "alirazasabir007@gmail.com" 
        self.wv.loadUrl(f'https://aigrowthbox-ayesha-ai.hf.space?email={email}')
        activity.setContentView(self.wv)
        
        # ہر 0.5 سیکنڈ بعد ویب سائٹ سے کمانڈز (آواز یا گیلری) پوچھے گا
        Clock.schedule_interval(self.poll_commands, 0.5)

    @run_on_ui_thread
    def poll_commands(self, dt):
        if self.wv:
            self.wv.evaluateJavascript("getPendingAlienCommands()", JSReceiver(self.handle_commands))

    def handle_commands(self, data):
        if not data or data == "null": return
        
        commands = data.split("###")
        for cmd in commands:
            if "SPEAK|||" in cmd:
                text_to_speak = cmd.split("|||")[1]
                self.speak_now(text_to_speak)
            elif "CMD|||CMD_OPEN_GALLERY" in cmd:
                self.open_device_gallery()

    def speak_now(self, text):
        if self.tts and self.tts_ready:
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, "1")
        else:
            self.show_toast("سپیکر ابھی گرم ہو رہا ہے...")

    def open_device_gallery(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.on_image_selected)
        except Exception as e:
            self.show_toast("گیلری نہیں کھل سکی")

    def on_image_selected(self, selection):
        if selection:
            filepath = selection[0]
            try:
                with open(filepath, "rb") as f:
                    data = base64.b64encode(f.read()).decode('utf-8')
                
                # تصویر کو واپس چیٹ باکس میں بھیجنا
                js_code = f"window.receiveImageFromAndroid('data:image/jpeg;base64,{data}')"
                run_on_ui_thread(lambda: self.wv.evaluateJavascript(js_code, None))()
                self.show_toast("تصویر منتخب ہو گئی!")
            except:
                self.show_toast("تصویر لوڈ کرنے میں خرابی")

class AlienAIChat(App):
    def build(self): return AlienAppBase()

if __name__ == '__main__': AlienAIChat().run()
    
