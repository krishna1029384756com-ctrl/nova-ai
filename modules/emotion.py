current_emotion = "😊 Happy"


def set_emotion(emotion):
    global current_emotion
    current_emotion = emotion
    print(f"[Emotion] {current_emotion}")


def get_emotion():
    return current_emotion