import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# اینڈرائیڈ 16 گرافکس فکس
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # اگر لیپ ٹاپ پر ٹیسٹ کریں تو کریش نہ ہو
    run_on_ui_thread = lambda x: x

class HuggingFaceSpace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        if platform == 'android':
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # ویب سائٹ کو صحیح چلانے کے لیے ضروری سیٹنگز
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setMediaPlaybackRequiresUserGesture(False)
            
            webview.setWebViewClient(WebViewClient())
            webview.setWebChromeClient(WebChromeClient())
            
            # رضا بھائی، یہ آپ کے ہگنگ فیس کا ڈائریکٹ لنک ہے
            webview.loadUrl('https://huggingface.co/spaces/aigrowthbox/ayesha-ai')
            
            activity.setContentView(webview)

class AlianAI(App):
    def build(self):
        return HuggingFaceSpace()

if __name__ == '__main__':
    AlianAI().run()
    
