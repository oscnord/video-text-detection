from cv2 import cv2
import pytesseract


print('OpenCV version: ' + cv2.__version__)
# hardcoded list with keywords for now
DICT = ['director', 'directed', 'written', 'writer',
        'producer', 'produced', 'production', 'lead']

path = input('Enter path to file or hls manifest: ')

vidcap = cv2.VideoCapture(path)
success,frame = vidcap.read()
framenbr = 0

print('Working...')
while success:
    success,frame = vidcap.read()
    if not success:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    data = pytesseract.image_to_string(gray, lang='eng', config='--psm 6').lower()
    if any(word in data for word in DICT):
        print(data + '\nFrame number: ' + str(framenbr))
    framenbr += 1
