import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.webbrowser import open_url

class AyeshaAI(App):
    def build(self):
        # یہ براہ راست براؤزر میں کھول دے گا تاکہ ایپ کریش نہ ہو
        open_url("https://raza-ayesha-ai.hf.space")
        layout = BoxLayout()
        layout.add_widget(Label(text="Ayesha AI is loading in your browser..."))
        return layout

if __name__ == "__main__":
    AyeshaAI().run()
    
