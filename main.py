from time import sleep
from gpiozero import AngularServo, Buzzer

# ======================
# GPIO PINS
# ======================

DISPENSING_SERVO_PIN = 17
DOOR_SERVO_PIN = 27
BUZZER_PIN = 22



CENTER = 90
RIGHT = 180
LEFT = 0

DOOR_CLOSED = 90
DOOR_OPEN = 0


HOLD_TIME = 1
COOLDOWN_TIME = 10

next_direction = "right"



dispensing_servo = AngularServo(
    DISPENSING_SERVO_PIN,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
)

door_servo = AngularServo(
    DOOR_SERVO_PIN,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
)

buzzer = Buzzer(BUZZER_PIN)




def move_center():
    dispensing_servo.angle = CENTER


def move_right():
    dispensing_servo.angle = RIGHT


def move_left():
    dispensing_servo.angle = LEFT


def open_door():
    door_servo.angle = DOOR_OPEN


def close_door():
    door_servo.angle = DOOR_CLOSED


def alarm():
    for _ in range(3):
        buzzer.on()
        sleep(0.2)
        buzzer.off()
        sleep(0.2)


def dispense():
    global next_direction

    alarm()

    if next_direction == "right":
        move_right()
        next_direction = "left"
    else:
        move_left()
        next_direction = "right"

    open_door()

    sleep(HOLD_TIME)

    close_door()
    move_center()

    sleep(COOLDOWN_TIME)



try:
    move_center()
    close_door()

    sleep(1)

    print("Ready. Press Enter to dispense.")

    while True:
        input()
        dispense()

except KeyboardInterrupt:
    print("Stopping...")

finally:
    close_door()
    move_center()

    sleep(0.5)

    dispensing_servo.close()
    door_servo.close()
    buzzer.close()