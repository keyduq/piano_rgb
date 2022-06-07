import io
from tabnanny import check
import time
import rtmidi
import serial
from colour import Color

midi_in = rtmidi.MidiIn()
midiout = rtmidi.MidiOut()
# print(midi_in.get_ports())
# print(midiout.get_ports())
ser = serial.Serial('COM3', 9600)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
time.sleep(1)  # wait for arduino to initialize
last_color = None
black = Color("black")


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
  last_color = color
  data = str(int(color.red * 255)) + ',' + str(int(color.green * 255)
                                               ) + ',' + str(int(color.blue * 255)) + "\n"
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
    hue = key / 88
    color = Color(hue=hue, saturation=1, luminance=msg[2]/254)
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


if __name__ == '__main__':
  main()
