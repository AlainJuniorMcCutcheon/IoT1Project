# IoT1Project

# Description
The Burglary Alarm System is a simple yet effective security solution built with a Raspberry Pi to help protect homes or small businesses. Using a PIR motion sensor, button module, LED module, and an active buzzer, the system detects movement and alerts the user when there’s a potential intrusion.

Real-World Use Case
In today’s world, keeping our homes safe is more important than ever. Many homes get broken into by intruders every day, and homeowners are often oblivious to what's going on in their house while they’re away because they have poor security. This system is designed to act as an affordable and customizable alarm for anyone looking to secure their space. The PIR motion sensor detects movement and triggers the alarm when someone enters the area. This can be especially useful for people who want a quick way to secure rooms, entrances, or even their entire home.

The button module allows users to easily arm or disarm the system with a simple press. When armed, the system actively monitors for movement, and any detected motion immediately sets off the LED to blink rapidly and the buzzer to sound an alarm. This makes it easy to know when something is wrong, even from a distance.

In addition to its primary purpose of enhancing home security, this system provides an opportunity to explore basic sensor integration and automation. It is an ideal project for individuals looking to learn about IoT, sensor-based systems, and Raspberry Pi programming while creating something practical and useful for everyday life.

# How To Use
Using the alarm system is straightforward. Simply launch the application, and the system will automatically arm itself after a 5-second countdown. Once armed, the GUI will clearly display “ARMED” to indicate its status.

If the PIR motion sensor detects any movement, the system will immediately activate the alarm: the LED will begin flashing rapidly, the buzzer will emit a loud sound, and the display will update to “TRIGGERED.”

To deactivate the alarm, press and hold the physical button or the on-screen button for three seconds. This deliberate press duration acts as a basic security feature, ensuring the system isn’t accidentally disarmed. If the button is not held for the full three seconds, the alarm will remain active.

Once disarmed, the screen will show “System Disarmed” and, after a short 5-second delay, the system will automatically re-arm. During each activation and deactivation event, a timestamp is logged and displayed in the scrollable event log at the bottom of the GUI.

For ease of use, the interface is fully translated in both English and French, making it accessible to a wider range of users.

If available, you may also use a touch screen device to operate the application.

# List

| Name            | Picture                                                                                               | Wiring                                                                 |
|-----------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| PIR Sensor Module | ![image](https://github.com/user-attachments/assets/695fae26-0fac-402d-9f3b-8966f2cb2cb9) | VCC → 3.3V<br>GND → GND<br>OUT → GPIO6                                  |
| Button Module     | ![image](https://github.com/user-attachments/assets/9d1e5dfd-78dc-4904-9307-bc4751ba5fbb) | VCC → 3.3V <br>GND → GND<br>OUT → GPIO17                          |
| LED Module        | ![image](https://github.com/user-attachments/assets/3746c211-2c57-430b-b2c1-a0977adb7f35) | <br>GND → GND<br>Signal → GPIO23                       |
| Passive Buzzer    | ![image](https://github.com/user-attachments/assets/5d8dd3fa-708a-4c24-80f5-501c47bfd825) | VCC → 3.3V <br>GND → GND<br>Signal → GPIO25                      |

# GPIO Wiring
![image](https://github.com/user-attachments/assets/963cb4b9-d79b-4993-9c85-9dd6813f2666)
