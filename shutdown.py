from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

from sys import platform

if platform == 'win32':
	import subprocess
elif platform[:5] == 'linux':
	import os

	if os.geteuid() != 0:
		raise (EnvironmentError, 'Run as ROOT!')
else:
	raise (EnvironmentError, 'Unsupported system!')


Window.clearcolor = (1, 1, 1, 1)
Window.size = (300, 500)


class AppLayout(FloatLayout):
	def __init__(self, **kwargs):
		super(AppLayout, self).__init__(**kwargs)

		self.label = Label(
            text='sHutdown',
            color=[0,0,.65,1],
            size_hint=(.75,.3),
            pos_hint={'center_x':.5, 'center_y':.7},
            font_size=62
        )

		self.label2 = Label(
            text='Type below number of minutes',
            color=[0,0,0,.7],
            pos_hint={'center_x':.5, 'center_y':.5},
            font_size=11
        )

		self.button = Button(text='Start',
                             size_hint=(.5,.15),
                             pos_hint={'center_x':.5, 'center_y':.1},
                             color=(1,1,1,1),
                             background_color=(1,1,1,.6)
         )

		self.button.clock = False
		self.button.bind(on_release=self.buttonPress)

		self.textinput = TextInput(text='60',
                                   hint_text='min',
                                   multiline=False,
                                   input_filter='int',
                                   size_hint=(.5,.10),
                                   pos_hint={'center_x':.5, 'center_y':.4},
                                   font_size=35,
                                   cursor_color=[0,0,.65,1]
        )

		self.add_widget(self.label)
		self.add_widget(self.label2)
		self.add_widget(self.textinput)
		self.add_widget(self.button)

	def buttonPress(self, instance):
		self.button.clock = not self.button.clock

		if not self.textinput or int(self.textinput.text) < 1:
			self.button.clock = False
			self.textinput.text = 420
			pass

		if self.button.clock:
			self.button.text = 'Stop'
			self.clock = Clock.schedule_once(self.clock_callback, 60)
		else:
			self.button.text = 'Start'
			self.clock.cancel()

	def clock_callback(self, dt):
		_time = int(self.textinput.text)

		self.textinput.text = str(_time-1)
		self.clock = Clock.schedule_once(self.clock_callback, 60)

		if _time == 1:
			if platform == 'win32':
				subprocess.call(["shutdown.exe", "/s", "/f"])
			else:
				os.system("shutdown now -h")


class ShutDownApp(App):
	def build(self):
		return AppLayout()

if __name__ == '__main__':
	ShutDownApp().run()
