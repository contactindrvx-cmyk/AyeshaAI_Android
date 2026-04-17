import os, socket, json
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
    AccountManager = autoclass('android.accounts.AccountManager')
    WebView = autoclass('android.webkit.WebView')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    Context = autoclass('android.content.Context')
    Intent = autoclass('android.content.Intent')

    # 🔊 اصلی اینڈرائیڈ سپیکر اور ہارڈویئر کلاسز
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')
    Vibrator = autoclass('android.os.Vibrator')
    CameraManager = autoclass('android.hardware.camera2.CameraManager')

    WindowManager = autoclass('android.view.WindowManager')
    LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
    VideoView = autoclass('android.widget.VideoView')
    
    try: MyWebChromeClient = autoclass('org.alien.MyWebChromeClient')
    except: MyWebChromeClient = autoclass('android.webkit.WebChromeClient')

    # 🎤 سپیکر کو ریڈی کرنے کا لسنر
    class TTSInitListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
        def __init__(self):
            super().__init__()
            self.is_ready = False
        @java_method('(I)V')
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.is_ready = True

    # 🔗 جاوا سکرپٹ سے میسج پکڑنے والا ریسیور
    class JSReceiver(PythonJavaClass):
        __javainterfaces__ = ['android/webkit/ValueCallback']
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
        @java_method('(Ljava/lang/Object;)V')
        def onReceiveValue(self, value):
            if value and str(value) != 'null':
                try:
                    val = json.loads(str(value))
                    if val != "null": self.callback(val)
                except: pass
else:
    run_on_ui_thread = lambda x: x

class AlienAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = None
        self.camera_manager = None
        self.camera_id = None
        self.wv = None
        if platform == 'android':
            # کیمرہ اور آڈیو کی پرمیشن
            request_permissions([Permission.RECORD_AUDIO, Permission.GET_ACCOUNTS, Permission.CAMERA])
            self.init_hardware()
            Clock.schedule_once(self.start_app, 3)

    def init_hardware(self):
        try:
            self.tts_listener = TTSInitListener()
            self.tts = TextToSpeech(activity, self.tts_listener)
            self.camera_manager = activity.getSystemService(Context.CAMERA_SERVICE)
            self.camera_id = self.camera_manager.getCameraIdList()[0]
        except Exception as e:
            print("Hardware Init Error:", e)

    def start_app(self, dt):
        if platform == 'android' and Settings.canDrawOverlays(activity):
            self.show_bubble()
        self.load_webview()
        # ہر آدھے سیکنڈ بعد ویب سائٹ سے کمانڈز پکڑے گا
        if platform == 'android':
            Clock.schedule_interval(self.poll_js_queue, 0.5)

    def show_bubble(self):
        try:
            params = LayoutParams(350, 350, LayoutParams.TYPE_APPLICATION_OVERLAY, 8, -3)
            wm = activity.getSystemService(Context.WINDOW_SERVICE)
            vv = VideoView(activity)
            path = os.path.join(os.path.dirname(__file__), "presplash.mp4")
            vv.setVideoURI(Uri.parse("file://" + path))
            vv.setOnPreparedListener(autoclass('android.media.MediaPlayer$OnPreparedListener')({'onPrepared': lambda mp: mp.setLooping(True)}))
            vv.start()
            wm.addView(vv, params)
        except: pass

    @run_on_ui_thread
    def load_webview(self):
        am = AccountManager.get(activity)
        accs = am.getAccountsByType('com.google')
        email = accs[0].name if accs else "guest@alien.ai"
        self.wv = WebView(activity)
        self.wv.getSettings().setJavaScriptEnabled(True)
        self.wv.getSettings().setDomStorageEnabled(True) 
        self.wv.setWebChromeClient(MyWebChromeClient())
        self.wv.loadUrl(f'https://aigrowthbox-ayesha-ai.hf.space?email={email}')
        activity.setContentView(self.wv)

    @run_on_ui_thread
    def poll_js_queue(self, dt):
        if self.wv:
            self.wv.evaluateJavascript("typeof getPendingAlienCommands === 'function' ? getPendingAlienCommands() : 'null'", JSReceiver(self.handle_js_commands))

    def handle_js_commands(self, data):
        cmds = data.split("###")
        for cmd_str in cmds:
            if cmd_str.startswith("SPEAK|||"):
                text = cmd_str.split("|||")[1]
                self.speak_text(text)
            elif cmd_str.startswith("CMD|||"):
                cmd = cmd_str.split("|||")[1]
                self.execute_command(cmd)

    def speak_text(self, text):
        if self.tts and self.tts_listener.is_ready:
            loc = Locale("ur", "PK")
            self.tts.setLanguage(loc)
            # پرانی آواز بند کر کے نئی شروع کرے گا
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)

    def execute_command(self, cmd):
        print("Executing Command:", cmd)
        try:
            if cmd == "CMD_FLASHLIGHT_ON" and self.camera_manager and self.camera_id:
                self.camera_manager.setTorchMode(self.camera_id, True)
            elif cmd == "CMD_FLASHLIGHT_OFF" and self.camera_manager and self.camera_id:
                self.camera_manager.setTorchMode(self.camera_id, False)
            elif cmd == "CMD_VIBRATE":
                vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                if vibrator and vibrator.hasVibrator():
                    vibrator.vibrate(500)
            elif cmd.startswith("CMD_YOUTUBE_SEARCH"):
                query = cmd.replace("CMD_YOUTUBE_SEARCH", "").strip()
                intent = Intent(Intent.ACTION_SEARCH)
                intent.setPackage("com.google.android.youtube")
                intent.putExtra("query", query)
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                activity.startActivity(intent)
            elif cmd == "CMD_WHATSAPP_MSG":
                intent = Intent(Intent.ACTION_MAIN)
                intent.setAction(Intent.ACTION_SEND)
                intent.setType("text/plain")
                intent.setPackage("com.whatsapp")
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                activity.startActivity(intent)
        except Exception as e:
            print("Command Error:", e)

class AlienAIChat(App):
    def build(self): return AlienAppBase()

if __name__ == '__main__': AlienAIChat().run()
                   
