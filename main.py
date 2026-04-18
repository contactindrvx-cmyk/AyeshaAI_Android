from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.window import Window

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    from android.activity import bind as activity_bind
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    MyWebClient = autoclass('com.raza.alien.MyWebClient')
    FileChooserParams = autoclass('android.webkit.WebChromeClient$FileChooserParams')
    
    # 🟢 تصویر سلیکٹ ہونے کے بعد اسے ویب سائٹ کے حوالے کرنے کا پکا طریقہ
    def on_activity_result(request_code, result_code, intent):
        if request_code == 100:
            if MyWebClient.mUploadMessage is not None:
                # اگر تصویر سلیکٹ ہوئی ہے (result_code == -1 یعنی OK)
                if result_code == -1 and intent is not None:
                    data = cast('android.content.Intent', intent)
                    results = FileChooserParams.parseResult(result_code, data)
                    MyWebClient.mUploadMessage.onReceiveValue(results)
                else:
                    # اگر کینسل کر دیا تو 'None' بھیجنا ضروری ہے ورنہ بٹن جام ہو جائے گا
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
                "android.permission.READ_MEDIA_IMAGES"
            ])
            self.create_webview()
        return self.root

    if platform == 'android':
        @run_on_ui_thread
        def create_webview(self):
            self.webview = WebView(Activity)
            s = self.webview.getSettings()
            
            # 🔵 آواز اور تصویر کے لیے ماسٹر سیٹنگز
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) 
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False) 
            s.setAllowFileAccess(True)
            s.setAllowContentAccess(True)
            s.setJavaScriptCanOpenWindowsAutomatically(True) # آواز کے پلیئر کے لیے
            s.setMixedContentMode(0) 
            
            # موبائل کروم کی شناخت تاکہ ویب سائٹ آواز بند نہ کرے
            user_agent = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
            s.setUserAgentString(user_agent)
            
            Activity.setVolumeControlStream(3) 
            
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(MyWebClient())
            
            # ڈائریکٹ لنک
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
