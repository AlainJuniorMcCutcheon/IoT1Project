from gpiozero import Button, Buzzer, MotionSensor, LED
from time import sleep

# Define the GPIO pins
pir = MotionSensor(6)     # PIR sensor pin
button = Button(17)       # Button pin
buzzer = Buzzer(25)       # Buzzer pin
led = LED(23)             # LED pin (GPIO 22)

def test_pir():
    print("Testing PIR Motion Sensor...")
    print("Waiting for motion...")
    while True:
        pir.wait_for_motion()
        print("Motion detected!")
        buzzer.on()
        led.on()  # Turn on LED when motion is detected
        sleep(0.5)
        buzzer.off()
        led.off()  # Turn off LED after delay
        pir.wait_for_no_motion()
        print("No motion.")
        sleep(1)

def test_button():
    print("Testing Button...")
    print("Waiting for button press...")
    while True:
        button.wait_for_press()
        print("Button pressed!")
        buzzer.on()
        led.on()  # Turn on LED when button is pressed
        sleep(0.5)
        buzzer.off()
        led.off()  # Turn off LED after delay
        button.wait_for_release()
        print("Button released")
        sleep(1)

def test_buzzer():
    print("Testing Buzzer...")
    print("Buzzer on for 1 second...")
    buzzer.on()
    led.on()  # Turn on LED when buzzer is active
    sleep(1)
    buzzer.off()
    led.off()  # Turn off LED after buzzer is off
    print("Test complete.")

def test_all_components():
    print("Testing All Components (PIR, Button, Buzzer, LED)...")
    print("Press Ctrl+C to stop.")
    while True:
        if pir.motion_detected:
            print("Motion detected!")
            buzzer.on()
            led.on()  # Turn on LED when motion is detected
            sleep(0.5)
            buzzer.off()
            led.off()  # Turn off LED after delay
        
        if button.is_pressed:
            print("Button pressed!")
            buzzer.on()
            led.on()  # Turn on LED when button is pressed
            sleep(0.5)
            buzzer.off()
            led.off()  # Turn off LED after delay
        
        sleep(1)

def main():
    print("Starting tests...\n")
    while True:
        print("\nChoose test to run:")
        print("1: PIR Sensor Test")
        print("2: Button Test")
        print("3: Buzzer Test")
        print("4: Test All Components")
        print("5: Exit")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            test_pir()
        elif choice == '2':
            test_button()
        elif choice == '3':
            test_buzzer()
        elif choice == '4':
            test_all_components()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please choose between 1 and 5.")

if __name__ == "__main__":
    main()
