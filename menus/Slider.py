import pygame
import pygame_gui


class Slider:
    def __init__(self, _screen, text, posx, posy, color, manager, start_value, range, _width=220, _height=30):
        slider_format = {"horizontal_slider":{"colours": {
                            "normal_bg": "#25292e",
                            "hovered_bg": "#35393e",
                            "disabled_bg": "#25292e",
                            "selected_bg": "#25292e",
                            "active_bg": "#193784",
                            "dark_bg": "#15191e,#202020,0",
                            "normal_text": "#c5cbd8",
                            "hovered_text": "#FFFFFF",
                            "selected_text": "#FFFFFF",
                            "disabled_text": "#6d736f"
                        },"misc":{
                            "shape": "rectangle",
                            "enable_arrow_buttons": "0",
                            "sliding_button_width": "15"
                        }
                },
            "horizontal_slider.button":
                {
                    "misc":
                        {
                            "border_width": "1"
                        }
                },
            "horizontal_slider.#sliding_button":
                {
                    "colours":
                        {
                            "normal_bg": "#FF0000"
                        }
                }
        }
        self.text = text
        self.posx = posx
        self.posy = posy
        self.was_pressed = False
        self.manager = manager
        self.color = color
        self.ref = pygame_gui.elements.ui_horizontal_slider
        self.slider = self.ref.UIHorizontalSlider(pygame.Rect(posx, posy+20, _width, _height), start_value, range, manager)
        self.value_font = pygame.font.SysFont("Calibri", 20, True, False)
        self.value_text = self.value_font.render(text + str(self.slider.get_current_value()), True, color)
        self.screen = _screen

    def update_text(self):
        self.value_text = self.value_font.render(self.text + str(self.slider.get_current_value().__round__()) + "%", True, self.color)

    def draw(self):
        self.update_text()
        self.screen.blit(self.value_text, (self.posx, self.posy))

    def get_current_value(self):
        return self.slider.get_current_value()

    def is_pressed(self):
        if self.slider.grabbed_slider and not self.was_pressed:
            self.was_pressed = True
            return True
        else:
            return False

    def is_released(self):
        if not self.slider.grabbed_slider and self.was_pressed:
            self.was_pressed = False
            return True
        else:
            return False