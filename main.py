from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.window import Window

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
    import android.activity
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    MyWebClient = autoclass('com.raza.alien.MyWebClient')
    FileChooserParams = autoclass('android.webkit.WebChromeClient$FileChooserParams')
    
    # 🟢 یہ فنکشن گیلری سے منتخب کی گئی تصویر ویب سائٹ کو دے گا
    def on_activity_result(request_code, result_code, intent):
        if request_code == 100:
            if MyWebClient.mUploadMessage is not None:
                results = FileChooserParams.parseResult(result_code, intent)
                MyWebClient.mUploadMessage.onReceiveValue(results)
                MyWebClient.mUploadMessage = None
                
    android.activity.bind(on_activity_result=on_activity_result)

class AlienAIApp(App):
    def build(self):
        # 🔴 یہ لائن سکرین کو سونے نہیں دے گی، جس سے مائیک نہیں کٹے گا
        Window.keep_on = True 
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
            
            # 🟢 آواز اور ہارڈویئر کی فائنل سیٹنگز
            s.setJavaScriptEnabled(True)
            s.setDomStorageEnabled(True) 
            s.setDatabaseEnabled(True)
            s.setMediaPlaybackRequiresUserGesture(False)
            s.setAllowFileAccess(True)
            s.setAllowContentAccess(True)
            s.setMixedContentMode(0) # 🔴 آواز کا حل (Mixed Content Allow)
            Activity.setVolumeControlStream(3) # 🔴 میڈیا سپیکر کا حل (Stream Music)
            
            self.webview.setWebViewClient(WebViewClient())
            self.webview.setWebChromeClient(MyWebClient())
            
            self.webview.loadUrl('https://aigrowthbox-ayesha-ai.hf.space')
            Activity.setContentView(self.webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
