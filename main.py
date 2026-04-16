import kivy
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
import google.generativeai as genai

# آپ کی فراہم کردہ 3 کیز
API_KEYS = [
    "AIzaSyBuhS0ZC2tg370mo-nQW-_zKY_OUMFAGdo", 
    "AIzaSyD_DqBfz2wJtpEfbw1lf25GZOi_nkzouXo",
    "AIzaSyDFPFHsjz116X430v1oZYgBe-MLY6qinm8"
]

class AyeshaAI(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        screen = MDScreen()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.input_text = MDTextField(
            hint_text="عائشہ سے کچھ پوچھیں...",
            mode="rectangle"
        )
        
        btn = MDRaisedButton(
            text="بات کریں",
            pos_hint={"center_x": .5},
            on_release=self.ask_ayesha
        )
        
        self.response_label = MDTextField(
            hint_text="عائشہ کا جواب یہاں آئے گا",
            readonly=True,
            multiline=True
        )
        
        layout.add_widget(self.input_text)
        layout.add_widget(btn)
        layout.add_widget(self.response_label)
        
        screen.add_widget(layout)
        return screen

    def ask_ayesha(self, instance):
        user_query = self.input_text.text
        if not user_query:
            return

        success = False
        # باری باری تینوں کیز چیک کرنے کا سسٹم
        for i, key in enumerate(API_KEYS):
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-pro')
                
                response = model.generate_content(user_query)
                self.response_label.text = response.text
                success = True
                print(f"Success with Key {i+1}")
                break 
            except Exception as e:
                print(f"Key {i+1} failed: {str(e)}")
                continue 

        if not success:
            self.response_label.text = "معذرت رضا بھائی، تمام کیز مصروف ہیں یا انٹرنیٹ کا مسئلہ ہے۔ تھوڑی دیر بعد ٹرائی کریں۔"

if __name__ == "__main__":
    AyeshaAI().run()
    
