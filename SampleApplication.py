import AbstractApplication as Base
import spacy
import json
from textblob import TextBlob
import numpy as np
from threading import Semaphore
import random


class SampleApplication(Base.AbstractApplication):
    def init_locks(self):
        self.speechLock = Semaphore(0)

    def init_stories(self, id=10):
        with open("aesopFables.json") as file:
            dataset = json.load(file)["stories"]
        self.story = dataset[id]
        self.blob = TextBlob(" ".join(self.story["story"]))
        self.sentences = self.blob.sentences
        processed_story = [
            " \\mrk=" + str(i + 2) + "\\ " + str(self.sentences[i]) for i in range(len(self.sentences))
        ]

        self.story["story"] = "\\rspd=80\\" + "".join(processed_story)

    def init_gesture_list(self):
        self.gesture_list = list(self.gesture_to_probability.keys())

    def init_gestures(self):
        self.gesture_to_probability = {
            "animations/Stand/Emotions/Negative/Fearful_1": [-0.718, 0.6],
            "animations/Stand/BodyTalk/Speaking/BodyTalk_18": [-0.3, 0.7],
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_01": [0.1, 0.8],
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_03": [0.5, 0.6],
            "animations/Stand/BodyTalk/Speaking/BodyTalk_11": [0.5, 0.6],
            "animations/Stand/BodyTalk/Speaking/BodyTalk_17": [0.5, 0.8],
            "animations/Stand/Emotions/Positive/Proud_2": [0.8, 0.85],
            "animations/Stand/Emotions/Positive/Confident_1": [0.85, 0.87],
            "animations/Stand/Exclamation/NAO/Center_Neutral_EXC_01": [0.46, 0.7],
            "animations/Stand/Exclamation/NAO/Right_Strong_EXC_04": [0.85, 0, 8],
            "animations/Stand/BodyTalk/Speaking/BodyTalk_5": [0.56, 0.67],
            "animations/Stand/BodyTalk/Speaking/BodyTalk_4": [0.1, 0.89],
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_05": [-0.9, 0.87],
            "animations/Stand/Self & others/NAO/Center_Neutral_SAO_03": [0, 0.75],
            "animations/Stand/Gestures/Explain_4": [0, 0.75],
            "animations/Stand/Gestures/Explain_1": [0, 0.75],
            "animations/Stand/Emotions/Positive/Happy_4": [0.85, 0.87],
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_01": [0, 0.75],
            "animations/Stand/Gestures/Explain_9": [0, 0.75],
            "animations/Stand/Gestures/Explain_8": [0, 0.75],
            "animations/Stand/Negation/NAO/Center_Strong_NEG_01": [0.67, 0.55],
            "animations/Stand/Negation/NAO/Center_Strong_NEG_05": [-0.7, 0.67],
            "animations/Stand/Self & others/NAO/Left_Neutral_SAO_01": [0, 0.75],
            "animations/Stand/Self & others/NAO/Left_Neutral_SAO_02": [0.55, 0.75],
            "animations/Stand/Self & others/NAO/Left_Strong_SAO_02": [0.55, 0.75],
            "animations/Stand/Space & time/NAO/Right_Slow_SAT_01": [0.55, 0.75],
            "animations/Stand/Exclamation/NAO/Left_Strong_EXC_03": [0.85, 0.87],
            "animations/Stand/Gestures/Desperate_5": [-0.7, 0.67],
            "animations/Stand/Gestures/Desperate_2": [-0.3, 0.7],
            "animations/Stand/Emotions/Positive/Excited_1": [0.85, 0.87],
            "animations/Stand/Gestures/You_3": [0, 0.75],
            "animations/Stand/Emotions/Negative/Disappointed_1": [-0.9, 0.87],
            "animations/Stand/Negation/NAO/Right_Strong_NEG_01": [-0.3, 0.7],
            "animations/Stand/Emotions/Negative/Frustrated_1": [-0.7, 0.67],
            "animations/Stand/Gestures/Explain_3": [0, 0.75],
            "animations/Stand/BodyTalk/Speaking/BodyTalk_2": [0, 0.75],
            "animations/Stand/Gestures/Desperate_1": [-0.9, 0.87],
            "animations/Stand/Emotions/Positive/Sure_1": [-0.3, 0.7],
        }

        self.led_gestures = {
            "animations/Stand/Emotions/Negative/Fearful_1": True,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_18": False,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_01": False,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_03": False,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_11": False,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_17": False,
            "animations/Stand/Emotions/Positive/Proud_2": True,
            "animations/Stand/Emotions/Positive/Confident_1": True,
            "animations/Stand/Exclamation/NAO/Center_Neutral_EXC_01": False,
            "animations/Stand/Exclamation/NAO/Right_Strong_EXC_04": False,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_5": False,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_4": False,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_05": False,
            "animations/Stand/Self & others/NAO/Center_Neutral_SAO_03": False,
            "animations/Stand/Gestures/Explain_4": False,
            "animations/Stand/Gestures/Explain_1": False,
            "animations/Stand/Emotions/Positive/Happy_4": True,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_01": False,
            "animations/Stand/Gestures/Explain_9": False,
            "animations/Stand/Gestures/Explain_8": False,
            "animations/Stand/Negation/NAO/Center_Strong_NEG_01": False,
            "animations/Stand/Negation/NAO/Center_Strong_NEG_05": False,
            "animations/Stand/Self & others/NAO/Left_Neutral_SAO_01": False,
            "animations/Stand/Self & others/NAO/Left_Neutral_SAO_02": False,
            "animations/Stand/Self & others/NAO/Left_Strong_SAO_02": False,
            "animations/Stand/Space & time/NAO/Right_Slow_SAT_01": False,
            "animations/Stand/Exclamation/NAO/Left_Strong_EXC_03": False,
            "animations/Stand/Gestures/Desperate_5": True,
            "animations/Stand/Gestures/Desperate_2": True,
            "animations/Stand/Emotions/Positive/Excited_1": True,
            "animations/Stand/Gestures/You_3": False,
            "animations/Stand/Emotions/Negative/Disappointed_1": True,
            "animations/Stand/Negation/NAO/Right_Strong_NEG_01": False,
            "animations/Stand/Emotions/Negative/Frustrated_1": True,
            "animations/Stand/Gestures/Explain_3": False,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_2": False,
            "animations/Stand/Gestures/Desperate_1": True,
            "animations/Stand/Emotions/Positive/Sure_1": True,
        }

        self.neutral_gestures = [
            x for x in self.gesture_to_probability if np.argmax(self.gesture_to_probability[x]) == 2
        ]

    def init_leds_gestures(self):
        self.led_gesture = {
            "anger": "red",
            "surprise": "yellow",
            "disgust": "greenyellow",
            "sadness": "blue",
            "happiness": "green",
            "fear": "cyan",
            "neutral": "white",
        }
        self.leds_to_emotion = {
            "anger": [-0.5, 0.3],
            "surprise": [0.5, 0.6],
            "disgust": [-0.4, 0.4],
            "sadness": [-0.5, 0.3],
            "happiness": [1, 0.6],
            "fear": [-0.5, 0.4],
            "neutral": [0, 0.0],
        }

        # does it make sense to use linear regression?

    def chooseGesture(self, sentence, policy=random):
        # Use an epsilon greedy policy. Meaning we will choose the given polarity a subjetivity porcent of the time.
        return random.choice(self.gesture_list)

    def main(self):
        self.init_stories(36)
        self.init_gestures()
        self.init_gesture_list()
        self.init_leds_gestures()
        self.setLanguage("en-US")
        self.init_locks()

        for sent in self.sentences:
            processedsent = "\\rspd=80\\" + sent.string
            # print(processedsent)
            self.say(processedsent)
            gesture = self.chooseGesture(sent)
            self.doGesture(gesture)
            self.speechLock.acquire()
            # print(gesture + "\n")

        # SpaCy testing
        # nlp = spacy.load("en_core_web_sm")
        # doc = nlp(str(self.story))
        # entities = [(i, i.label_, i.label) for i in doc.ents]

        # print(entities)
        # self.sayAnimated(" \\rspd=85\\ \\mrk=1\\ " + str(self.story["title"]))
        # self.sayAnimated(str(self.story["story"]))
        # sleep(2)

    def onRobotEvent(self, event):
        if event == "TextDone":
            self.speechLock.release()


# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
