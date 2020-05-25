from pyPS4Controller.controller import Controller, Event
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#left
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

#right
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)


pl = GPIO.PWM(33, 50)
pr = GPIO.PWM(40, 50)

pl.start(0)
pr.start(0)

class MyEventDefinition(Event):

    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    # each overloaded function, has access to:
    # - self.button_id
    # - self.button_type
    # - self.value
    # use those variables to determine which button is being pressed
    def x_pressed(self):
        return self.button_id == 0 \
            and self.button_type == 1\
            and self.value == 1

    def x_released(self):
        return self.button_id == 0 \
            and self.button_type == 1 \
            and self.value == 0

    def circle_pressed(self):
        return self.button_id == 1 \
            and self.button_type == 1 \
            and self.value == 1

    def circle_released(self):
        return self.button_id == 1 \
            and self.button_type == 1 \
            and self.value == 0

    def triangle_pressed(self):
        return self.button_id == 2 \
            and self.button_type == 1 \
            and self.value == 1

    def triangle_released(self):
        return self.button_id == 2 \
            and self.button_type == 1 \
            and self.value == 0

    def square_pressed(self):
        return self.button_id == 3 \
            and self.button_type == 1 \
            and self.value == 1

    def square_released(self):
        return self.button_id == 3 \
            and self.button_type == 1 \
            and self.value == 0


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.bearingl = 0
        self.bearingr = 0
        self.maxStick = 32767
        self.limitMax = 88
        self.limitMin = 50

    def on_triangle_press(self):
        #forward
        GPIO.output(36, 1)
        GPIO.output(38, 0)
        GPIO.output(35, 1)
        GPIO.output(37, 0)
        pl.ChangeDutyCycle(self.limitMax)
        pr.ChangeDutyCycle(self.limitMax)

    def on_triangle_release(self):
        pl.ChangeDutyCycle(0)
        pr.ChangeDutyCycle(0)

    def on_x_press(self):
        #forward
        GPIO.output(36, 0)
        GPIO.output(38, 1)
        GPIO.output(35, 0)
        GPIO.output(37, 1)
        pl.ChangeDutyCycle(self.limitMax)
        pr.ChangeDutyCycle(self.limitMax)

    def on_x_release(self):
        pl.ChangeDutyCycle(0)
        pr.ChangeDutyCycle(0)

    def on_L3_up(self, value):
        GPIO.output(36, 1)
        GPIO.output(38, 0)
        GPIO.output(35, 1)
        GPIO.output(37, 0)
        drive = (abs(value) / self.maxStick) \
            * (self.limitMax - self.limitMin) \
            + self.limitMin
        dutyl = drive - self.bearingl if drive - self.bearingl > 0 else 0
        dutyr = drive - self.bearingr if drive - self.bearingr > 0 else 0
        print("\n\nup: ", value)
        print("drive: ", drive)
        print("left: ", self.bearingl)
        print("right: ", self.bearingr)
        print("dutyl: ", dutyl)
        print("dutylr: ", dutyr)
        pl.ChangeDutyCycle(dutyl)
        pr.ChangeDutyCycle(dutyr)

    def on_L3_down(self, value):
        GPIO.output(36, 0)
        GPIO.output(38, 1)
        GPIO.output(35, 0)
        GPIO.output(37, 1)
        drive = (abs(value) / self.maxStick) \
            * (self.limitMax - self.limitMin) \
            + self.limitMin
        dutyl = drive - self.bearingl if drive - self.bearingl > 0 else 0
        dutyr = drive - self.bearingr if drive - self.bearingr > 0 else 0
        print("\n\ndown: ", value)
        print("drive: ", drive)
        print("left: ", self.bearingl)
        print("right: ", self.bearingr)
        print("dutyl: ", dutyl)
        print("dutylr: ", dutyr)
        pl.ChangeDutyCycle(dutyl)
        pr.ChangeDutyCycle(dutyr)

    def on_L3_left(self, value):
        self.bearingl = (abs(value) / self.maxStick) \
            * (self.limitMax - self.limitMin) \
            + self.limitMin
        self.bearingr = 0
        print("\n\nleft: ", value)
        print("bearingl: ", self.bearingl)
        print("bearingr: ", self.bearingr)

    def on_L3_right(self, value):
        self.bearingl = 0
        self.bearingr = (abs(value) / self.maxStick) \
            * (self.limitMax - self.limitMin) \
            + self.limitMin
        print("\n\nright: ", value)
        print("bearingl: ", self.bearingl)
        print("bearingr: ", self.bearingr)

    def on_playstation_button_press(self):
        pl.stop()
        pr.stop()

        GPIO.cleanup()

        print("\n\n\n************ GPIO Cleaned up. Ready to exit. "
              "(Ctrl-c)***************\n\n\n")

        raise SystemExit

print("Listening...")

controller = MyController(interface="/dev/input/js0",
                          connecting_using_ds4drv=False,
                          event_definition=MyEventDefinition)

# controller.debug = True
# you can start listening before controller is paired, as long as you pair it
# within the timeout window
controller.listen(timeout=60)



# pl.ChangeDutyCycle(85)
# pr.ChangeDutyCycle(85)
# time.sleep(10)
# pl.ChangeDutyCycle(100)
# pr.ChangeDutyCycle(100)
# time.sleep(10)
