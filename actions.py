import pyautogui





def perform_action(gesture, fingers, is_pinching, smooth_x, smooth_y):
    global ga, rga, minga, nav, ent
    # Move mouse if only index finger is up
    if fingers[1]==1 and sum(fingers)==1:
        pyautogui.moveTo(smooth_x, smooth_y, duration=0.025)

    # Only trigger click on transition from not pinching to pinching
    # For left click
    if fingers[1]==1 and is_pinching:
        if not ga:
            pyautogui.click()
            ga = True
    else:
        ga = False   

    # For right click
    if fingers[2]==1 and is_pinching:
        if not rga:
            pyautogui.rightClick()
            rga = True
    else:
        rga = False

    #for minimizing window
    if gesture == "Fist":
        if not minga:
            pyautogui.hotkey('winleft', 'down')
            minga = True
    else:
        minga = False
                        
    #for navigating taskbar
    if gesture == "Pinky":
        if not nav:
            pyautogui.hotkey('winleft', 't')
            nav = True
    else:
        nav = False
            
    #for enter key
    if gesture == "Peace Sign":
        if not ent:
            pyautogui.hotkey('enter')
            ent = True
    else:
        ent = False