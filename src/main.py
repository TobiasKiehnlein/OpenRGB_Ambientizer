from config import Config
from screencapture import screen_recorder

test = Config().some_object.some_prop
screen_recorder.capture_screen().show()
print(test)
