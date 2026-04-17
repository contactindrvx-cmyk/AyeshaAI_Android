from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity

class AyeshaAIApp(App):
    def build(self):
        self.layout = FloatLayout()
        
        # 🟢 فلوٹنگ ببل (عائشہ کی ویڈیو)
        self.bubble_video = Video(
            source='ayesha.mp4',  # یہاں آپ کی ویڈیو کا نام ہونا چاہیے
            state='play',
            options={'eos': 'loop'}, # ویڈیو بار بار چلے گی
            size_hint=(None, None),
            size=(250, 250), # ببل کا سائز
            pos_hint={'right': 0.95, 'top': 0.95} # سکرین کے اوپر دائیں کونے میں
        )
        self.layout.add_widget(self.bubble_video)

        # اینڈرائیڈ کے لیے پرمیشنز اور ویب ویو
        if platform == 'android':
            request_permissions([
                Permission.INTERNET,
                Permission.RECORD_AUDIO,
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            self.create_webview()
            
        return self.layout

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            webview = WebView(Activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.getSettings().setMediaPlaybackRequiresUserGesture(False) # آٹو پلے کے لیے
            webview.setWebViewClient(WebViewClient())
            webview.setWebChromeClient(WebChromeClient())
            
            # 👇 یہاں اپنا اصل ہگنگ فیس کا لنک ڈالیں
            webview.loadUrl('YOUR_HUGGING_FACE_LINK_HERE')
            
            # ویب ویو کو سیٹ کرنا
            Activity.setContentView(webview)

if __name__ == '__main__':
    AyeshaAIApp().run()
    
