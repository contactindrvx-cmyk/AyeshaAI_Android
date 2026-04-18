from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity

class AlienAIApp(App):
    def build(self):
        self.root = Widget() 
        if platform == 'android':
            request_permissions([
                Permission.INTERNET,
                Permission.RECORD_AUDIO,
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            webview = WebView(Activity)
            settings = webview.getSettings()
            
            # بیسک سیٹنگز
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setMediaPlaybackRequiresUserGesture(False)
            
            # 🟢 بٹن اور سکرین فٹ کرنے کی سیٹنگز (Viewport Fix)
            settings.setLoadWithOverviewMode(True)
            settings.setUseWideViewPort(True)
            
            webview.setWebViewClient(WebViewClient())
            webview.setWebChromeClient(WebChromeClient())
            
            # 🟢 ڈائریکٹ ایپ کا لنک (یہ فالتو ہیڈر خود بخود اڑا دے گا)
            clean_url = 'https://aigrowthbox-ayesha-ai.hf.space'
            webview.loadUrl(clean_url)
            
            Activity.setContentView(webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
