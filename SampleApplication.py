import AbstractApplication as Base
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
            "animations/Stand/Emotions/Negative/Fearful_1": -2,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_18": -1,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_01": 0,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_03": 1,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_11": 1,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_17": 1,
            "animations/Stand/Emotions/Positive/Proud_2": 2,
            "animations/Stand/Emotions/Positive/Confident_1": 2,
            "animations/Stand/Exclamation/NAO/Center_Neutral_EXC_01": 1,
            "animations/Stand/Exclamation/NAO/Right_Strong_EXC_04": 2,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_5": 1,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_4": 0,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_05": -2,
            "animations/Stand/Self & others/NAO/Center_Neutral_SAO_03": 0,
            "animations/Stand/Gestures/Explain_4": 0,
            "animations/Stand/Gestures/Explain_1": 0,
            "animations/Stand/Emotions/Positive/Happy_4": 1,
            "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_01": 0,
            "animations/Stand/Gestures/Explain_9": 0,
            "animations/Stand/Gestures/Explain_8": 0,
            "animations/Stand/Negation/NAO/Center_Strong_NEG_01": 1,
            "animations/Stand/Negation/NAO/Center_Strong_NEG_05": -2,
            "animations/Stand/Self & others/NAO/Left_Neutral_SAO_01": 0,
            "animations/Stand/Self & others/NAO/Left_Neutral_SAO_02": 1,
            "animations/Stand/Self & others/NAO/Left_Strong_SAO_02": 1,
            "animations/Stand/Space & time/NAO/Right_Slow_SAT_01": 1,
            "animations/Stand/Exclamation/NAO/Left_Strong_EXC_03": 2,
            "animations/Stand/Gestures/Desperate_5": -2,
            "animations/Stand/Gestures/Desperate_2": -1,
            "animations/Stand/Emotions/Positive/Excited_1": 2,
            "animations/Stand/Gestures/You_3": 0,
            "animations/Stand/Emotions/Negative/Disappointed_1": -2,
            "animations/Stand/Negation/NAO/Right_Strong_NEG_01": -1,
            "animations/Stand/Emotions/Negative/Frustrated_1": -2,
            "animations/Stand/Gestures/Explain_3": 0,
            "animations/Stand/BodyTalk/Speaking/BodyTalk_2": 0,
            "animations/Stand/Gestures/Desperate_1": -2,
            "animations/Stand/Emotions/Positive/Sure_1": -1,
        }

        self.sentiment_to_gesture = {
            0: [
                "animations/Stand/Emotions/Negative/Fearful_1",
                "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_05",
                "animations/Stand/Negation/NAO/Center_Strong_NEG_05",
                "animations/Stand/Gestures/Desperate_5",
                "animations/Stand/Emotions/Negative/Disappointed_1",
                "animations/Stand/Emotions/Negative/Frustrated_1",
                "animations/Stand/Gestures/Desperate_1",
            ],
            1: [
                "animations/Stand/BodyTalk/Speaking/BodyTalk_18",
                "animations/Stand/Gestures/Desperate_2",
                "animations/Stand/Negation/NAO/Right_Strong_NEG_01",
                "animations/Stand/Emotions/Positive/Sure_1",
            ],
            2: [
                "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_01",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_4",
                "animations/Stand/Self & others/NAO/Center_Neutral_SAO_03",
                "animations/Stand/Gestures/Explain_4",
                "animations/Stand/Gestures/Explain_1",
                "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Strong_AFF_01",
                "animations/Stand/Gestures/Explain_9",
                "animations/Stand/Gestures/Explain_8",
                "animations/Stand/Self & others/NAO/Left_Neutral_SAO_01",
                "animations/Stand/Gestures/You_3",
                "animations/Stand/Gestures/Explain_3",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_2",
            ],
            3: [
                "animations/Stand/BodyTalk/BodyLanguage/NAO/Center_Slow_AFF_03",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_11",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_17",
                "animations/Stand/Exclamation/NAO/Center_Neutral_EXC_01",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_5",
                "animations/Stand/Emotions/Positive/Happy_4",
                "animations/Stand/Negation/NAO/Center_Strong_NEG_01",
                "animations/Stand/Self & others/NAO/Left_Neutral_SAO_02",
                "animations/Stand/Self & others/NAO/Left_Strong_SAO_02",
                "animations/Stand/Space & time/NAO/Right_Slow_SAT_01",
            ],
            4: [
                "animations/Stand/Emotions/Positive/Proud_2",
                "animations/Stand/Emotions/Positive/Confident_1",
                "animations/Stand/Exclamation/NAO/Right_Strong_EXC_04",
                "animations/Stand/Exclamation/NAO/Left_Strong_EXC_03",
                "animations/Stand/Emotions/Positive/Excited_1",
            ],
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
            "anger": -1,
            "surprise": 1,
            "disgust": -1,
            "sadness": -1,
            "happiness": 2,
            "fear": -1,
            "neutral": 0,
        }

        # does it make sense to use linear regression?

    def chooseGesture(self, sentence, policy=random):
        # Use an epsilon greedy policy. Meaning we will choose the given polarity a subjetivity porcent of the time.
        polarity, subjectivity = sentence.sentiment
        category = 0
        # Invert subjectivity
        subjectivity = - subjectivity + 1

        # Assign category depending on sentiment
        if polarity > 0.7:  # Very positive
            category = 4
        elif polarity < -0.7:  # Very negative
            category = 0
        elif polarity > 0.2 and polarity < 0.7:  # Positive
            category = 3
        elif polarity < -0.2 and polarity > -0.7:  # Negative
            category = 1
        else:  # Neutral
            category = 2

        categories_distribution = np.ones(5, dtype=float) * subjectivity / 5
        categories_distribution[category] += 1 - subjectivity
        # categories_distribution[category] += 1 - subjectivity / 3
        # categories_distribution[category] += 1 - subjectivity / 3

        # Allow changing category depending on subjectivity

        best_category = np.random.choice(np.arange(5), 1, p=categories_distribution)[0]

        return random.choice(self.sentiment_to_gesture[best_category])

    def main(self):
        self.init_stories(36)
        self.init_gestures()
        self.init_gesture_list()
        self.init_leds_gestures()
        self.setLanguage("en-US")
        self.init_locks()

        # very_bad = [x for x in self.gesture_to_probability if self.gesture_to_probability[x] == -2]
        # bad = [x for x in self.gesture_to_probability if self.gesture_to_probability[x] == -1]
        # neutral = [x for x in self.gesture_to_probability if self.gesture_to_probability[x] == 0]
        # good = [x for x in self.gesture_to_probability if self.gesture_to_probability[x] == 1]
        # very_good = [x for x in self.gesture_to_probability if self.gesture_to_probability[x] == 2]
        # print(very_bad)
        # print(bad)
        # print(good)
        # print(very_good)
        # print(neutral)

        for sent in self.sentences:
            processedsent = "\\rspd=80\\" + sent.string
            print(processedsent)
            # self.say(processedsent)
            gesture = self.chooseGesture(sent)
            # self.doGesture(gesture)
            # self.speechLock.acquire()
            print(gesture + "\n")

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
