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
import requests
import json
from plyer import tts

# SSL فکس: سرٹیفکیٹ کی لوکیشن سیٹ کرنا
try:
    os.environ['SSL_CERT_FILE'] = certifi.where()
except Exception:
    pass

API_KEYS = [
    "AIzaSyBuhS0ZC2tg370mo-nQW-_zKY_OUMFAGdo", 
    "AIzaSyD_DqBfz2wJtpEfbw1lf25GZOi_nkzouXo",
    "AIzaSyDFPFHsjz116X430v1oZYgBe-MLY6qinm8"
]

class AlianAI(MDApp):
    def build(self):
        # اینڈرائیڈ 16 تھیم فکس
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical')
        
        # 1. ہیڈر
        self.toolbar = MDTopAppBar(
            title="Alian AI (Flash 2.5)",
            elevation=4,
            md_bg_color=self.theme_cls.primary_color
        )
        main_layout.add_widget(self.toolbar)
        
        # 2. چیٹ ایریا
        chat_container = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        self.message_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            size_hint=(1, None),
            height=dp(400),
            md_bg_color=(0.12, 0.12, 0.18, 1),
            radius=[20,]
        )
        
        self.response_label = MDTextField(
            text="سلام رضا بھائی! اب میں 2.5 ورژن پر کام کر رہا ہوں۔ بتائیے عائشہ کے حوالے سے کیا مدد کروں؟",
            readonly=True,
            multiline=True,
            mode="fill",
            fill_color_normal=(0, 0, 0, 0),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        
        self.speaker_btn = MDIconButton(
            icon="volume-high",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            pos_hint={"right": 1},
            on_release=self.speak_message
        )
        
        self.message_card.add_widget(self.response_label)
        self.message_card.add_widget(self.speaker_btn)
        chat_container.add_widget(self.message_card)
        main_layout.add_widget(chat_container)
        
        # 3. ان پٹ بار
        input_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10), spacing=dp(5))
        self.input_text = MDTextField(
            hint_text="کچھ پوچھیں...",
            mode="round",
            size_hint_x=0.85
        )
        send_btn = MDIconButton(
            icon="send-circle",
            on_release=self.ask_alian,
            icon_size="40sp",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color
        )
        
        input_layout.add_widget(self.input_text)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        
        screen.add_widget(main_layout)
        return screen

    def ask_alian(self, instance):
        user_query = self.input_text.text.strip()
        if not user_query: return
        
        self.response_label.text = "Alian سوچ رہا ہے..."
        self.input_text.text = ""
        
        for key in API_KEYS:
            try:
                # یہاں ماڈل کا نام 2.5 پر سیٹ کر دیا ہے
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": user_query}]}]}
                
                response = requests.post(url, headers=headers, json=data, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    self.response_label.text = answer
                    return
            except Exception:
                continue
                
        self.response_label.text = "سرور کا مسئلہ ہے یا آپ کی 2.5 والی کیز کی لمٹ ختم ہو گئی ہے۔"

    def speak_message(self, instance):
        try:
            tts.speak(self.response_label.text)
        except Exception:
            pass

if __name__ == "__main__":
    AlianAI().run()
        
