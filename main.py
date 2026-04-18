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
        # صرف ایک خالی بیس لے آؤٹ، تاکہ کریش نہ ہو
        self.root = Widget() 
        
        if platform == 'android':
            # کیمرہ، مائیک اور انٹرنیٹ کی پرمیشنز
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
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.getSettings().setMediaPlaybackRequiresUserGesture(False)
            
            # ڈیفالٹ کلائنٹ تاکہ کوئی ایرر نہ آئے اور ایپ براؤزر میں نہ کھلے
            webview.setWebViewClient(WebViewClient())
            webview.setWebChromeClient(WebChromeClient())
            
            # آپ کا لنک embed=true کے ساتھ (یہ خود ہیڈر ہٹا دے گا)
            clean_url = 'https://huggingface.co/spaces/aigrowthbox/ayesha-ai?embed=true'
            webview.loadUrl(clean_url)
            
            # ویب ویو کو پوری سکرین پر سیٹ کرنا
            Activity.setContentView(webview)

if __name__ == '__main__':
    AlienAIApp().run()
    
