from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.window import Window

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    from android.activity import bind as activity_bind # 🔴 نیا بائنڈر جو گیلری کھولے گا
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    MyWebClient = autoclass('com.raza.alien.MyWebClient')
    FileChooserParams = autoclass('android.webkit.WebChromeClient$FileChooserParams')
    
    # 🔴 عائشہ کی آواز کے لیے تیسرے سرور کی پرمیشن
    CookieManager = autoclass('android.webkit.CookieManager') 
    
    # 🟢 تصویر کو گیلری سے پکڑ کر ویب سائٹ کے پلس بٹن کو دینا
    def on_activity_result(request_code, result_code, intent):
        if request_code == 100:
            if MyWebClient.mUploadMessage is not None:
                try:
                    results = FileChooserParams.parseResult(result_code, intent)
                    MyWebClient.mUploadMessage.onReceiveValue(results)
                except Exception:
                    MyWebClient.mUploadMessage.onReceiveValue(None)
                MyWebClient.mUploadMessage = None
                
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
            self.webview = WebView(Activity)
            s = self.webview.getSettings()
            
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) 
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) 
            s.setAllowFileAccess(True)
            s.setAllowContentAccess(True)
            s.setAllowFileAccessFromFileURLs(True)
            s.setAllowUniversalAccessFromFileURLs(True)
            s.setMixedContentMode(0) 
            
            # 🔴 آواز کا 100% پکا علاج (Cookies اور ہارڈویئر ایکسلریشن)
            cookie_manager = CookieManager.getInstance()
            cookie_manager.setAcceptCookie(True)
            cookie_manager.setAcceptThirdPartyCookies(self.webview, True) # اس سے عائشہ کی آواز ان لاک ہوگی
            self.webview.setLayerType(2, None) # آواز کو صاف چلانے کے لیے Hardware Acceleration
            
            Activity.setVolumeControlStream(3) 
            
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(MyWebClient())
            
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
