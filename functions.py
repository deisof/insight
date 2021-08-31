import cv2


def generate_frames(camera, face_cascade):
    """Функция генерирует обработаные кадры с камеры"""

    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_rects = face_cascade.detectMultiScale(frame, 1.3, 5)

            print(f'Количество лиц: {len(face_rects)}')

            if len(face_rects) > 1:
                write_file('Больше одного человека за компьютером')
                print('Больше одного человека')
            elif len(face_rects) < 1:
                write_file('Нет на месте тестируемого')
                print('Вернитесь на место')

            for (x, y, w, h) in face_rects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def write_file(s):
    """Функция дополняет содержимое файла violations.txt, который содержит выявленные нарушения"""
    f_out = open('data_cam/violations.txt', 'a', encoding='utf8')
    f_out.write(s + '\n')
    f_out.close()
