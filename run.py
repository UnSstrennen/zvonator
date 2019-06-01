from sys import argv
from main import config
from time import sleep
from playsound import playsound


SOUND_DIRECTORY = config['play_settings']['sound_directory']


class Amplifier:
    def __init__(self):
        self.delay_before_using = config['amplifier']['boot_duration']
        self.port = config['amplifier']['port']

    def on(self):
        with open(self.port, 'wb') as lpt:
            lpt.write(b'\xff')
            sleep(self.delay_before_using)

    def off(self):
        with open(self.port, 'wb') as lpt:
            lpt.write(b'\x00')


amplifier = Amplifier()

to_play = argv[1:]  # arguments given in cmd are paths to sounds to play

amplifier.on()
for path in to_play:
    playsound(SOUND_DIRECTORY + path)
    # if current sound is last sound - do not make a delay
    last = to_play[-1] == path
    if not last:
        sleep(config['play_settings']['delay_between_tracks'])
amplifier.off()
