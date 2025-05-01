from kivy.app import App
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime
import time
import json
import uuid

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config

Builder.load_file('alarm_gui.kv')

translations = {
    'en': {
        'title': "Smart Home Alarm System",
        'armed': "System Armed",
        'disarmed': "System Disarmed",
        'triggered': "TRIGGERED",
        'buzzer': "Buzzer:",
        'motion': "Motion:",
        'hold_to_disable': "Hold to Disable",
        'alarm_log': "Alarm Log",
        'alarm_triggered': "Alarm triggered at",
        'alarm_deactivated': "Alarm deactivated at",
        'Yes': "Yes",
        'No': "No"
    },
    'fr': {
        'title': "Système d'alarme domotique",
        'armed': "Système Armé",
        'disarmed': "Système Désarmé",
        'triggered': "DÉCLENCHÉ",
        'buzzer': "Buzzer :",
        'motion': "Mouvement :",
        'hold_to_disable': "Maintenir pour désactiver",
        'alarm_log': "Journal d'alarme",
        'alarm_triggered': "Alarme déclenchée à",
        'alarm_deactivated': "Alarme désactivée à",
        'Yes': "Oui",
        'No': "Non"
    }
}

class AlarmSystem(BoxLayout):
    system_status = 'DISARMED'
    buzzer_status = 'OFF'
    motion_status = 'No'
    led_color = ListProperty([0.5, 0.5, 0.5, 1])
    led_blinking = False
    arm_button_held = False
    armed_time = None
    held_time = 0
    led_flash_event = None
    log_text = StringProperty("")
    language = StringProperty('en')
    mqtt_client = None
    is_connected = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Auto-arm countdown
        self.auto_arm_event = Clock.schedule_interval(self.auto_arm_countdown, 1)

        # MQTT Client Setup
        self.setup_mqtt()

        # Schedule telemetry every 5 seconds
        Clock.schedule_interval(self.send_sample_telemetry, 5)

    def setup_mqtt(self):
        try:
            client_id = str(uuid.uuid4())
            self.mqtt_client = AWSIoTMQTTClient(client_id)
            self.mqtt_client.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
            self.mqtt_client.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
            self.mqtt_client.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
            self.mqtt_client.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

            if self.mqtt_client.connect():
                self.is_connected = True
                print("MQTT Connected ✅")
        except Exception as e:
            print("MQTT connection failed ❌:", e)

    def send_sample_telemetry(self, dt):
        if not self.is_connected:
            print("MQTT not connected, skipping telemetry")
            return

        telemetry = {
            'sample_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'device_id': config.CLIENT_ID,
            'system_status': self.system_status,
            'buzzer_status': self.buzzer_status,
            'motion_status': self.motion_status
        }

        try:
            self.mqtt_client.publish(config.TOPIC, json.dumps(telemetry), 1)
            print("📡 Published:", telemetry)
        except Exception as e:
            print("Failed to publish telemetry:", e)

    def get_translation(self, key):
        return translations[self.language].get(key, key)

    def update_language(self, *args):
        t = translations[self.language]
        self.ids.title_label.text = t['title']
        self.ids.status_label.text = t[self.system_status.lower()]
        self.ids.alarm_button.text = t['hold_to_disable']
        self.ids.buzzer_label_title.text = t['buzzer']
        self.ids.motion_label_title.text = t['motion']
        self.ids.log_title.text = t['alarm_log']
        self.ids.buzzer_label.text = t['Yes'] if self.buzzer_status == 'ON' else t['No']
        self.ids.motion_label.text = t['Yes'] if self.motion_status == 'Yes' else t['No']

    def auto_arm_countdown(self, dt):
        if self.system_status == 'DISARMED' and self.armed_time is None:
            self.armed_time = time.time()
        if self.armed_time and time.time() - self.armed_time >= 5:
            self.system_status = 'ARMED'
            self.ids.status_label.text = self.get_translation('armed')
            self.armed_time = None

    def on_alarm_button_down(self):
        self.arm_button_held = True
        self.held_time = time.time()

    def on_alarm_button_up(self):
        if self.arm_button_held and time.time() - self.held_time >= 3:
            self.deactivate_alarm()
        else:
            self.trigger_alarm()
        self.arm_button_held = False

    def trigger_alarm(self):
        self.system_status = 'TRIGGERED'
        self.ids.status_label.text = self.get_translation('triggered')
        self.buzzer_status = 'ON'
        self.motion_status = 'Yes'
        self.led_blinking = True
        self.update_log()

        if self.led_flash_event is None:
            self.led_flash_event = Clock.schedule_interval(self.blink_led, 0.5)

        if self.auto_arm_event:
            Clock.unschedule(self.auto_arm_event)

        self.update_gui()

    def deactivate_alarm(self):
        self.system_status = 'DISARMED'
        self.ids.status_label.text = self.get_translation('disarmed')
        self.led_blinking = False
        self.led_color = (0.5, 0.5, 0.5, 1)
        self.buzzer_status = 'OFF'
        self.motion_status = 'No'
        self.update_log()

        if self.led_flash_event:
            Clock.unschedule(self.led_flash_event)
            self.led_flash_event = None

        self.auto_arm_event = Clock.schedule_interval(self.auto_arm_countdown, 1)

        self.update_gui()

    def update_log(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t = translations[self.language]
        if self.system_status == 'TRIGGERED':
            self.log_text += f"{t['alarm_triggered']} {current_time}\n"
        else:
            self.log_text += f"{t['alarm_deactivated']} {current_time}\n"
        self.ids.log_label.text = self.log_text

    def blink_led(self, dt):
        if self.led_blinking:
            self.led_color = [1, 0, 0, 1] if self.led_color == [1, 1, 1, 1] else [1, 1, 1, 1]
        else:
            self.led_color = [0.5, 0.5, 0.5, 1]

    def update_gui(self):
        self.ids.buzzer_label.text = self.buzzer_status
        self.ids.motion_label.text = self.motion_status


class AlarmApp(App):
    def build(self):
        return AlarmSystem()


if __name__ == "__main__":
    AlarmApp().run()
