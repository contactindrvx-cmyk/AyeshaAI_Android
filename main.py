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

    # 🔴 یہ کلاس مائیک اور کیمرہ کو ویب سائٹ کے لیے چالو کرے گی
    class MyChromeClient(WebChromeClient):
        def onPermissionRequest(self, request):
            request.grant(request.getResources())

class AlienAIApp(App):
    def build(self):
        self.root = Widget()
        if platform == 'android':
            request_permissions([
                Permission.INTERNET, Permission.RECORD_AUDIO,
                Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            self.webview = WebView(Activity)
            s = self.webview.getSettings()
            
            # 🟢 آواز اور ہارڈویئر کا حل
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) # آواز کے لیے لازمی
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) # آٹو پلے آواز
            s.setAllowFileAccess(True) # پلس بٹن کے لیے
            s.setAllowContentAccess(True)
            
            # سٹیبل کلائنٹس
            self.webview.setWebViewClient(WebViewClient())
            # مائیک/کیمرہ کی اجازت والا کلائنٹ
            self.webview.setWebChromeClient(MyChromeClient())
            
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
