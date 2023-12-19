import time
import RPi.GPIO as GPIO
import threading
from picamera import PiCamera
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Label


GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT) #motor pins
GPIO.setup(27,GPIO.OUT) 
GPIO.setup(22,GPIO.OUT) 
GPIO.setup(23,GPIO.OUT)

GPIO.setup(5, GPIO.OUT) # Red 1 
GPIO.setup(6, GPIO.OUT) # Green 1
GPIO.setup(13, GPIO.OUT) # Blue 1

GPIO.setup(19, GPIO.OUT) # Red 2
GPIO.setup(26, GPIO.OUT) # Green 2
GPIO.setup(25, GPIO.OUT) # Blue 2

GPIO.setup(12, GPIO.OUT) # Red 3
GPIO.setup(16, GPIO.OUT) # Green 3
GPIO.setup(20, GPIO.OUT) # Blue 3


LED1 = [5,6,13]
LED2 = [19,26,25]
LED3 = [12,16,20]

def camera():

    camera = PiCamera()
    camera.resolution = (1920,1080)
    camera.exposure_mode = 'night'
    camera.start_preview()
    camera.capture()
    time.sleep(3)
    camera.stop_preview()
    camera.close()

def camera_picture():

    camera = PiCamera()
    camera.resolution = (1920,1080)
    camera.exposure_mode = 'night'
    camera.start_preview()
    time.sleep(3)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
    camera.close()
    

def camera_video():

    camera = PiCamera()
    camera.resolution = (1920,1080)
    camera.exposure_mode = 'night'
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/video.h264')
    time.sleep(20)
    camera.stop_recording()
    camera.stop_preview()
    camera.close()

def RGB_sequence():

    t = 0.5
    
    #for i in range(10):
      #  rgb_color(0,0,255,LED1, t)
     #   time.sleep(0.3)
      #  t = t + 0.5

    rgb_color(0,0,255,LED2, 1)
    rgb_color(255,0,0,LED3, 1) #reverse order
    rgb_color(0,0,255,LED1, 1)
    rgb_color(255,0,0,LED3, 1)
    rgb_color(0,0,255,LED2, 1)

    time.sleep(2)

    rgb_color(200,0,0,LED2, 0.5)
    time.sleep(0.2)
    rgb_color(230,0,0,LED2, 0.7)
    time.sleep(0.2)
    rgb_color(240,0,0,LED2, 1)
    time.sleep(0.2)
    rgb_color(255,0,0,LED2, 2)

    rgb_color(0,255,200,LED2, 1)
    rgb_color(255,0,0,LED3, 1) #reverse order
    rgb_color(0,0,255,LED1, 1)
    rgb_color(255,0,0,LED3, 1)
    rgb_color(0,0,255,LED2, 1)

    time.sleep(2)

    rgb_color(0,255,200,LED2, 1)
    rgb_color(255,0,0,LED3, 1) #reverse order
    rgb_color(0,0,255,LED1, 1)
    rgb_color(255,0,0,LED3, 1)
    rgb_color(0,0,255,LED2, 1)

    time.sleep(2)

    rgb_color(125,0,255,LED2, 1)
    rgb_color(255,0,0,LED3, 1) #reverse order
    rgb_color(0,0,255,LED1, 1)
    rgb_color(255,0,0,LED3, 1)
    rgb_color(0,0,255,LED2, 1)


def rgb_color(r,g,b,LED, sleepy): #I added a sleep time varaible for different sleep lengths
    R = r/255
    G = g/255
    B = b/255

    red = GPIO.PWM(LED[0],100)
    red.start(R)
    green = GPIO.PWM(LED[1],100)
    green.start(G) 
    blue = GPIO.PWM(LED[2],100)
    blue.start(B)

    time.sleep(sleepy)

dt = 0.02 #sleep time between steps

#define function to execute a single step
def step(a1, a2, b1, b2): 
    GPIO.output(17, a1)
    GPIO.output(27, b1)
    GPIO.output(22, a2)
    GPIO.output(23, b2)
    time.sleep(dt)

#next, define functions to execute rotations
def full_C(): #full clockwise
    step(1,0,0,1)
    step(1,1,0,0)
    step(0,1,1,0)
    step(0,0,1,1)

def full_CC(): #full counterclockwise 
    step(0,0,1,1)
    step(0,1,1,0)
    step(1,1,0,0)
    step(1,0,0,1)

def half_C(): #half clockwise
    step(1,0,0,1)
    step(1,0,0,0)
    step(1,1,0,0)
    step(0,1,0,0)
    step(0,1,1,0)
    step(0,0,1,0)
    step(0,0,1,1)
    step(1,0,0,0)

def half_CC(): #half counterclockwise
    step(1,0,0,0)
    step(0,0,1,1)
    step(0,0,1,0)
    step(0,1,1,0)
    step(0,1,0,0)
    step(1,1,0,0)
    step(1,0,0,0)
    step(1,0,0,1)


def spin_motor():
    N = 10000 #number of loop iterations
    for _ in range(N): 
        full_C()


def preset():
    t1 = threading.Thread(target=RGB_sequence)
    t2 = threading.Thread(target=spin_motor)
    t3 = threading.Thread(target=camera)

    t1.start()
    t2.start()
    t3.start()
        

def main():

    window = tk.Tk()

    window.title("Tiger Eye Discomneme")

    window.geometry("1000x700")

    label = tk.Label(window, text="Tiger Eye", font=('Times', 48)).place(
        relx=0.5, rely=0.37, anchor="center")

    labelk = tk.Label(window, text="Kaleidomneme").place(
        relx=0.5, rely=0.45, anchor="center")

    enter = tk.Button(window, text='Jungle Book',command=preset).place(
        relx=0.5, rely=0.55, anchor="center")
    
    picture = tk.Button(window, text='Snapshot',command=camera_picture).place(relx=0.40, rely=0.58)

    video = tk.Button(window, text="Video",command=camera_video).place(relx=0.52, rely=0.58)

    exit = tk.Button(window, text='Exit', command=window.destroy).place(
        relx=0.5, rely=0.66, anchor="center")

    window.mainloop()


if __name__ == "__main__":

    main()

GPIO.cleanup()
