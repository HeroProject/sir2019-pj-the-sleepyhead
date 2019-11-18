import AbstractApplication as Base
from textblob import TextBlob

class SampleApplication(Base.AbstractApplication):
    def main(self):
        text = "One fine day, Akbar lost his ring. When Birbal arrived in the court, Akbar told him \"I have lost my " \
               "ring. My father had given it to me as a gift. Please help me find it.\"  Birbal said, \'do not worry " \
               "your Majesty, I will find your ring right now.\' He said, \"Your Majesty the ring is here in this " \
               "court itself, it is with one of the courtiers. The courtier who has a straw in his beard has your " \
               "ring.\" The courtier who had the emperors ring was shocked and immediately moved his hand over his " \
               "beard. Birbal noticed this act of the courtier. He immediately pointed towards the courtier and " \
               "said, \"Please search this man. He has the emperors ring.\" Akbar could not understand how Birbal had" \
               " Managed to find the ring.  Birbal then told Akbar that a guilty person is always scared. Moral: A " \
               "Guilty Conscience need No Accuser."

        blob = TextBlob(text)

        self.setLanguage('en-US')
        # This loop breaks the arms gestures. We should add a lock for the "say" method
        for sentence in blob.sentences:
            self.say(str(text))
            gesture = self.chooseGesture(sentence.sentiment.polarity)
            self.doGesture(gesture)

    def onRobotEvent(self, event):
        print(event)

    # Basic animation selection, we can do better
    def chooseGesture(self, polarity):
        if polarity > 0.8:
            return "animations/Stand/Gestures/Enthusiastic_5"
        elif polarity > 0.6:
            return "animations/Stand/Gestures/Enthusiastic_4"
        elif polarity > 0.4:
            return "animations/Stand/Gestures/Yes_3"
        elif polarity > 0.2:
            return "animations/Stand/Gestures/Yes_2"
        elif polarity > 0:
            return "animations/Stand/Gestures/YouKnowWhat_1"
        elif polarity < 0 and polarity > -.2:
            return "animations/Stand/Gestures/YouKnowWhat_5"
        elif polarity < -.2 and polarity > -.4:
            return "animations/Stand/Gestures/Please_1"
        elif polarity < -.4 and polarity > -.6:
            return "animations/Stand/Gestures/No_3"
        elif polarity < -.6 and polarity > -.8:
            return "animations/Stand/Gestures/No_8"
        else:
            return "animations/Stand/Gestures/No_9"

# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
