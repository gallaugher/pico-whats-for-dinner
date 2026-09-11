# whats-for-dinner.py
import board, time, digitalio, pwmio, random
from adafruit_motor import servo
from adafruit_debouncer import Button

# create buttons
button_A_input = digitalio.DigitalInOut(board.GP6)
button_A_input.switch_to_input(digitalio.Pull.UP)  # Note: Pull.UP for external buttons
button_A = Button(button_A_input)

# Create & calibrate a servo
pwm = pwmio.PWMOut(board.GP13, frequency=50)  # My object / the servo / is on GP13
servo_1 = servo.Servo(pwm, min_pulse=750, max_pulse=2400)


current_angle = 0  # keep track of current angle to move left or right
servo_1.angle = current_angle

# Keep track of the last meal selection to avoid repeating
last_meal = -1  # Initialize to impossible value
NUM_OF_MEALS = 6
SEGMENT_SIZE = 180/NUM_OF_MEALS
ANGLE_OFFSET = SEGMENT_SIZE/2 # How much do I need to move to get to the "middle of the pie"?

def select_meal(current_angle):
    global last_meal
    random_meal = random.randint(0, NUM_OF_MEALS - 1)
    # Make sure we don't repeat the last selection
    while random_meal == last_meal:
        random_meal = random.randint(0, NUM_OF_MEALS - 1)
    last_meal = random_meal # remember this new meal as the last_meal
    # Each segment is 30°, but add 15° to get to the center
    target_angle = round( (random_meal * SEGMENT_SIZE) + ANGLE_OFFSET ) # 30° in our case + 15°
    print(f"Selected meal {random_meal}, moving to angle {target_angle}")
    # Move to the target angle
    if target_angle > current_angle:
        for i in range(current_angle, target_angle + 1):
            servo_1.angle = i
            print(f"angle: {i}")
            time.sleep(0.01)
    else:
        for i in range(current_angle, target_angle - 1, -1):
            servo_1.angle = i
            print(f"angle: {i}")
            time.sleep(0.01)
    return target_angle

print("What's for dinner running")
while True:
    button_A.update()
    if button_A.pressed:
        print("BUTTON PRESSED")
        current_angle = select_meal(current_angle)