import keyboard
import mouse
from char.i_char import IChar
from template_finder import TemplateFinder
from ui_manager import UiManager
from pather import Pather
from logger import Logger
from screen import Screen
from utils.misc import wait
import time
from pather import Pather, Location


class Hammerdin(IChar):
    def __init__(self, skill_hotkeys, char_config, screen: Screen, template_finder: TemplateFinder, ui_manager: UiManager, pather: Pather):
        Logger.info("Setting up Hammerdin")
        super().__init__(skill_hotkeys, char_config, screen, template_finder, ui_manager)
        self._pather = pather

    def pre_buff(self):
        keyboard.send(self._skill_hotkeys["holy_shield"])
        wait(0.1, 0.12)
        mouse.click(button="right")
        wait(self._cast_duration)
        if self._char_config["cta_available"]:
            self._pre_buff_cta()

    def _cast_hammers(self, time_in_s: float):
        keyboard.send(self._char_config["stand_still"], do_release=False)
        wait(0.05)
        keyboard.send(self._skill_hotkeys["blessed_hammer"])
        wait(0.05)
        keyboard.send(self._skill_hotkeys["concentration"])
        wait(0.05, 0.1)
        mouse.press(button="left")
        start = time.time()
        i = 0
        while (time.time() - start) < time_in_s:
            wait(0.04, 0.06)
            i += 1
            if i % 20 == 0:
                mouse.release(button="left")
                time.sleep(0.01)
                mouse.press(button="left")
        mouse.release(button="left")
        keyboard.send(self._char_config["stand_still"], do_press=False)

    def _do_redemption(self):
        keyboard.send(self._skill_hotkeys["redemption"])
        wait(1.5, 2.0)

    def kill_pindle(self) -> bool:
        wait(0.1, 0.15)
        self._pather.traverse_nodes(Location.PINDLE_SAVE_DIST, Location.PINDLE_END, self, time_out=2.0)
        self._cast_hammers(1)
        # pindle sometimes knocks back, get back in
        self._pather.traverse_nodes(Location.PINDLE_SAVE_DIST, Location.PINDLE_END, self, time_out=0.2)
        self._cast_hammers(max(1, self._char_config["atk_len_pindle"] - 1))
        wait(0.1, 0.15)
        self._do_redemption()
        return True

    def kill_eldritch(self) -> bool:
        self._pather.traverse_nodes(Location.ELDRITCH_SAVE_DIST, Location.ELDRITCH_END, self, time_out=0.2)
        wait(0.1, 0.15)
        self._cast_hammers(self._char_config["atk_len_eldritch"])
        wait(0.1, 0.15)
        self._do_redemption()
        return True

    def kill_shenk(self):
        self._pather.traverse_nodes(Location.SHENK_SAVE_DIST, Location.SHENK_END, self, time_out=0.2)
        wait(0.1, 0.15)
        self._cast_hammers(self._char_config["atk_len_shenk"])
        wait(0.1, 0.15)
        self._do_redemption()
        return True


if __name__ == "__main__":
    import os
    import keyboard
    keyboard.add_hotkey('f12', lambda: Logger.info('Force Exit (f12)') or os._exit(1))
    keyboard.wait("f11")
    from config import Config
    from ui_manager import UiManager
    config = Config()
    screen = Screen(config.general["monitor"])
    t_finder = TemplateFinder(screen)
    pather = Pather(screen, t_finder)
    ui_manager = UiManager(screen, t_finder)
    char = Hammerdin(config.hammerdin, config.char, screen, t_finder, ui_manager, pather)
    for i in range(20):
        char.pre_buff()
        time.sleep(1.5)
    # char.tp_town()
