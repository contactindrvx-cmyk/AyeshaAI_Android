import os, socket
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    AccountManager = autoclass('android.accounts.AccountManager')
    WebView = autoclass('android.webkit.WebView')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    
    # ببل اور ویڈیو کلاسز
    WindowManager = autoclass('android.view.WindowManager')
    LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
    VideoView = autoclass('android.widget.VideoView')
    PixelFormat = autoclass('android.graphics.PixelFormat')
    
    try: MyWebChromeClient = autoclass('org.alien.MyWebChromeClient')
    except: MyWebChromeClient = autoclass('android.webkit.WebChromeClient')
else:
    run_on_ui_thread = lambda x: x

class AlienAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            request_permissions([Permission.RECORD_AUDIO, Permission.GET_ACCOUNTS])
            Clock.schedule_once(self.start_app, 3)

    def start_app(self, dt):
        if platform == 'android' and Settings.canDrawOverlays(activity):
            self.show_bubble()
        self.load_webview()

    def show_bubble(self):
        try:
            params = LayoutParams(350, 350, LayoutParams.TYPE_APPLICATION_OVERLAY, 8, -3)
            wm = activity.getSystemService(autoclass('android.content.Context').WINDOW_SERVICE)
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
        wv = WebView(activity)
        wv.getSettings().setJavaScriptEnabled(True)
        wv.setWebChromeClient(MyWebChromeClient())
        wv.loadUrl(f'https://aigrowthbox-ayesha-ai.hf.space?email={email}')
        activity.setContentView(wv)

class AlienAIChat(App):
    def build(self): return AlienAppBase()

if __name__ == '__main__': AlienAIChat().run()
    
