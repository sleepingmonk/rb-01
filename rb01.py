from pyPS4Controller.controller import Controller
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

#forward
GPIO.output(36, 1)
GPIO.output(38, 0)

GPIO.output(35, 1)
GPIO.output(37, 0)

pl = GPIO.PWM(33, 50)
pr = GPIO.PWM(40, 50)

pl.start(0)
pr.start(0)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_triangle_press(self):
      pl.ChangeDutyCycle(70)
      pr.ChangeDutyCycle(70)

    def on_triangle_release(self):
      pl.ChangeDutyCycle(0)
      pr.ChangeDutyCycle(0)

    def on_L1_press(self):
      pl.stop()
      pr.stop()

      GPIO.cleanup()

print("Listening...")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.debug = True
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)



# pl.ChangeDutyCycle(85)
# pr.ChangeDutyCycle(85)
# time.sleep(10)
# pl.ChangeDutyCycle(100)
# pr.ChangeDutyCycle(100)
# time.sleep(10)

