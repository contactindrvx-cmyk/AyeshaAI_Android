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
    Toast = autoclass('android.widget.Toast')

    # 🔊 اصلی گوگل ٹی ٹی ایس (جیمنائی والا سسٹم)
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')
    Vibrator = autoclass('android.os.Vibrator')
    CameraManager = autoclass('android.hardware.camera2.CameraManager')

    WindowManager = autoclass('android.view.WindowManager')
    LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
    VideoView = autoclass('android.widget.VideoView')
    
    try: MyWebChromeClient = autoclass('org.alien.MyWebChromeClient')
    except: MyWebChromeClient = autoclass('android.webkit.WebChromeClient')

    class TTSInitListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
        def __init__(self):
            super().__init__()
            self.is_ready = False
        @java_method('(I)V')
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.is_ready = True

    class JSReceiver(PythonJavaClass):
        __javainterfaces__ = ['android/webkit/ValueCallback']
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
        @java_method('(Ljava/lang/Object;)V')
        def onReceiveValue(self, value):
            if value and str(value) != 'null':
                try:
                    val = str(value)
                    if val.startswith('"') and val.endswith('"'): val = val[1:-1]
                    val = val.replace('\\n', '\n').replace('\\"', '"')
                    if val and val != "null": self.callback(val)
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
            request_permissions([
                Permission.RECORD_AUDIO, 
                Permission.GET_ACCOUNTS, 
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE
            ])
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

    def show_toast(self, text):
        if platform == 'android':
            run_on_ui_thread(lambda: Toast.makeText(activity, text, Toast.LENGTH_SHORT).show())()

    def start_app(self, dt):
        if platform == 'android' and Settings.canDrawOverlays(activity):
            self.show_bubble()
        self.load_webview()
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
        self.wv.getSettings().setAllowFileAccess(True)
        self.wv.setWebChromeClient(MyWebChromeClient())
        # ہگنگ فیس والا لنک جو کہ ایپ کا دماغ ہے
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
            self.show_toast("عائشہ بول رہی ہے...")
            loc = Locale("ur", "PK")
            self.tts.setLanguage(loc)
            self.tts.setPitch(1.0)
            self.tts.setSpeechRate(1.0)
            
            # ⚡ زبردستی پلے کرنے کا بنڈل تاکہ آواز بلاک نہ ہو
            try:
                Bundle = autoclass('android.os.Bundle')
                params = Bundle()
                self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, params, "1")
            except:
                self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, "1")
        else:
            self.show_toast("سپیکر انجن تیار ہو رہا ہے...")
            self.init_hardware()

    def execute_command(self, cmd):
        try:
            if cmd == "CMD_OPEN_GALLERY":
                self.open_gallery()
            elif cmd == "CMD_FLASHLIGHT_ON" and self.camera_manager and self.camera_id:
                self.camera_manager.setTorchMode(self.camera_id, True)
            elif cmd == "CMD_FLASHLIGHT_OFF" and self.camera_manager and self.camera_id:
                self.camera_manager.setTorchMode(self.camera_id, False)
            elif cmd == "CMD_VIBRATE":
                vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                if vibrator and vibrator.hasVibrator():
                    vibrator.vibrate(500)
        except Exception as e:
            self.show_toast("Command Error: " + str(e))

    def open_gallery(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.handle_image_selection, filters=[("Images", "*.png", "*.jpg", "*.jpeg")])
        except Exception as e:
            self.show_toast("Gallery Error: " + str(e))

    def handle_image_selection(self, selection):
        if selection and len(selection) > 0:
            filepath = selection[0]
            import base64
            try:
                with open(filepath, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                js_code = f"receiveImageFromAndroid('data:image/jpeg;base64,{encoded}')"
                run_on_ui_thread(lambda: self.wv.evaluateJavascript(js_code, None))()
            except Exception as e:
                self.show_toast("Image Load Error")

class AlienAIChat(App):
    def build(self): return AlienAppBase()

if __name__ == '__main__': AlienAIChat().run()
                
