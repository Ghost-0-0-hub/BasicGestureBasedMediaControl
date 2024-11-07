import cv2
import mediapipe as mp
import time
import pyautogui

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()

is_playing = False

def pause_gesture(hand_landmarks):

    index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
    index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

    thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
    
    middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
    middle_dip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_DIP]
    
    ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
    ring_dip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_DIP]
    
    pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
    pinky_dip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_DIP]
    
    index_down = index_dip.y < index_tip.y
    thumb_down = thumb_tip.y < index_tip.y
    middle_down = middle_dip.y < middle_tip.y
    ring_down = ring_dip.y < ring_tip.y
    pinky_down = pinky_dip.y < pinky_tip.y

    return index_down and thumb_down and middle_down and ring_down and pinky_down
    
def vol_down(hand_landmarks):

    index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
    index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

    thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
    
    middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
    
    ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
    
    pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]


    index_extend = index_tip.y < index_dip.y
    thumb_extend = thumb_tip.y < index_dip.y
    ring_down =  ring_tip.y > index_dip.y
    middle_down = middle_tip.y > index_dip.y
    pinky_down = pinky_tip.y > index_dip.y

    return index_extend and thumb_extend and ring_down and middle_down and pinky_down

def vol_up(hand_landmarks):
    
    index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
    index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

    thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
    
    middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
    
    ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
    
    pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]

    index_extend = index_tip.y < index_dip.y
    middle_extend = middle_tip.y < index_dip.y
    ring_down = ring_tip.y > index_dip.y
    pinky_down = pinky_tip.y > index_dip.y

    return index_extend and middle_extend and ring_down and pinky_down


mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
prev_y = None
swipe_direction = None

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            if pause_gesture(hand_landmarks):
                pyautogui.press('space')
                time.sleep(1)
            elif vol_down(hand_landmarks):
                pyautogui.press('down')
                time.sleep(0.2)
            elif vol_up(hand_landmarks):
                pyautogui.press('up')
                time.sleep(0.2)
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hand.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracker', img)
    if cv2.waitKey(5) & 0XFF == 27:
        break

cap.release()
cv2.destroyAllWindows()