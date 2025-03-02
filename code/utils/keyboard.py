from kivy.core.window import Window

class KeyboardManager:
    def __init__(self, widget):
        self.pressed_keys = set()
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, widget)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1] if keycode[1] else text
        self.pressed_keys.add(key)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        key = keycode[1] if keycode[1] else ""
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        return True