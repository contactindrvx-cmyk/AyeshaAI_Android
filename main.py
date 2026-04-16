import os
import sqlite3
import socket
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# گرافکس فکس
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android.permissions import request_permissions, Permission
    
    # اینڈرائیڈ کی کلاسز
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    
    # آپ کی کسٹم جاوا کلاس جو مائیک کا پرمیشن الرٹ ختم کرے گی
    try:
        MyWebChromeClient = autoclass('org.alien.MyWebChromeClient')
    except Exception as e:
        print("Java Class Error:", e)
        MyWebChromeClient = autoclass('android.webkit.WebChromeClient')

    Context = autoclass('android.content.Context')
    WindowManager = autoclass('android.view.WindowManager')
    LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
    PixelFormat = autoclass('android.graphics.PixelFormat')
    VideoView = autoclass('android.widget.VideoView')
    Gravity = autoclass('android.view.Gravity')
else:
    run_on_ui_thread = lambda x: x

class AlienAppBase(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. ایپ کھلتے ہی مائیک کی پرمیشن مانگنا
        if platform == 'android':
            request_permissions([Permission.RECORD_AUDIO])
            # 2 سیکنڈ بعد ببل کی پرمیشن چیک کرنا
            Clock.schedule_once(self.check_overlay_permission, 2)
        
        # 3 سیکنڈ بعد اصل ایپ لانچ کرنا
        Clock.schedule_once(self.start_alien_brain, 3)

    def check_overlay_permission(self, dt):
        if platform == 'android':
            if not Settings.canDrawOverlays(activity):
                intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
                intent.setData(Uri.parse("package:" + activity.getPackageName()))
                activity.startActivity(intent)
            else:
                self.setup_floating_bubble()

    def setup_floating_bubble(self):
        try:
            # ببل کا سائز اور پوزیشن (دائیں طرف اوپر)
            params = LayoutParams(
                350, 350,
                LayoutParams.TYPE_APPLICATION_OVERLAY,
                LayoutParams.FLAG_NOT_FOCUSABLE,
                PixelFormat.TRANSLUCENT
            )
            params.gravity = Gravity.TOP | Gravity.RIGHT
            params.x = 20
            params.y = 100
            
            window_manager = activity.getSystemService(Context.WINDOW_SERVICE)
            self.bubble_video = VideoView(activity)
            
            # ببل کے اندر آپ کی presplash.mp4 ویڈیو چلانا
            video_file = os.path.join(os.path.dirname(__file__), "presplash.mp4")
            video_uri = Uri.parse("file://" + video_file)
            self.bubble_video.setVideoURI(video_uri)
            
            # ویڈیو کو لوپ (Loop) پر لگانا
            self.bubble_video.setOnPreparedListener(
                autoclass('android.media.MediaPlayer$OnPreparedListener')({
                    'onPrepared': lambda mp: mp.setLooping(True)
                })
            )
            
            self.bubble_video.start()
            window_manager.addView(self.bubble_video, params)
            print("[Alien AI] Video Bubble Launched!")
            
        except Exception as e:
            print(f"[Alien AI] Bubble Error: {e}")

    def start_alien_brain(self, dt):
        if self.check_internet():
            self.create_webview()
        else:
            msg = "Raza Bhai, Internet Connect Karein...\n[Alien AI]"
            lbl = Label(text=msg, halign="center", font_size="18sp")
            self.add_widget(lbl)

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    @run_on_ui_thread
    def create_webview(self):
        if platform == 'android':
            webview = WebView(activity)
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setMediaPlaybackRequiresUserGesture(False)
            settings.setAllowFileAccess(True)
            settings.setAllowContentAccess(True)
            
            webview.setWebViewClient(WebViewClient())
            
            # *** یہ ہے وہ لائن جو مائیک کا مسئلہ ختم کرے گی ***
            webview.setWebChromeClient(MyWebChromeClient())
            
            webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            activity.setContentView(webview)

class AlienAIChat(App):
    def build(self):
        return AlienAppBase()

if __name__ == '__main__':
    AlienAIChat().run()
    
