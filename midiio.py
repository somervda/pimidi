#!/usr/bin/python3

# Main wrapper for py_midi, ssd1306, mcp4725 and GPIO functionality
import json

class MidiIO:
  def __init__(self):
    # Load pimidi.config (json file)
    try:
        with open('settings.json') as settings_file:
            self.settings = json.load(settings_file)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.strerror, e.filename))

  def settingsSave(self):
    with open("settings.json", "w") as settings_file:
      json_settings = json.dumps(self.settings, indent=4)
      settings_file.write(json_settings)

# getters

  @property
  def cv_max_volts(self): 
      return self.settings["cv"]["max_volts"]
  
  @property
  def cv_midi_channel(self): 
      return self.settings["cv"]["midi_channel"]
  
  @property
  def cv_min_hertz(self): 
      return self.settings["cv"]["min_hertz"]

# setters
  @cv_max_volts.setter 
  def cv_max_volts(self, volts): 
      if(volts >= 6): 
        raise ValueError("Volts should never be more than 6 volts!") 
      self.settings["cv"]["max_volts"]=volts

  @cv_midi_channel.setter
  def cv_midi_channel(self, channel): 
      if(channel < 0 or channel > 15): 
        raise ValueError("CV can only track midi channels 0 to 15") 
      self.settings["cv"]["midi_channel"]=channel

  @cv_min_hertz.setter
  def cv_min_hertz(self, hertz): 
      if(hertz < 8.16 or hertz > 13289.75): 
        raise ValueError("Midi only supports a frequency range of 8.16 to 13289.75 hertz") 
      self.settings["cv"]["min_hertz"]=hertz

  def settingsPrint(self):
    print(self.settings)