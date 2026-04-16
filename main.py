import os
import sys

# --- اینڈرائیڈ 16 گرافکس بائی پاس (سب سے اوپر) ---
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'backend', 'sdl2')

import certifi
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp
import requests
from plyer import tts

# SSL فکس
try:
    os.environ['SSL_CERT_FILE'] = certifi.where()
except:
    pass

class AlianAI(MDApp):
    def build(self):
        # اینڈرائیڈ 16 کے لیے تھیم کا پکا حل
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        
        # مین سکرین
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=dp(10))
        
        # ہیڈر (سادہ لیکن پکا)
        header = MDLabel(
            text="Alian AI 2.5",
            halign="center",
            size_hint_y=None,
            height=dp(60),
            font_style="H5",
            theme_text_color="Primary"
        )
        layout.add_widget(header)
        
        # میسج ایریا
        self.msg_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            radius=[15,],
            md_bg_color=(0.12, 0.12, 0.18, 1)
        )
        
        self.response_label = MDTextField(
            text="سلام رضا بھائی! اگر آپ یہ دیکھ پا رہے ہیں تو ہم جیت گئے ہیں۔ بتائیے کیا حکم ہے؟",
            readonly=True,
            multiline=True,
            mode="fill",
            fill_color_normal=(0,0,0,0)
        )
        self.msg_card.add_widget(self.response_label)
        layout.add_widget(self.msg_card)
        
        # ان پٹ اور بٹن
        input_box = MDBoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        self.user_input = MDTextField(hint_text="عائشہ سے پوچھیں...", mode="round")
        send_btn = MDIconButton(icon="send", on_release=self.ask_alian)
        
        input_box.add_widget(self.user_input)
        input_box.add_widget(send_btn)
        layout.add_widget(input_box)
        
        screen.add_widget(layout)
        return screen

    def ask_alian(self, instance):
        query = self.user_input.text.strip()
        if not query: return
        self.response_label.text = "عائشہ سوچ رہی ہے..."
        self.user_input.text = ""
        
        api_key = "AIzaSyBuhS0ZC2tg370mo-nQW-_zKY_OUMFAGdo"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=10)
            if res.status_code == 200:
                self.response_label.text = res.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                self.response_label.text = "سرور مصروف ہے۔"
        except:
            self.response_label.text = "انٹرنیٹ چیک کریں۔"

if __name__ == "__main__":
    try:
        AlianAI().run()
    except Exception as e:
        # اگر ایپ کریش ہو تو ایرر کو ٹیکسٹ فائل میں لکھ دے تاکہ ہم پڑھ سکیں
        with open("error_log.txt", "w") as f:
            f.write(str(e))
        
