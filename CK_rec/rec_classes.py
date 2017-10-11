import mido
from mido import Message, MidiFile, MidiTrack

# Class for handling the recording
"""
@port is the midi input port
@device_id is the id passed for note-on messages (sometimes keyboards pass note-off as a different id or as velocity=0)
@tempo is the bpm tempo for the midi recording *** HAS TO BE SET **
@debug is for posting messages on console or not

"""
class CK_rec(object):
    def __init__(self, port, device_id, tempo=120, debug=True):
        self.port = port
        self.tempo = tempo
        self.debug = debug
        self.on_id = device_id
        self.__mid = MidiFile()
        self.__track = MidiTrack()
        self.prepareTrack()

    def prepareTrack(self):
        print("\nCodeKlavier is ready and ON.")
        input("Press [ENTER] to start recording...")
        print("You are now RECORDING")
        print("\nPress Control-C to stop the recording.\n")
        self.__mid.tracks.append(self.__track)

    def __call__(self, event, data=None):
        message, deltatime = event
        if message:
            miditime = int(round(mido.second2tick(deltatime, self.__mid.ticks_per_beat, mido.bpm2tempo(self.tempo))))
            if self.debug:
                print('deltatime: ', deltatime, 'msg: ', message)
            if message[0] == self.on_id:
                self.__track.append(Message('note_on', note=message[1], velocity=message[2], time=miditime))
            else:
                # print("note off!")
                self.__track.append(Message('note_off', note=message[1], velocity=message[2], time=miditime))

    def saveTrack(self, name):
        self.__mid.save('Recordings/'+name+'.mid')
        print("\nRecording saved as "+name+".mid in the Recordings folder\n")
