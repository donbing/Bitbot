import RPi.GPIO as GPIO


class Buttons():

    def __init__(self, config):
        self.config = config
        # map button actions
        self.BUTTONS = {
            5: self.toggle_picure_frame_mode,
            6: self.refresh_display,
            16: self.toggle_volume,
            24: self.toggle_extended_view,
        }
        # Set up RPi.GPIO with the "BCM" numbering scheme
        GPIO.setmode(GPIO.BCM)
        # buttons connect ground, so we need pullup mode
        GPIO.setup(self.BUTTONS.keys(), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # register handler for each button, falling edge, 250ms debounce
        for pin in self.BUTTONS.keys():
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                self.BUTTONS[pin],
                bouncetime=250
            )

    def toggle_picure_frame_mode(self):
        newstate = 'false' if self.config.photo_mode_enabled() else 'true'
        self.config.toggle_photo_mode(newstate)
        self.config.save()

    def refresh_display(self):
        self.config.save()

    def toggle_volume(self):
        newstate = 'false' if self.config.show_volume() else 'true'
        self.config.toggle_volume(newstate)
        self.config.save()

    def toggle_extended_view(self):
        newstate = 'false' if self.config.expand_chart() else 'true'
        self.config.toggle_expanded_chart(newstate)
        self.config.save()
