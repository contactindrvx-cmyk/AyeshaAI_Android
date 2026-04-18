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
    
    # 🟢 اب پائتھن کچھ نہیں کرے گا، صرف جاوا کو بتائے گا کہ گیلری بند ہو گئی ہے
    def on_activity_result(request_code, result_code, intent):
        if request_code == 100:
            # جاوا کا ماسٹر فنکشن کال ہو رہا ہے
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
                "android.permission.READ_MEDIA_AUDIO",
                "android.permission.READ_MEDIA_VIDEO"
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            WebView.setWebContentsDebuggingEnabled(True)
            
            self.webview = WebView(Activity)
            s = self.webview.getSettings()
            
            # 🔵 موبائل کروم کی شناخت تاکہ کوئی فیچر بلاک نہ ہو
            user_agent = "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
            s.setUserAgentString(user_agent)
            
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) 
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) 
            s.setAllowFileAccess(True)
            s.setAllowContentAccess(True)
            s.setMixedContentMode(0) 
            
            CookieManager = autoclass('android.webkit.CookieManager')
            cookie_manager = CookieManager.getInstance()
            cookie_manager.setAcceptCookie(True)
            cookie_manager.setAcceptThirdPartyCookies(self.webview, True)
            
            Activity.setVolumeControlStream(3) 
            
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(MyWebClient())
            
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
