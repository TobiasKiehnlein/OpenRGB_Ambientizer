import time
from abc import ABC, abstractmethod

from PIL import Image, ImageGrab
from mss import mss


class ScreenCapture(ABC):

    @abstractmethod
    def capture_screen(self) -> Image.Image:
        pass


class MssScreenCapture(ScreenCapture):

    def capture_screen(self) -> Image.Image:
        # Capture entire screen
        with mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            # Convert to PIL/Pillow Image
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


class ImageGrabScreen(ScreenCapture):

    def capture_screen(self) -> Image.Image:
        return ImageGrab.grab()


def get_screen_recorder() -> ScreenCapture:
    mss_capture = MssScreenCapture()
    screen_grab = ImageGrabScreen()
    start = time.time_ns()
    mss_capture.capture_screen()
    mss_capture_delta = time.time_ns() - start
    start = time.time_ns()
    screen_grab.capture_screen()
    screen_grab_delta = time.time_ns() - start

    if screen_grab_delta > mss_capture_delta:
        _screen_recorder_instance = MssScreenCapture()
    else:
        _screen_recorder_instance = ImageGrabScreen()
    return _screen_recorder_instance


screen_recorder: ScreenCapture = get_screen_recorder()
