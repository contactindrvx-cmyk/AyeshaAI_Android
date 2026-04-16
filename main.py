import os
import certifi
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivy.core.window import Window
import requests
from plyer import tts

# SSL اور گرافکس فکس (اینڈرائیڈ 16 کے لیے)
try:
    os.environ['SSL_CERT_FILE'] = certifi.where()
    # یہ لائن کریش کو روکنے میں مدد دے گی
    os.environ['KIVY_VIDEO'] = 'ffpyplayer' 
except Exception:
    pass

API_KEYS = [
    "AIzaSyBuhS0ZC2tg370mo-nQW-_zKY_OUMFAGdo", 
    "AIzaSyD_DqBfz2wJtpEfbw1lf25GZOi_nkzouXo",
    "AIzaSyDFPFHsjz116X430v1oZYgBe-MLY6qinm8"
]

class AlianAI(MDApp):
    def build(self):
        # لوگو اور آئیکن سیٹ کرنا
        self.icon = 'icon.png' 
        
        # اینڈرائیڈ 16 کے لیے تھیم کو زبردستی ری سیٹ کرنا
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical')
        
        # ٹاپ بار
        self.toolbar = MDTopAppBar(
            title="Alian AI (2.5 Flash)",
            elevation=2,
            md_bg_color=self.theme_cls.primary_color
        )
        main_layout.add_widget(self.toolbar)
        
        # چیٹ ایریا
        container = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.message_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            size_hint=(1, None),
            height=dp(420),
            md_bg_color=(0.1, 0.1, 0.15, 1),
            radius=[20,]
        )
        
        self.response_label = MDTextField(
            text="سلام رضا بھائی! میں اب بالکل ٹھیک ہو کر واپس آ گیا ہوں۔",
            readonly=True,
            multiline=True,
            mode="fill",
            fill_color_normal=(0, 0, 0, 0),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        
        self.speaker_btn = MDIconButton(
            icon="volume-high",
            pos_hint={"right": 1},
            on_release=self.speak_message
        )
        
        self.message_card.add_widget(self.response_label)
        self.message_card.add_widget(self.speaker_btn)
        container.add_widget(self.message_card)
        main_layout.add_widget(container)
        
        # ان پٹ بار
        input_bar = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10))
        self.input_text = MDTextField(hint_text="بات کریں...", mode="round", size_hint_x=0.85)
        send_btn = MDIconButton(icon="send", on_release=self.ask_alian)
        
        input_bar.add_widget(self.input_text)
        input_bar.add_widget(send_btn)
        main_layout.add_widget(input_bar)
        
        screen.add_widget(main_layout)
        return screen

    def ask_alian(self, instance):
        query = self.input_text.text.strip()
        if not query: return
        self.response_label.text = "Alian سوچ رہا ہے..."
        self.input_text.text = ""
        
        for key in API_KEYS:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
                response = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=15)
                if response.status_code == 200:
                    self.response_label.text = response.json()['candidates'][0]['content']['parts'][0]['text']
                    return
            except Exception: continue
        self.response_label.text = "سرور کا مسئلہ ہے۔"

    def speak_message(self, instance):
        try: tts.speak(self.response_label.text)
        except Exception: pass

if __name__ == "__main__":
    AlianAI().run()
    
