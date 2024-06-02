from sequence import Sequence

o = Sequence(quiet=False)
o.sequenceFile = "metronome.abc"
o.repeat = True
o.bps = 60
o.transpose = 0
o.play()
