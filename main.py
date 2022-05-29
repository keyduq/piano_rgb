import rtmidi
import math
import PySimpleGUI as sg
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from colored import fg, bg, attr


midi_in = rtmidi.MidiIn()
midiout = rtmidi.MidiOut()
# print(midi_in.get_ports())
midi_in.open_port(0)
# print(midiout.get_ports())
midiout.open_port(2)

class PianoWidget(Widget):
  rgba = ListProperty([0.3, 0.5, 1, 1])
  def __init__(self, **kwargs):
    super(PianoWidget, self).__init__(**kwargs)
    midi_in.set_callback(self.replicate_midi)
  
  def on_touch_down(self, _):
    self.rgba = [1, 0, 0, 1]
    return True
  
  def replicate_midi(self, data, _):
    msg = data[0]
    midiout.send_message(msg)
    if (msg[0] == 144): # 144: key down, 128: key up
      self.rgba = [0, msg[1] * 2 / 255, 0, msg[2]/128]
    print(msg)

class PianoApp(App):
  title = 'Piano color'
  piano_widget = PianoWidget()

  def build(self):
    return PianoWidget()


# def main():
#   print(midi_in.get_ports())
#   midi_in.open_port(0)

#   print(midiout.get_ports())
#   midiout.open_port(2)

#   midi_in.set_callback(replicate_midi)

#   while True:
#     event, values = window.read()
#     if event == 'OK' or event == sg.WIN_CLOSED:
#       break;
#   window.close()

if __name__ == '__main__':
  PianoApp().run()
  # main()