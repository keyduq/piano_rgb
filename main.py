import io
import time
import rtmidi
import serial
from colour import Color
from datetime import datetime

from mode_type import ModeType

midi_in = rtmidi.MidiIn()
midiout = rtmidi.MidiOut()
ser = serial.Serial('COM3', 9600)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
time.sleep(1)  # wait for arduino to initialize
last_color = None
black = Color("black")
mode = ModeType.SPECTRUM
hue_start = 80


def main():
  while True:
    connected = connect()
    if not connected:
      time.sleep(1)
      if last_color != black:
        send_color(black)
    else:
      available = True
      while available:
        available = check_piano_available()
        time.sleep(1)


def connect():
  try:
    midi_in.open_port(get_casio_input_port())
    midiout.open_port(get_output_port())
    midi_in.set_callback(replicate_midi)
    midi_in.set_error_callback(on_midi_error)
    return True
  except SystemError as err:
    print(f"{err=}")
    raise err
  except BaseException as err:
    if midi_in.is_port_open():
      midi_in.cancel_callback()
      midi_in.cancel_error_callback()
      midi_in.close_port()
    if midiout.is_port_open():
      midiout.close_port()
    return False


def send_color(color):
  global last_color
  color_merged = color if last_color is None else merge_colors(last_color, color)
  last_color = color_merged
  data = f'{str(int(color_merged.red * 255))},{str(int(color_merged.green * 255))},{str(int(color_merged.blue * 255))}\n'
  sio.write(data)
  sio.flush()


def on_midi_error(errtype, msg, data):
  print(errtype)
  print(msg)


def replicate_midi(data, _):
  msg = data[0]
  midiout.send_message(msg)
  if (msg[0] == 144):  # 144: key down, 128: key up
    key = msg[1] - 20
    if mode == ModeType.SPECTRUM:
      hue = key / 88
    elif mode == ModeType.COLOR_RANGE:
      hue = (hue_start + key / 2) / 360
    else:
      hue = key / 88
    color = Color(hue=hue, saturation=1, luminance=(40 + msg[2])/254)
    send_color(color)


def check_piano_available():
  try:
    available_input_ports = midi_in.get_ports()
    casio_match = [e for e in available_input_ports if "CASIO" in e]
    if (len(casio_match) == 0):
      return False
    return True
  except:
    return False


def get_casio_input_port():
  try:
    available_input_ports = midi_in.get_ports()
    casio_match = [e for e in available_input_ports if "CASIO" in e]
    return available_input_ports.index(casio_match[0])
  except:
    return None


def get_output_port():
  try:
    available_output_ports = midiout.get_ports()
    casio_match = [e for e in available_output_ports if "loopmidi" in e]
    return available_output_ports.index(casio_match[0])
  except:
    return None


def merge_colors(first: Color, second: Color):
  hue = (first.hue + second.hue) / 2
  luminance = second.luminance
  return Color(hue=hue, saturation=1, luminance=luminance)


if __name__ == '__main__':
  main()
