from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity

    # 🔴 یہ کلاس مائیک اور کیمرہ کی اجازت ویب سائٹ کو دے گی
    class MyWebChromeClient(WebChromeClient):
        def onPermissionRequest(self, request):
            request.grant(request.getResources())

class AlienAIApp(App):
    def build(self):
        self.root = Widget() 
        if platform == 'android':
            request_permissions([
                Permission.INTERNET,
                Permission.RECORD_AUDIO,
                Permission.CAMERA,
                Permission.MODIFY_AUDIO_SETTINGS,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            self.webview = WebView(Activity)
            settings = self.webview.getSettings()
            
            # 🟢 آواز اور ہارڈویئر سیٹنگز
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True) # آواز کے لیے ضروری
            settings.setDatabaseEnabled(True)
            settings.setMediaPlaybackRequiresUserGesture(False) # آواز آٹو پلے کے لیے
            
            # 🔵 فائل اپلوڈ (تصویر بھیجنے) کے لیے سیٹنگز
            settings.setAllowFileAccess(True)
            settings.setAllowContentAccess(True)
            settings.setAllowFileAccessFromFileURLs(True)
            settings.setAllowUniversalAccessFromFileURLs(True)
            
            # ویب ویو کلائنٹس
            self.webview.setWebViewClient(WebViewClient())
            # 🔴 مائیک اور کیمرہ کے لیے نیا کلائنٹ
            self.webview.setWebChromeClient(MyWebChromeClient())
            
            # آپ کا لنک
            clean_url = 'https://aigrowthbox-ayesha-ai.hf.space'
            self.webview.loadUrl(clean_url)
            
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
