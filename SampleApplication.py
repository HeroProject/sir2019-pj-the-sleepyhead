import AbstractApplication as Base
import json
from textblob import TextBlob
import numpy as np
from threading import Semaphore
import random
import time


class SampleApplication(Base.AbstractApplication):

    # Pass the required Dialogflow parameters (add your Dialogflow parameters)
    def init_settings(self):
        """
        Initialize important settings
        """
        self.setDialogflowKey("nao-asipei-148b2e2fe841.json")
        self.setDialogflowAgent("nao-asipei")
        self.speed = "\\rspd=80\\"
        self.genreList = ["adventure", "mistery", "fantasy", "romance", "historical"]
        self.init_time = 0
        self.timing = 0

    # Make the robot ask the question, and wait until it is done speaking

    def init_locks(self):
        self.speechLock = Semaphore(0)
        self.nameLock = Semaphore(0)

    def init_stories(self):
        """
        Read the stories from the file "fables.json" and initialize the dataset.
        """
        with open("fables.json") as file:
            self.dataset = json.load(file)["stories"]

    def select_story(self, genre):
        """
        Initialize the story story given the genre

        Keyword arguments:
        Genre -- Genre of the story
        """
        genre = genre.lower()
        np.random.shuffle(self.dataset)
        for story in self.dataset:
            if story["genre"] == genre:
                self.story = story
                break
        self.blob = TextBlob(" ".join(self.story["story"]))
        self.sentences = self.blob.sentences
        processed_story = [
            " \\mrk=" + str(i + 2) + "\\ " + str(self.sentences[i]) for i in range(len(self.sentences))
        ]
        self.story["story"] = self.speed + "".join(processed_story)

    def init_gesture_list(self):
        """
        Initialize the gesture list from the dictionary
        """
        self.gesture_list = list(self.gesture_to_probability.keys())

    def init_gestures(self):
        """
        Initialize the Gestures dictionaries and categorize them in 5 categories that represent the sentiment.
        """
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
        """
        Initialize the LEDs dictionaries.
        """

        self.led_gesture = {
            "anger": "red",
            "surprise": "yellow",
            "disgust": "greenyellow",
            "sadness": "blue",
            "happiness": "green",
            "fear": "cyan",
            "neutral": "white",
        }
        self.emotion_to_led = {
            0: ["anger", "sadness"],
            1: ["disgust", "fear"],
            2: ["neutral"],
            3: ["surprise"],
            4: ["happiness"],
        }
        self.leds_to_emotion = {
            "anger": 2,
            "surprise": 3,
            "disgust": 1,
            "sadness": 0,
            "happiness": 4,
            "fear": 1,
            "neutral": 2,
        }

    def tell_stories(self, genre):
        """
        Command the robot to tell a story based on the genre

        Keyword arguments:
        Genre -- Genre of the story
        """

        # We have his name and the kind of story. Init story
        self.select_story(genre)
        # Get when we start telling the story
        # self.init_time = time.time()
        self.sayAnimated(self.speed + "The story I'm going to tell is " + self.story["title"])
        self.speechLock.acquire()
        for sent in self.sentences:
            # print(self.timing - self.init_time == 61)
            # if self.timing - self.init_time > 60:
            #     break
            processedsent = self.speed + sent.string
            print(processedsent)
            self.say(processedsent)
            gesture, led = self.chooseGesture(sent)
            print(gesture + "\n")
            self.doGesture(gesture)
            if not self.led_gestures[gesture]:
                self.setEyeColour(self.led_gesture[led])
                print(self.led_gesture[led])
            self.speechLock.acquire()
            # self.timing = time.time()

        self.sayAnimated(self.speed + "The moral of the story is " + self.story["moral"])
        self.speechLock.acquire()

    def chooseGesture(self, sentence):
        """
        Selects a gesture and LED color given the sentence.
        It analyzes the sentiment of the sentence and create a distribution
        to select the category over which the choose will be chosen

        Keyword arguments:
        Sentece -- Sentence of the story

        Returns a Gesture name and a LED color matching the sentiment
        """
        # Use an epsilon greedy policy kind of.
        # Meaning we will choose the given polarity a subjetivity porcent of the time.
        polarity, subjectivity = sentence.sentiment
        category = 0
        # Invert subjectivity
        # subjectivity = - subjectivity + 1

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

        variance = 1 * subjectivity / 5
        max_shift = np.max([abs(index - category) for index in range(len(categories_distribution))])
        min_shift = 1 if category == 0 or category == 4 else 2
        for index in range(len(categories_distribution)):
            shift = abs(index - category)
            if shift > 1:  # far from the choosen polarity.
                categories_distribution[index] -= variance * shift * 0.2
            elif min_shift == 2 and shift == 1:
                categories_distribution[index] += variance * (max_shift - shift) * 0.1
            else:
                categories_distribution[index] += variance * (max_shift - shift) * 0.2

        if (np.abs(1.0 - sum(categories_distribution))) > 0.00001:
            aux = (1.0 - sum(categories_distribution)) / 5
            categories_distribution = [x + aux for x in categories_distribution]

        # Allow changing category depending on subjectivity
        best_category = np.random.choice(np.arange(5), 1, p=categories_distribution)[0]

        return (
            random.choice(self.sentiment_to_gesture[best_category]),
            random.choice(self.emotion_to_led[best_category]),
        )

    def main(self):
        self.init_stories()
        self.init_settings()
        self.init_gestures()
        self.init_gesture_list()
        self.init_leds_gestures()
        self.setLanguage("en-US")
        self.init_locks()

        self.sayAnimated("Hello, I am PJ! what is your name?")
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.name = None
        count = 0
        while not self.name and count < 2:
            count += 1
            self.setAudioContext("answer_name")
            self.startListening()
            self.nameLock.acquire(timeout=5)
            self.stopListening()
            if not self.name:  # wait one more second after stopListening (if needed)
                self.nameLock.acquire(timeout=1)

            # Respond and wait for that to finish
            if self.name:
                self.sayAnimated("Nice to meet you " + self.name + "!")
            else:
                if count < 2:
                    self.sayAnimated("Sorry, I didn't catch your name. Can you repeat it?")
                else:
                    self.sayAnimated("Sorry, I didn't catch your name, but I will tell you a story anyway")
                    self.name = ""
            self.speechLock.acquire()

        self.sayAnimated(
            self.speed
            + "Okay "
            + self.name
            + " What kind of story would you like to here tonight? Today I have Adventure, Mistery, Fantasy, Romance and Historical"
        )
        self.speechLock.acquire()

        count = 0
        self.genre = None
        while not self.genre and count < 2:
            count += 1
            self.setAudioContext("answer_genre")
            self.startListening()
            self.nameLock.acquire(timeout=5)
            self.stopListening()
            if not self.genre:  # wait one more second after stopListening (if needed)
                self.nameLock.acquire(timeout=1)

            # Respond and wait for that to finish
            if self.genre:
                self.sayAnimated(self.speed + "Okay," + self.genre + "it is!")
            else:
                if count < 2:
                    self.sayAnimated("Sorry, I didn't catch it. Can you repeat it?")
                else:
                    self.genre = random.choice(self.genreList)
                    self.sayAnimated(
                        self.speed
                        + "I didn't get it, so we are doing one of my favorite genres "
                        + self.genre
                    )
            self.speechLock.acquire()

        self.tell_stories(self.genre)

        self.setEyeColour("white")
        self.sayAnimated(
            self.speed + "Oh well, its getting late now, would you like me to tell you another story?"
        )
        self.speechLock.acquire()

        count = 0
        self.answer_exit = None
        while not self.answer_exit and count < 2:
            count += 1
            self.setAudioContext("answer_exit")
            self.startListening()
            self.nameLock.acquire(timeout=5)
            self.stopListening()
            if not self.answer_exit:  # wait one more second after stopListening (if needed)
                self.nameLock.acquire(timeout=1)

            yes_list = ["yes", "yeah", "sure"]
            # Respond and wait for that to finish
            if self.answer_exit:
                if self.answer_exit in yes_list:
                    self.sayAnimated(self.speed + "Okay, then I will tell you another story")
                    self.speechLock.acquire()
                    self.tell_stories(self.genre)
                    self.sayAnimated(self.speed + "And now, Good night and sweet dreams.")
                    self.doGesture("animations/Stand/Gestures/BowShort_1")
                    self.speechLock.acquire()
                else:
                    self.sayAnimated(self.speed + "Good night, sweet dreams")
                    self.doGesture("animations/Stand/Gestures/BowShort_1")
                    self.speechLock.acquire()
            else:
                if count < 2:
                    self.sayAnimated("Sorry, I didn't catch your answer. Can you repeat it?")
                else:
                    self.sayAnimated(self.speed + "I suppose you fell asleep.. Good night, sweet dreams")
                    self.doGesture("animations/Stand/Gestures/BowShort_1")
            self.speechLock.acquire()

    def onRobotEvent(self, event):
        if event == "TextDone":
            self.speechLock.release()

    def onAudioIntent(self, *args, intentName):
        if intentName == "answer_name" and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()
        elif intentName == "answer_genre" and len(args) > 0:
            self.genre = args[0]
            self.nameLock.release()
        elif intentName == "answer_exit" and len(args) > 0:
            self.answer_exit = args[0]
            self.nameLock.release()


# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
