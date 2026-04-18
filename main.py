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
            # موبائل سے بنیادی پرمیشنز مانگنا
            request_permissions([
                Permission.INTERNET, 
                Permission.RECORD_AUDIO,
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MODIFY_AUDIO_SETTINGS
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            self.webview = WebView(Activity)
            s = self.webview.getSettings()
            
            # 🟢 آواز اور فائل ایکسیس کی بالکل محفوظ سیٹنگز
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) # عائشہ کی آواز کے لیے ضروری
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) # آواز آٹو پلے
            s.setAllowFileAccess(True) # پلس بٹن سے فائل اپلوڈ کے لیے
            s.setAllowContentAccess(True)
            
            # 🔴 یہاں اوریجنل کلائنٹ استعمال کیا ہے تاکہ کریش نہ ہو
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(WebChromeClient())
            
            # آپ کا لنک
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
