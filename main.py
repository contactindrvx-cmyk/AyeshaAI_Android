import os
# اینڈرائیڈ 16 کریش کو مستقل روکنے کے لیے گرافکس انجن کو فکس کرنا
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import certifi
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
import requests
from plyer import tts

# انٹرنیٹ کنکشن کے لیے سرٹیفکیٹ فکس
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
        # لوگو کا پکا حل: یہاں سے ایپ آپ کا icon.png اٹھائے گی
        self.icon = 'icon.png'
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        
        screen = MDScreen()
        
        # مین لے آؤٹ (اس سے ہیڈر اوپر فکس رہے گا)
        main_layout = MDBoxLayout(orientation='vertical')
        
        # 1. ٹاپ ہیڈر (اب یہ اوپر سے ہلے گا نہیں)
        self.toolbar = MDTopAppBar(
            title="Alian AI (2.5 Flash)",
            elevation=4,
            md_bg_color=self.theme_cls.primary_color
        )
        main_layout.add_widget(self.toolbar)
        
        # 2. درمیانی حصہ: چیٹ اور سپیکر
        chat_area = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        self.message_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            size_hint=(1, 1),
            md_bg_color=(0.12, 0.12, 0.18, 1),
            radius=[20,]
        )
        
        # سکرول ویو تاکہ لمبا میسج بھی آسانی سے پڑھا جا سکے
        scroll = MDScrollView()
        self.response_label = MDTextField(
            text="سلام رضا بھائی! میں عائشہ ہوں۔ اب میرا نیا دماغ 2.5 فلیش بالکل سیٹ ہے۔ بتائیے کیا کروں؟",
            readonly=True,
            multiline=True,
            mode="fill",
            fill_color_normal=(0, 0, 0, 0),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        scroll.add_widget(self.response_label)
        self.message_card.add_widget(scroll)
        
        # پروفیشنل سپیکر بٹن (میسج کے بالکل نیچے)
        self.speaker_btn = MDIconButton(
            icon="volume-high",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            pos_hint={"right": 1},
            on_release=self.speak_message
        )
        self.message_card.add_widget(self.speaker_btn)
        
        chat_area.add_widget(self.message_card)
        main_layout.add_widget(chat_area)
        
        # 3. نیچے والا حصہ: ان پٹ بار
        input_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10), spacing=dp(5))
        self.input_text = MDTextField(
            hint_text="عائشہ سے کچھ پوچھیں...",
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
        
        self.response_label.text = "عائشہ سوچ رہی ہے..."
        self.input_text.text = ""
        
        for key in API_KEYS:
            try:
                # Gemini 2.5 Flash API
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": user_query}]}]}
                
                response = requests.post(url, headers=headers, json=data, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    self.response_label.text = result['candidates'][0]['content']['parts'][0]['text']
                    return
            except Exception:
                continue
                
        self.response_label.text = "معذرت رضا بھائی، انٹرنیٹ کا مسئلہ ہے یا سرور جواب نہیں دے رہا۔"

    def speak_message(self, instance):
        try:
            if self.response_label.text:
                tts.speak(self.response_label.text)
        except Exception:
            pass

if __name__ == "__main__":
    AlianAI().run()
    
