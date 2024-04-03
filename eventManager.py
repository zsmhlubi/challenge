from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from datetime import datetime
from event import Event

class EventManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.events = []

        # Widgets for adding events
        self.title_input = TextInput(hint_text='Title', size_hint=(1, None), height=dp(40))
        self.description_input = TextInput(hint_text='Description', size_hint=(1, None), height=dp(40))
        self.date_input = TextInput(hint_text='Date (YYYY-MM-DD)', size_hint=(1, None), height=dp(40))
        self.time_input = TextInput(hint_text='Time (HH:MM)', size_hint=(1, None), height=dp(40))
        self.add_button = Button(text='Add Event', size_hint=(1, None), height=dp(40))
        self.add_button.bind(on_press=self.add_event)

        # Widgets for deleting events
        self.delete_title_input = TextInput(hint_text='Event Title to Delete', size_hint=(1, None), height=dp(40))
        self.delete_button = Button(text='Delete Event', size_hint=(1, None), height=dp(40))
        self.delete_button.bind(on_press=self.delete_event)

        # Widget for displaying events
        self.event_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.event_list_layout.bind(minimum_height=self.event_list_layout.setter('height'))
        self.event_list_scrollview = ScrollView()

        # Add widgets to the layout
        self.add_widget(Label(text='Events', size_hint=(1, None), height=40))
        self.add_widget(self.event_list_scrollview)
        self.add_widget(Label(text='Event Manager', size_hint=(1, None), height=40))
        self.add_widget(self.title_input)
        self.add_widget(self.description_input)
        self.add_widget(self.date_input)
        self.add_widget(self.time_input)
        self.add_widget(self.add_button)
        self.add_widget(self.delete_title_input)
        self.add_widget(self.delete_button)
        self.event_list_scrollview.add_widget(self.event_list_layout)  # Moved here to ensure correct order

        self.update_event_list()
        
    def add_event(self, instance):
        title = self.title_input.text.strip()
        description = self.description_input.text.strip()
        date = self.date_input.text.strip()
        time = self.time_input.text.strip()

        if not title or not description:
            self.show_error_popup("Title and Description are required.")
            return

        if not self.is_valid_date(date):
            self.show_error_popup("Invalid date format. Use YYYY-MM-DD.")
            return

        if not self.is_valid_time(time):
            self.show_error_popup("Invalid time format. Use HH:MM.")
            return
        if any(event.title == title for event in self.events):
            self.show_error_popup("Event title already exists.")
            return

        new_event = Event(title, description, date, time)
        self.events.append(new_event)
        self.events.sort(key=lambda x: (x.date, x.time))  # Sort by date, then time
        self.update_event_list()
        self.clear_inputs()

    def delete_event(self, instance):
        title_to_delete = self.delete_title_input.text.strip()
        if not title_to_delete:
            self.show_error_popup("Please enter the title of the event to delete.")
            return

        for event in self.events:
            if event.title == title_to_delete:
                self.events.remove(event)
                self.update_event_list()
                return

        self.show_error_popup("Event not found.")

    def is_valid_date(self, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def is_valid_time(self, time):
        try:
            datetime.strptime(time, '%H:%M')
            return True
        except ValueError:
            return False

    def update_event_list(self):
        self.event_list_layout.clear_widgets()
        if not self.events:
            no_events_label = Label(text="No events to display", size_hint_y=None, height=dp(40))
            self.event_list_layout.add_widget(no_events_label)
            return
        
        for event in self.events:
            event_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, None))
            event_layout.bind(minimum_height=event_layout.setter('height')) 

            title_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint=(1, None))
            title_layout.bind(minimum_height=title_layout.setter('height')) 
            title_label = Label(text=event.title , size_hint=(0.2, 1), halign='left')
            date_label = Label(text='Date: ' + event.date, size_hint=(0.4, 1))
            time_label = Label(text='Time: ' + event.time, size_hint=(0.4, 1))
            title_layout.add_widget(title_label)
            title_layout.add_widget(date_label)
            title_layout.add_widget(time_label)
            event_layout.add_widget(title_layout)

            description_label = Label(text='event Information: ' + event.description, size_hint=(0.9, None), padding=(50,10),halign='left',text_size=(self.width - dp(20), None))
            event_layout.add_widget(description_label)

            self.event_list_layout.add_widget(event_layout)

    def show_error_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()
        
    def clear_inputs(self):
        self.title_input.text = ''
        self.description_input.text = ''
        self.date_input.text = ''
        self.time_input.text = ''
