from pynput import keyboard
import pyautogui
import random
from time import sleep

def _click(min_x, max_x, min_y, max_y, left=True):
    position = pyautogui.position()
    target = (
        random.randint(min_x, max_x),
        random.randint(min_y, max_y)
        )
    halved_distance = ((target[0] - position[0]) // 3, (target[1] - position[1]) // 3)
    if halved_distance[0] > 1:
        ax, bx = 0, halved_distance[0]
    elif halved_distance[0] < -1:
        ax, bx = halved_distance[0], 0
    else:
        ax, bx = -20, 20
    if halved_distance[1] > 1:
        ay, by = 0, halved_distance[1]
    elif halved_distance[1] < -1:
        ay, by = halved_distance[1], 0
    else:
        ay, by = -5, 5
    pyautogui.move(random.randint(ax, bx), random.randint(ay, by), 0.1)
    pyautogui.move(random.randint(ax, bx), random.randint(ay, by), 0.1)
    pyautogui.move(random.randint(ax, bx), random.randint(ay, by), 0.1)
    pyautogui.moveTo(*target, 0.1)
    if left == True:
        pyautogui.click()
    else:
        pyautogui.click(button='right')

class Slot:
    count = 0
    total_x, total_y = pyautogui.size()
    max_x = total_x - 350
    min_x = total_x - 385
    max_y = 220
    min_y = 200
    interval_y = 59
    def __init__(self, max_x, min_x, max_y, min_y):
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        Slot.count += 1

    def __str__(self):
        return "Slot({}, {}, {}, {})".format(self.max_x, self.min_x, self.max_y, self.min_y)
    
    @classmethod
    def another(cls):
        max_y = cls.max_y + (cls.count * cls.interval_y)
        min_y = cls.min_y + (cls.count * cls.interval_y)
        return cls(cls.max_x, cls.min_x, max_y, min_y)
    
    @classmethod
    def factory(cls, quantity):
        slots = []
        for n in range(quantity):
            slots.append(cls.another())
        return slots

    def click(self, left=True):
        _click(self.min_x, self.max_x,self.min_y, self.max_y, left=False)

class Target:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y

    def click(self):
        _click(self.min_x, self.max_x, self.min_y, self.max_y, left=True)


def on_press(key):
    """ try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key)) """
    if isinstance(key, keyboard._win32.KeyCode):
        if hotkey.suspended == False:
            if key.char in '1234':
                hotkey.change_target(key.char)
                #slot_list[int(key.char)].click(left=False)
            elif key.char in 'xfgvbnm':
                hotkey.action(key.char)
            else:
                pass
        else:
            print('Hotkeys are suspended. Press F1 to resume.')
    else: ## key is special
        if key == keyboard.Key.f2:
            print(pyautogui.position())
        elif key == keyboard.Key.f1:
            hotkey.suspention()
            print('Suspention')
        else:
            pass


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


class Hotkey:
    def __init__(self):
        self.slots = Slot.factory(7)
        self.targets = {
            '2': Target(2369, 2530, 427, 440), #'battle_1'
            '3': Target(2368, 2532, 454, 472), #'battle_2'
            '1': Target(1708, 1759, 491, 539), #'player'
            '4': Target(1538, 1941, 336, 656) #'around'
            }
        self.target = '1'
        self.suspended = False
        
    def change_target(self, target_key):
        self.target = target_key
        print('Target changed to {}.'.format(target_key))
    
    def action(self, slot_key):
        self.slots['xfgvbnm'.index(slot_key)].click()
        sleep(0.1)
        self.targets[self.target].click()
    
    def suspention(self):
        self.suspended = not self.suspended







if __name__ == "__main__":

    hotkey = Hotkey()

    print('testing')
    for slot in hotkey.slots:
        print(slot)

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    print('Listener is done.')