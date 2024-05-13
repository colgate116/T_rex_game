import mss
import cv2
import numpy as np
import pyautogui

'''
https://chromedino.com/
код для игры в динозаврика                        
'''

'''
Инструкция и аннотация:
1.Открыть сайт https://chromedino.com
2.Запустить программу
3.Нажать пробел на сайте, чтобы динозаврик побежал
4. Когда игра закончится, запустить программу заново (так как переменная counter не обнуляется)


Средний результат: 700-900
Лучший результат: 3578 (доказательство на изображения, игрок N I это я)
Почему средний результат сильно хуже лучшего?
Потому что необходимо правильно рассчитать коэффициент ускорения
'''


def grab_screen(region):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        if region:
            monitor["top"] = region["top"]
            monitor["left"] = region["left"]
            monitor["width"] = region["width"]
            monitor["height"] = region["height"]
        img = np.array(sct.grab(monitor))
        return img[:, :, :3]


def detect_obstacles(image):
    # Преобразование в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray, 500, 500)
    # Порог для выделения объектов
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # Нахождение контуров

    # kernel = np.ones((20, 20), np.uint8)
    # gray = cv2.dilate(gray, kernel, iterations=1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x_list = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 1 and h > 1:
            x_list.append(x+w)
            #gray = cv2.rectangle(gray, (x, y), (x + w, y + h), 100, 2)

    #cv2.imshow('Image with Rectangle', gray)
    #cv2.waitKey(1000)
    return x_list


def jump():
    pyautogui.press('space')

def main():
    region = {"top": 355, "left": 680, "width": 250, "height": 48}
    count=0
    while True:
        screen = grab_screen(region)
        obstacle = detect_obstacles(screen)
        if obstacle:
            if max(obstacle) < int(168+1.013 **(count//8  )):
                jump()
                count+=1
        print(count)

if __name__ == '__main__':
    main()
