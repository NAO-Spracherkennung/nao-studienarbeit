#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse


class SpeechDetector(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(SpeechDetector, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        # self.subscriber = self.memory.subscriber("SpeechDetected")
        self.subscriber = self.memory.subscriber("SoundDetected")
        self.subscriber.signal.connect(self.on_speech_detected)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        # self.speech_recognition = session.service("ALSpeechRecognition")
        self.speech_recognition = session.service("ALSoundDetection")
        self.speech_recognition.subscribe("SpeechDetector")

    def on_speech_detected(self, speech_detected):
        """
        Callback for event FaceDetected.
        """
        if speech_detected:  # only speak the first time a face appears
            print("I saw a face!")
            self.tts.say("Hello, you!")

    def onInput_onStart(self):
        self.isRunning = True
        self.ad = ALProxy("ALAudioDevice")
        self.addedPaths = [self.behaviorAbsolutePath()]
        for addedPath in self.addedPaths:
            sys.path.append(addedPath)
        from pydub import AudioSegment
        songPath = os.path.join(self.behaviorAbsolutePath(), "audio_file.wav")
        self.song = AudioSegment.from_wav(songPath)
        try:
            # here is important to note that the second parameter is contigus memory audio data!
            self.ad.sendLocalBufferToOutput(
                int(self.song.frame_count()), id(self.song._data))
        except Exception as e:
            self.log("error for buffer: " + str(e) + str(id(self.song.data)))
        self.onUnload()
        pass

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print("Starting SpeechDetector")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, stopping SpeechDetector")
            self.speech_recognition.unsubscribe("SpeechDetector")
            # stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["SpeechDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = SpeechDetector(app)
    human_greeter.run()
    # 168.254.64.15
