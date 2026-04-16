import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
import google.generativeai as genai
from plyer import tts

API_KEYS = [
    "AIzaSyBuhS0ZC2tg370mo-nQW-_zKY_OUMFAGdo", 
    "AIzaSyD_DqBfz2wJtpEfbw1lf25GZOi_nkzouXo",
    "AIzaSyDFPFHsjz116X430v1oZYgBe-MLY6qinm8"
]

class AlianAI(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical')
        
        self.toolbar = MDTopAppBar(
            title="Alian AI",
            elevation=4,
            pos_hint={"top": 1},
            md_bg_color=self.theme_cls.primary_color
        )
        main_layout.add_widget(self.toolbar)
        
        self.chat_area = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        self.message_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            size_hint=(1, None),
            height=dp(350),
            md_bg_color=(0.1, 0.1, 0.15, 1),
            radius=[15,]
        )
        
        self.response_label = MDTextField(
            text="سلام رضا بھائی! میں Alian ہوں۔ آپ کے Android 16 کے لیے تیار ہوں۔",
            readonly=True,
            multiline=True,
            font_size="17sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.message_card.add_widget(self.response_label)
        
        self.speaker_btn = MDIconButton(
            icon="volume-high",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            pos_hint={"center_x": 0.9},
            on_release=self.speak_message
        )
        self.message_card.add_widget(self.speaker_btn)
        
        self.chat_area.add_widget(self.message_card)
        main_layout.add_widget(self.chat_area)
        
        input_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), padding=dp(10), spacing=dp(5))
        self.input_text = MDTextField(hint_text="Alian سے بات کریں...", mode="fill", size_hint_x=0.85)
        send_btn = MDIconButton(icon="send", on_release=self.ask_alian, icon_size="30sp")
        
        input_layout.add_widget(self.input_text)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        
        screen.add_widget(main_layout)
        return screen

    def ask_alian(self, instance):
        user_query = self.input_text.text
        if not user_query: return
        
        self.response_label.text = "Alian سوچ رہا ہے..."
        self.input_text.text = ""
        
        for key in API_KEYS:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(user_query)
                self.response_label.text = response.text
                return
            except Exception:
                continue
        self.response_label.text = "رابطہ کرنے میں مشکل ہو رہی ہے۔"

    def speak_message(self, instance):
        try:
            tts.speak(self.response_label.text)
        except:
            pass

if __name__ == "__main__":
    AlianAI().run()
    
