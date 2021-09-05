import cv2
import keyboard
import numpy as np
import pyautogui

s = []


def generate_frames(camera, face_cascade):
    """Функция генерирует обработаные кадры с камеры"""
    keyboard.add_hotkey('ctrl + c', lambda: s.append('Произошло копирование' + '\n'))
    keyboard.add_hotkey('ctrl + v', lambda: s.append('Произошло копирование' + '\n'))
    while True:
        global s
        success, frame = camera.read()
        out = cv2.VideoWriter("data_cam/output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20.0, (1920, 1080))

        if not success:
            break
        else:
            face_rects = face_cascade.detectMultiScale(frame, 1.3, 5)
            s.append(f'Количество лиц: {len(face_rects)}' + '\n')

            if len(face_rects) > 1:
                s.append('Больше одного человека за компьютером' + '\n')
            elif len(face_rects) < 1:
                s.append('Нет на месте тестируемого' + '\n')

            for (x, y, w, h) in face_rects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)

            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def write_file(s, password):
    temp = []
    """Функция дополняет содержимое файла violations.txt, который содержит выявленные нарушения"""
    f_out = open(f'data_cam/{password}.txt', 'w', encoding='utf8')
    temp.append(s[0])
    for i in range(1, len(s) - 1):
        if s[i] != s[i - 1]:
            temp.append(s[i])
    f_out.writelines(temp)
    f_out.close()
