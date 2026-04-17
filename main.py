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

# ہیڈر ہٹانے کے لیے کسٹم کلائنٹ
class MyWebViewClient(WebViewClient):
    def onPageFinished(self, view, url):
        # یہ لائن ہیڈر اور فالتو ایلیمنٹس کو غائب کر دے گی
        view.loadUrl("javascript:(function() { " +
                     "document.querySelector('header').style.display='none'; " +
                     "document.querySelector('footer').style.display='none'; " +
                     "document.querySelector('.header').style.display='none'; " +
                     "})()")

class AlienAIApp(App):
    def build(self):
        self.layout = FloatLayout()
        
        # 🟢 فلوٹنگ ببل
        self.bubble_video = Video(
            source='ayesha.mp4',
            state='play',
            options={'eos': 'loop'}, 
            size_hint=(None, None),
            size=(250, 250), 
            pos_hint={'right': 0.98, 'top': 0.95} 
        )
        self.layout.add_widget(self.bubble_video)

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
            webview.getSettings().setMediaPlaybackRequiresUserGesture(False)
            
            # ہیڈر چھپانے والا کلائنٹ سیٹ کریں
            webview.setWebViewClient(MyWebViewClient())
            webview.setWebChromeClient(WebChromeClient())
            
            # ایمبیڈ موڈ کے ساتھ لنک لوڈ کریں
            clean_url = 'https://huggingface.co/spaces/aigrowthbox/ayesha-ai?embed=true'
            webview.loadUrl(clean_url)
            
            Activity.setContentView(webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
