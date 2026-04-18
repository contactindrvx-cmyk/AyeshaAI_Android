from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity

class AlienAIApp(App):
    def build(self):
        self.root = Widget()
        if platform == 'android':
            request_permissions([
                Permission.INTERNET, Permission.RECORD_AUDIO,
                Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE, Permission.MODIFY_AUDIO_SETTINGS
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            self.webview = WebView(Activity)
            s = self.webview.getSettings()
            
            # آواز اور فائلز کی سیٹنگز
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) 
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) 
            s.setAllowFileAccess(True)
            s.setAllowContentAccess(True)
            
            # 🔴 آپ کی بنائی ہوئی اصلی جاوا کلاس بلائی جا رہی ہے
            MyWebClient = autoclass('com.raza.alien.MyWebClient')
            
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(MyWebClient())
            
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
