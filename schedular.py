from kivy.app import App
from eventManager import EventManager

class EventApp(App):
    def build(self):
        return EventManager()

if __name__ == '__main__':
    EventApp().run()
