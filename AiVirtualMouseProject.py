from HandTrackingModule import handDetector
import cv2
import numpy as np
import time
import autopy
import pyautogui

# Initialisation
pTime = 0
width, height = 640, 480
frameR = 100
smoothening = 8
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
selecting = False
selection_start_pos = None

# Gestes
DOUBLE_CLICK_FINGERS = 2
COPY_FINGERS = 3
PASTE_FINGERS = 4
SELECT_TEXT_FINGERS = 5
FINGER_DISTANCE_THRESHOLD = 40

# Modes d'affichage
DISPLAY_MODES = {
    1: ("MODE SOURIS", (0, 255, 0)),
    2: ("MODE DOUBLE CLIC", (255, 255, 0)),
    3: ("MODE COPIER", (255, 0, 255)),
    4: ("MODE COLLER", (0, 255, 255)),
    5: ("MODE SELECTION", (255, 165, 0))
}

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Détecteur
detector = handDetector(maxHands=1)
screen_width, screen_height = autopy.screen.size()

# État
action_text = ""
action_time = 0
last_action_time = 0
action_delay = 0.5

while True:
    try:
        success, img = cap.read()
        if not success:
            print("Erreur webcam")
            continue
            
        img = detector.findHands(img)
        
        # Détection sécurisée de la main
        hand_data = detector.findPosition(img, draw=False)
        if hand_data is not None:
            lmlist, bbox = hand_data
        else:
            lmlist, bbox = [], []
            # Afficher un message quand aucune main n'est détectée
            cv2.putText(img, "Mettez votre main dans le cadre", (width//4, height//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        current_mode = 0  # Mode par défaut (inactif)

        if len(lmlist) != 0:
            fingers = detector.fingersUp()
            total_fingers = sum(fingers)
            current_mode = total_fingers

            # Debug: Afficher l'état des doigts
            finger_status = f"Pouce:{fingers[0]} Index:{fingers[1]} Majeur:{fingers[2]} Annulaire:{fingers[3]} Auriculaire:{fingers[4]}"
            cv2.putText(img, finger_status, (10, height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

            # 1 doigt: Mouvement
            if total_fingers == 1 and fingers[1] == 1:
                if selecting:
                    pyautogui.mouseUp()
                    selecting = False
                    selection_start_pos = None
                
                x1, y1 = lmlist[8][1], lmlist[8][2]
                x3 = np.interp(x1, (frameR, width-frameR), (0, screen_width))
                y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

                curr_x = prev_x + (x3 - prev_x)/smoothening
                curr_y = prev_y + (y3 - prev_y)/smoothening

                autopy.mouse.move(screen_width - curr_x, curr_y)
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                prev_x, prev_y = curr_x, curr_y

            # 2 doigts: Double-clic
            # 2 doigts: Double-clic
            elif total_fingers == DOUBLE_CLICK_FINGERS and time.time() - last_action_time > action_delay:
                    result = detector.findDistance(8, 12, img)
                    if result:  # Vérifie que result n'est pas None
                        length, img, _ = result
                        if length < FINGER_DISTANCE_THRESHOLD:
                            autopy.mouse.click(autopy.mouse.Button.LEFT, 2)
                            action_text = "Double Click"
                            action_time = time.time()
                            last_action_time = time.time()



            # 3 doigts: Copier
            elif total_fingers == COPY_FINGERS and time.time() - last_action_time > action_delay:
                pyautogui.hotkey('ctrl', 'c')
                action_text = "Copied!"
                action_time = time.time()
                last_action_time = time.time()

            # 4 doigts: Coller
            elif total_fingers == PASTE_FINGERS and time.time() - last_action_time > action_delay:
                pyautogui.hotkey('ctrl', 'v')
                action_text = "Pasted!"
                action_time = time.time()
                last_action_time = time.time()

            # 5 doigts: Sélection
            elif total_fingers >= 5 or (all(fingers[1:]) and fingers[0] == 1):
                if not selecting:
                    pyautogui.mouseDown()
                    selecting = True
                    action_text = "Selection Texte"
                    action_time = time.time()
                    selection_start_pos = (prev_x, prev_y)
                
                x1, y1 = lmlist[8][1], lmlist[8][2]
                x3 = np.interp(x1, (frameR, width-frameR), (0, screen_width))
                y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

                curr_x = prev_x + (x3 - prev_x)/smoothening
                curr_y = prev_y + (y3 - prev_y)/smoothening

                autopy.mouse.move(screen_width - curr_x, curr_y)
                
                if selection_start_pos:
                    start_x, start_y = selection_start_pos
                    cv2.rectangle(img, 
                                (int(start_x * width/screen_width), int(start_y * height/screen_height)),
                                (x1, y1), (0, 255, 0), 2)
                
                prev_x, prev_y = curr_x, curr_y
            else:
                if selecting:
                    pyautogui.mouseUp()
                    selecting = False
                    selection_start_pos = None
                    last_action_time = time.time()

        # Affichage du mode actuel
        if current_mode in DISPLAY_MODES:
            mode_text, color = DISPLAY_MODES[current_mode]
            overlay = img.copy()
            cv2.rectangle(overlay, (5, 5), (250, 40), (50, 50, 50), -1)
            cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
            cv2.putText(img, mode_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        else:
            overlay = img.copy()
            cv2.rectangle(overlay, (5, 5), (200, 40), (50, 50, 50), -1)
            cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
            cv2.putText(img, "MODE: INACTIF", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Affichage des actions
        if time.time() - action_time < 1:
            cv2.putText(img, action_text, (width//2-100, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Instructions
        instructions = [
            "1 doigt: Deplacer souris",
            "2 doigts: Double-clic",
            "3 doigts: Copier (Ctrl+C)",
            "4 doigts: Coller (Ctrl+V)",
            "5 doigts: Selection texte"
        ]
        
        for i, text in enumerate(instructions):
            cv2.putText(img, text, (10, 100 + i*30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        # FPS
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (20, 50), 
                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow("Controle Gestuel", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Erreur mineure: {e}")
        continue

if selecting:
    pyautogui.mouseUp()
cap.release()
cv2.destroyAllWindows()
