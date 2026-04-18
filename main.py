from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.window import Window

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    from android.activity import bind as activity_bind
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    MyWebClient = autoclass('com.raza.alien.MyWebClient')
    
    def on_activity_result(request_code, result_code, intent):
        if request_code == 100:
            MyWebClient.handleUpload(result_code, intent)
                
    activity_bind(on_activity_result=on_activity_result)

class AlienAIApp(App):
    def build(self):
        Window.keep_on = True 
        self.root = Widget()
        if platform == 'android':
            request_permissions([
                Permission.INTERNET, Permission.RECORD_AUDIO,
                Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE, Permission.MODIFY_AUDIO_SETTINGS,
                "android.permission.READ_MEDIA_IMAGES",
                "android.permission.READ_MEDIA_AUDIO"
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            # 🔴 آواز کے لیے ہارڈویئر ایکسلریشن آن کرنا (بہت ضروری)
            WebView.setWebContentsDebuggingEnabled(True)
            
            self.webview = WebView(Activity)
            
            # 🔴 آواز کو صاف چلانے کے لیے لیئر ٹائپ سیٹ کریں
            self.webview.setLayerType(2, None) # LAYER_TYPE_HARDWARE = 2
            
            s = self.webview.getSettings()
            
            # 🔵 آواز اور آٹو پلے کی حتمی سیٹنگز
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) 
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) # آواز خود چلنے کے لیے
            s.setJavaScriptCanOpenWindowsAutomatically(True)
            s.setAllowFileAccess(True)
            s.setAllowContentAccess(True)
            s.setMixedContentMode(0) 
            
            # 🔴 اصلی کروم کا تازہ ترین ورژن (تاکہ آواز بلاک نہ ہو)
            user_agent = "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro Build/TD1A.220804.031) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36"
            s.setUserAgentString(user_agent)
            
            # والیم کنٹرول
            Activity.setVolumeControlStream(3) 
            
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(MyWebClient())
            
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
