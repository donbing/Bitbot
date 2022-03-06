from src.configuration.log_decorator import info_log


class Buttons():
    def __init__(self, config):
        self.config = config
        # 👆 map button actions
        self.BUTTONS = {
            5: self.toggle_picure_frame_mode,
            6: self.refresh_display,
            16: self.toggle_volume,
            24: self.toggle_extended_view,
        }
        try:
            import RPi.GPIO as GPIO
            # 🎰 set up RPi.GPIO with the "BCM" numbering scheme
            GPIO.setmode(GPIO.BCM)
            # 🌍 buttons connect ground, so we need pullup mode
            button_keys = self.BUTTONS.keys()
            GPIO.setup(list(button_keys), GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # ⛏️ register handler for each button, falling edge, 250ms debounce
            for pin in self.BUTTONS.keys():
                GPIO.add_event_detect(
                    pin,
                    GPIO.FALLING,
                    lambda pin: self.BUTTONS[pin](),
                    bouncetime=250
                )
        except RuntimeError:
            pass

    @info_log
    def toggle_picure_frame_mode(self):
        newstate = str(not self.config.photo_mode_enabled()).lower()
        self.config.toggle_photo_mode(newstate, False)
        self.config.save()

    @info_log
    def refresh_display(self):
        self.config.save()

    @info_log
    def toggle_volume(self):
        newstate = str(not self.config.show_volume()).lower()
        self.config.toggle_volume(newstate)
        self.config.save()

    @info_log
    def toggle_extended_view(self):
        newstate = str(not self.config.expand_chart()).lower()
        self.config.toggle_expanded_chart(newstate)
        self.config.save()