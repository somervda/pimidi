#!/usr/bin/python3

# Main wrapper for py_midi, ssd1306, mcp4725 and GPIO functionality
import json
import math


class MidiIO:
    MIDINOTE127 = 12543.85

    def __init__(self):
        # Load pimidi.config (json file)
        try:
            with open('settings.json') as settings_file:
                self.settings = json.load(settings_file)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.strerror, e.filename))
        self.cvSettup()

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

    @property
    def midi_display(self):
        return self.settings["midi"]["display"]

    @property
    def midi_default_channel(self):
        return self.settings["midi"]["default_channel"]

# setters
    @cv_max_volts.setter
    def cv_max_volts(self, volts):
        if(volts >= 6):
            raise ValueError("Volts should never be more than 6 volts!")
        self.settings["cv"]["max_volts"] = volts

    @cv_midi_channel.setter
    def cv_midi_channel(self, channel):
        if(channel < 0 or channel > 15):
            raise ValueError("CV can only track midi channels 0 to 15")
        self.settings["cv"]["midi_channel"] = channel

    @cv_min_hertz.setter
    def cv_min_hertz(self, hertz):
        if(hertz < 8.16 or hertz > 13289.75):
            raise ValueError(
                "Midi only supports a frequency range of 8.16 to 13289.75 hertz")
        self.settings["cv"]["min_hertz"] = hertz

    @midi_display.setter
    def midi_display(self, display):
        self.settings["midi"]["display"] = display

    @midi_default_channel.setter
    def midi_default_channel(self, channel):
        if(channel < 0 or channel > 15):
            raise ValueError("Midi only supports channels 0 to 15")
        self.settings["midi"]["default_channel"] = channel

    def cvSettup(self):
        # etFreqStep is the ratio in hertz between 2 adjacent notes in the equal temperament scale (12th root of 2)
        self.etFreqRatio = math.pow(2, 1/12)

        # The ratio in hertz between 2 adjacent dac values going to logarithmic oscillators
        self.cvfreqRatio = math.pow(2, 1/(4095/self.cv_max_volts))
        self.cvMinHertzNoteAndOffset()
        print("self.cv_first_midi_note", self.cv_first_midi_note)
        print("self.dacOffset", self.dacOffset)

    def cvMinHertzNoteAndOffset(self):
        # Find the first midi note above the cv_min_hertz
        for note in range(127, 0, -1):
            noteHertz = self.getMidiNoteHertz(note)
            if (self.cv_min_hertz > noteHertz):
                break
        self.cv_first_midi_note = note + 1
        # Find the DAC value offset to that first note
        for dacOffset in range(0, int((4095/self.cv_max_volts)/12)+1, 1):
            if (self.cv_min_hertz * math.pow(self.cvfreqRatio, dacOffset)) >= self.getMidiNoteHertz(self.cv_first_midi_note):
                self.dacOffset = dacOffset
                break

    def getMidiNoteHertz(self, note):
        return self.MIDINOTE127/(math.pow(self.etFreqRatio, 127-note))

    def settingsPrint(self):
        print(self.settings)
