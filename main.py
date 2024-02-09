import pyautogui as pyautogui
import numpy as np
import time
from random import randint, choice
from math import ceil
import sys
import threading
# import keyboard
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

on = True

def execute():
    on = False # The function you want to execute to stop the loop

# keyboard.add_hotkey("shift+a", execute)  # add the hotkey

def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    return result

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n - 1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                list(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def mouse_bez(init_pos, fin_pos, deviation, speed):
    '''
    GENERATE BEZIER CURVE POINTS
    Takes init_pos and fin_pos as a 2-tuple representing xy coordinates
        variation is a 2-tuple representing the
        max distance from fin_pos of control point for x and y respectively
        speed is an int multiplier for speed. The lower, the faster. 1 is fastest.

    '''

    # time parameter
    ts = [t / (speed * 100.0) for t in range(speed * 101)]

    # bezier centre control points between (deviation / 2) and (deviaion) of travel distance, plus or minus at random
    control_1 = (
    init_pos[0] + choice((-1, 1)) * abs(ceil(fin_pos[0]) - ceil(init_pos[0])) * 0.01 * randint(deviation / 2,
                                                                                               deviation),
    init_pos[1] + choice((-1, 1)) * abs(ceil(fin_pos[1]) - ceil(init_pos[1])) * 0.01 * randint(deviation / 2, deviation)
    )
    control_2 = (
    init_pos[0] + choice((-1, 1)) * abs(ceil(fin_pos[0]) - ceil(init_pos[0])) * 0.01 * randint(deviation / 2,
                                                                                               deviation),
    init_pos[1] + choice((-1, 1)) * abs(ceil(fin_pos[1]) - ceil(init_pos[1])) * 0.01 * randint(deviation / 2, deviation)
    )

    xys = [init_pos, control_1, control_2, fin_pos]
    bezier = make_bezier(xys)
    points = bezier(ts)

    return points

def random_mouse_move(field_width=200, field_height=200, hours=8):
    '''
    :param field_width: your screen width
    :param field_height: your screen height
    :param hours: How many hours will the mouse move
    '''
    global on_break
    # Define center of screen and field size
    center_x, center_y = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2  # Detect screen center

    old_point = [center_x, center_y]  # Previous point, the first value is the center of the field
    interval = 0  # Interval when fast move apply

    # Generate random points and move mouse cursor to them
    # num_steps = 10
    # for i in range(num_steps):
    t_end = time.time() + 60 * 60 * hours
    while time.time() < t_end:
        # Определение времени работы и перерыва
        work_time = randint(10, 40) * 60  # Случайное время работы от 10 до 40 минут
        break_time = randint(8, 14) * 60  # Случайный перерыв от 8 до 14 минут (свыше 15 минут может заблокироваться сеанс RDP)

        # Для тестирования
        # work_time = randint(60, 120) # Случайное время работы от 1 до 2 минут
        # break_time = randint(30, 60)  # Случайный перерыв от 30 до 60 секунд
        
        # Работа в течение определенного времени
        t_work_end = time.time() + work_time
        while time.time() < t_work_end and time.time() < t_end:
            interval += 1
            # Generate random point
            point = np.random.rand(2) * [field_width, field_height] + [center_x - field_width // 2, center_y - field_height // 2]

            point1 = [round(old_point[0]), round(old_point[1])]
            point2 = [round(point[0]), round(point[1])]

            points = mouse_bez(point1, point2, 2, 1)  # Get an array of points of the Bezier curve

            if interval < 3:
                for x in points:
                    pyautogui.moveTo(x[0], x[1])
            else:
                pyautogui.moveTo(point[0], point[1], duration=0.5)  # Move mouse cursor to point quickly
                interval = 0

            old_point = point  # Remember previous point

            pyautogui.press('ctrl')
            time.sleep(0.5)  # задержка в полсекунды
            pyautogui.press('alt')
            time.sleep(0.5)  # задержка в полсекунды
            pyautogui.click()  # click the mouse
            pyautogui.scroll(randint(1, 10))  # scroll up 10 "clicks"
            pyautogui.scroll(-randint(1, 4))  # scroll down 10 "clicks"
            # pyautogui.click(button='right')  # right-click the mouse

            # Pause briefly to simulate human behavior
            time.sleep(np.random.normal(0.5, 0.1))
        on_break = True
        print(f"\nTaking a break for {break_time/60} minutes.")
        time.sleep(break_time)
        on_break = False

start_time = time.time()  # Запоминаем время начала работы скрипта
work_time_accumulated = 0  # Накопленное время работы без учета перерывов
on_break = False  # Флаг для отслеживания перерыва

def track_time():
    global on_break, work_time_accumulated
    last_time_checked = start_time

    while not done:
        current_time = time.time()
        if not on_break:
            work_time_accumulated += current_time - last_time_checked
            elapsed_hours = int(work_time_accumulated // 3600)
            elapsed_minutes = int((work_time_accumulated % 3600) // 60)
            elapsed_seconds = int(work_time_accumulated % 60)

            # Очищаем строку перед выводом
            sys.stdout.write('\r' + ' ' * 50)  # Очищаем строку
            sys.stdout.flush()

            # Выводим обновленное время
            sys.stdout.write(f'\rProcessing... Time elapsed: {elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s')
            sys.stdout.flush()
        last_time_checked = current_time
        time.sleep(1)

done = False

def main():
    clear_terminal()
    global done
    spinner = threading.Thread(target=track_time)
    spinner.start()

    try:
        random_mouse_move(200, 200, 8)
    finally:
        done = True
        spinner.join()

if __name__ == '__main__':
    main()