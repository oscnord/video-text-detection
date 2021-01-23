from cv2 import cv2
import pytesseract


print('OpenCV version: ' + cv2.__version__)
# list with keywords
DICT = ['director', 'directed', 'written', 'writer',
        'producer', 'produced', 'production', 'lead']
# Get path to file
path = input('Enter path to video file: ')
# Get frame step
step = int(input('frame step: '))
if step <= 0:
    step = 1
print(step)

success = True
frameStep = 0
counter = 0

vidcap = cv2.VideoCapture(path)
frame = vidcap.read()

print('Working...')
while success:
    if frameStep == step and frame is not None:
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.resize(gray_image, None, fx=2,
                                fy=2, interpolation=cv2.INTER_LINEAR)
        blur_image = cv2.GaussianBlur(gray_image, (11, 11), 0)
        thresh = cv2.threshold(
            blur_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        opening = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        data = pytesseract.image_to_string(
            invert, lang='eng', config='--psm 6').lower()

        if any(word in data for word in DICT):
            print(data + '\nFrame number: ' + str(counter))

        frameStep = 0
    success, frame = vidcap.read()
    frameStep += 1
    counter += 1

print('Number of frames: ' + str(counter))
