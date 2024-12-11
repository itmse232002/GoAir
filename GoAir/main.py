from asyncio import current_task
import random
import cv2
import numpy as np
import speech_recognition as sr
from handTracker import HandTracker
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import random
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import re


user_db = {
    "itsme232002": "mummymummy",
    "rishu": "mummymummy",
    "akash": "mummymummy",
    "tusharbhatt": "mummymummy" 
}


def verify_login(username, password):
    if username in user_db and user_db[username] == password:
        return True
    return False

def on_login():
    username = username_entry.get()
    password = password_entry.get()

    if verify_login(username, password):
        messagebox.showinfo("Login Successful", "Welcome!")
        root.destroy() 
       
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = confirm_password_entry.get()
    phone = reg_phone_entry.get()
    email = reg_email_entry.get()
    captcha_input = captcha_entry.get()

    
    if len(phone) != 10 or not phone.isdigit():
        messagebox.showerror("Registration Failed", "Phone number must be 10 digits")
        return

  
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Registration Failed", "Invalid email format")
        return

    
    if captcha_input != captcha:
        messagebox.showerror("Registration Failed", "Incorrect CAPTCHA")
        return

   
    if password != confirm_password:
        messagebox.showerror("Registration Failed", "Passwords do not match")
        return
    
   
    if username in user_db:
        messagebox.showerror("Registration Failed", "Username already exists")
        return

   
    user_db[username] = password
    messagebox.showinfo("Registration Successful", "User registered successfully!")
    register_frame.pack_forget()  # Hide registration frame
    login_frame.pack()  # Show login form


def generate_captcha():
    global captcha
    captcha = ''.join(random.choices('0123456789', k=5))
    captcha_label.config(text=captcha)


def go_to_login():
    register_frame.pack_forget()  
    login_frame.pack()  


root = tk.Tk()
root.title("Login and Registration")

# Set the window size and make sure it's visible
root.geometry("300x400")

# Create a frame for the login form
login_frame = tk.Frame(root)


username_label = tk.Label(login_frame, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=on_login)
login_button.pack(pady=10)

register_label = tk.Label(login_frame, text="Not a user?")
register_label.pack(pady=5)

register_button = tk.Button(login_frame, text="Register", command=lambda: [login_frame.pack_forget(), register_frame.pack()])
register_button.pack(pady=5)

login_frame.pack()  # Display the login form initially


register_frame = tk.Frame(root)      # Create a frame for the registration form


reg_username_label = tk.Label(register_frame, text="Username:")
reg_username_label.pack(pady=5)
reg_username_entry = tk.Entry(register_frame)
reg_username_entry.pack(pady=5)

reg_password_label = tk.Label(register_frame, text="Password:")
reg_password_label.pack(pady=5)
reg_password_entry = tk.Entry(register_frame, show="*")
reg_password_entry.pack(pady=5)

confirm_password_label = tk.Label(register_frame, text="Confirm Password:")
confirm_password_label.pack(pady=5)
confirm_password_entry = tk.Entry(register_frame, show="&")
confirm_password_entry.pack(pady=5)

reg_phone_label = tk.Label(register_frame, text="Phone Number (10 digits):")
reg_phone_label.pack(pady=5)
reg_phone_entry = tk.Entry(register_frame)
reg_phone_entry.pack(pady=5)

reg_email_label = tk.Label(register_frame, text="Email:")
reg_email_label.pack(pady=5)
reg_email_entry = tk.Entry(register_frame)
reg_email_entry.pack(pady=5)


captcha_label = tk.Label(register_frame, text="", font=("Arial", 14), bg="white", width=10)
captcha_label.pack(pady=10)

generate_captcha_button = tk.Button(register_frame, text="Generate CAPTCHA", command=generate_captcha)
generate_captcha_button.pack(pady=5)

captcha_input_label = tk.Label(register_frame, text="Enter CAPTCHA:")
captcha_input_label.pack(pady=5)

captcha_entry = tk.Entry(register_frame)
captcha_entry.pack(pady=5)

register_button = tk.Button(register_frame, text="Register", command=register_user)
register_button.pack(pady=10)

back_to_login_button = tk.Button(register_frame, text="Back to Login", command=go_to_login)
back_to_login_button.pack(pady=5)


root.mainloop()





class ColorRect():
    def __init__(self, x, y, w, h, color, text='', alpha=0.5):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.alpha = alpha

    def drawRect(self, img, text_color=(255, 255, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2):
        alpha = self.alpha

       
        shadow_offset = 5
        shadow_color = (50, 50, 50)  # Dark gray for shadow effect
        shadow_x, shadow_y = self.x + shadow_offset, self.y + shadow_offset

       
        if shadow_y + self.h > img.shape[0]:
            shadow_y = img.shape[0] - self.h
        if shadow_x + self.w > img.shape[1]:
            shadow_x = img.shape[1] - self.w

        shadow_rec = img[shadow_y: shadow_y + self.h, shadow_x: shadow_x + self.w]
        dark_rect = np.ones(shadow_rec.shape, dtype=np.uint8) * np.array(shadow_color, dtype=np.uint8)
        res_shadow = cv2.addWeighted(shadow_rec, alpha, dark_rect, 1 - alpha, 1.0)

        if res_shadow is not None:
            img[shadow_y: shadow_y + self.h, shadow_x: shadow_x + self.w] = res_shadow

      
        bg_x1, bg_y1 = self.x, self.y                                      # Draw the main rectangle
        bg_x2, bg_y2 = self.x + self.w, self.y + self.h

       
        if bg_y2 > img.shape[0]:                                        # Ensure rectangle coordinates are within bounds
            bg_y1 = img.shape[0] - self.h                         
            bg_y2 = img.shape[0]
        if bg_x2 > img.shape[1]:
            bg_x1 = img.shape[1] - self.w
            bg_x2 = img.shape[1]

        bg_rec = img[bg_y1:bg_y2, bg_x1:bg_x2]
        white_rect = np.ones(bg_rec.shape, dtype=np.uint8)
        white_rect[:] = self.color
        res = cv2.addWeighted(bg_rec, alpha, white_rect, 1 - alpha, 1.0)

        if res is not None:
            img[bg_y1:bg_y2, bg_x1:bg_x2] = res

        
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 0, 0), 3)

       
        text_size = cv2.getTextSize(self.text, fontFace, fontScale, thickness)
        text_width, text_height = text_size[0]
        text_x = int(self.x + self.w / 2 - text_width / 2)
        text_y = int(self.y + self.h / 2 + text_height / 2)

        cv2.putText(img, self.text, (text_x, text_y), fontFace, fontScale, text_color, thickness)

    def isOver(self, x, y):
        return (self.x + self.w > x > self.x) and (self.y + self.h > y > self.y)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = f"{current_line} {word}".strip()
        (text_width, text_height), _ = cv2.getTextSize(test_line, font[0], font[1], font[2])
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def capture_speech():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()  # Convert text to lowercase
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""



def speech_to_search():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()  # Convert text to lowercase for uniformity
            print(f"Recognized text: {text}")

            if "search" in text:
                search_query = text.split("search", 1)[1].strip()  # Extract the query after "search"
                if search_query:
                    print(f"Searching for: {search_query}")
                    
                    # Perform the web search
                    search_url = f"https://www.bing.com/search?q={search_query.replace(' ', '+')}"  # Encode spaces in URL
                    headers = {
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.180 Safari/537.36"
                        )
                    }
                    response = requests.get(search_url, headers=headers)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        results = []
                        for item in soup.find_all('li', {'class': 'b_algo'}):
                            title = item.find('a').text
                            link = item.find('a')['href']
                            results.append((title, link))

                        if results:
                            print("Top search results:")
                            for idx, (title, link) in enumerate(results[:5], start=1):  # Display top 5 results
                                print(f"{idx}. {title}\n   {link}\n")
                        else:
                            print("No results found.")
                    else:
                        print(f"Failed to retrieve search results. Status code: {response.status_code}")
                else:
                    print("Please specify what to search for.")
            else:
                print("No 'search' keyword detected. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
#if __name__ == "__main__":
 #   while True:
  #      speech_to_search()
  
  

def recognize_and_convert_shapes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv2.boundingRect(approx)

        if len(approx) == 4:
            aspectRatio = float(w) / h
            if 0.9 <= aspectRatio <= 1.1:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
        elif len(approx) > 5:
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
        else:
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                radius = int(np.sqrt(M['m00'] / np.pi))
                cv2.circle(image, (cX, cY), radius, (0, 255, 0), 2)

    return image


detector = HandTracker(detectionCon=0.8)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

canvas = np.zeros((720, 1280, 3), np.uint8)  
shapes_canvas = np.zeros((720, 1280, 3), np.uint8)  
px, py = 0, 0
color = (255, 0, 0)
brushSize = 5
eraserSize = 20

scroll_offset = 0
scroll_step = 100
max_scroll = 400

colorsBtn = ColorRect(200, 0, 100, 100, (120, 255, 0), 'Colors')
colors = []
for i in range(88):
    colors.append(ColorRect(300 + i * 100, 0, 100, 100, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
max_scroll = len(colors) * 100 - 1280

eraser = ColorRect(900, 0, 100, 100, (0, 0, 0), "Eraser")

clear = ColorRect(1000, 0, 100, 100, (100, 100, 100), "Clear")

pens = []
for i, penSize in enumerate(range(5,25,5)):
    pens.append(ColorRect(1100,50+100*i,100,100, (50,50,50), str(penSize)))

penBtn = ColorRect(1100, 0, 100, 50, color, 'Pen')
boardBtn = ColorRect(50, 0, 100, 100, (255,255,0), 'Board')


whiteBoard = ColorRect(50, 120, 1020, 580, (255,255,255),alpha = 0.6)

ccBtn = ColorRect(1180, 310, 100, 100, (255, 165, 0), "Type")  


textBtn = ColorRect(1200, 0, 100, 100, (255, 0, 255), 'Text')

shapeToggleBtn = ColorRect(700, 0, 100, 100, (0, 255, 255), 'Shapes')
shape_recognition_enabled = False

textToDisplay = ""
hideBoard = True
hideColors = True
hidePenSizes = True
hideText = True
coolingCounter = 20

prev_x, prev_y = None, None

while True:
    if coolingCounter:
        coolingCounter -= 1

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.flip(frame, 1)

    detector.findHands(frame)
    positions = detector.getPostion(frame, draw=False)
    upFingers = detector.getUpFingers(frame)

    if upFingers:
        x, y = positions[8][0], positions[8][1]
        if prev_x is not None and prev_y is not None:
            dx, dy = x - prev_x, y - prev_y
            if abs(dx) > 30:
                if dx > 0:
                    scroll_offset = min(max_scroll, scroll_offset + scroll_step)
                else:
                    scroll_offset = max(0, scroll_offset - scroll_step)

        prev_x, prev_y = x, y

        if upFingers[1] and not whiteBoard.isOver(x, y):
            px, py = 0, 0

            if not hidePenSizes:
                for pen in pens:
                    if pen.isOver(x, y):
                        brushSize = int(pen.text)
                        pen.alpha = 0
                    else:
                        pen.alpha = 0.5

            if not hideColors:
                for cb in colors:
                    if cb.isOver(x, y):
                        color = cb.color
                        cb.alpha = 0
                    else:
                        cb.alpha = 0.5

                if clear.isOver(x, y):
                    clear.alpha = 0
                    canvas = np.zeros((720, 1280, 3), np.uint8)
                    shapes_canvas = np.zeros((720, 1280, 3), np.uint8)
                else:
                    clear.alpha = 0.5
                    
                    
                if eraser.isOver(x, y) and not coolingCounter:
                    coolingCounter = 10
                    eraser.alpha = 0
                    color = (0, 0, 0)  # Set color to black for erasing
                    brushSize = eraserSize  # Use a larger brush size for erasing
                else:
                    eraser.alpha = 0.5

            if colorsBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                colorsBtn.alpha = 0
                hideColors = not hideColors
                colorsBtn.text = 'Colors' if hideColors else 'Hide'
            else:
                colorsBtn.alpha = 0.5

            if penBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                penBtn.alpha = 0
                hidePenSizes = not hidePenSizes
                penBtn.text = 'Pen' if hidePenSizes else 'Hide'
            else:
                penBtn.alpha = 0.5

            if boardBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                boardBtn.alpha = 0
                hideBoard = not hideBoard
                boardBtn.text = 'Board' if hideBoard else 'Hide'
            else:
                boardBtn.alpha = 0.5

            if textBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                textBtn.alpha = 0
                hideText = not hideText
                textBtn.text = 'Text' if hideText else 'Hide'
                if not hideText:
                    textToDisplay = speech_to_search() 
                   # textToDisplay = capture_speech()
                else:
                    textToDisplay = ""
            else:
                textBtn.alpha = 0.5
                
                
            if ccBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                textBtn.alpha = 0
                hideText = not hideText
                textBtn.text = 'Type' if hideText else 'Hide'
                if not hideText:
                    #textToDisplay = speech_to_search() 
                    textToDisplay = capture_speech()
                else:
                    textToDisplay = ""
            else:
                textBtn.alpha = 0.5
                
          

                
                
            
            
            

           
            if shapeToggleBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                shapeToggleBtn.alpha = 0
                shape_recognition_enabled = not shape_recognition_enabled
                shapeToggleBtn.text = 'Shapes' if not shape_recognition_enabled else 'Hide Shapes'
            else:
                shapeToggleBtn.alpha = 0.5

        elif upFingers[1] and not upFingers[2]:
            if whiteBoard.isOver(x, y) and not hideBoard:
                if shape_recognition_enabled:
                   
                    cv2.circle(shapes_canvas, positions[8], brushSize, color, -1)
                    if px == 0 and py == 0:
                        px, py = positions[8]
                    cv2.line(shapes_canvas, (px, py), positions[8], color, brushSize * 2)
                    px, py = positions[8]
                else:
                    # Draw on canvas
                    cv2.circle(canvas, positions[8], brushSize, color, -1)
                    if px == 0 and py == 0:
                        px, py = positions[8]
                    cv2.line(canvas, (px, py), positions[8], color, brushSize * 2)
                    px, py = positions[8]
        
            
            
        elif upFingers[1] and not upFingers[2]:
            if whiteBoard.isOver(x, y) and not hideBoard:
                if color == (0, 0, 0):  # Eraser mode
                    cv2.circle(canvas, positions[8], eraserSize, color, -1)
                else:
                    cv2.circle(canvas, positions[8], brushSize, color, -1)
                if px == 0 and py == 0:
                    px, py = positions[8]
                cv2.line(canvas, (px, py), positions[8], color, brushSize * 2)
                px, py = positions[8]
        
        
        else:
            px, py = 0, 0

    for i, cb in enumerate(colors):
        if isinstance(cb, ColorRect):
            cb.x = 300 + i * 100 - scroll_offset

    if not hideColors:
        for cb in colors:
            if isinstance(cb, ColorRect):
                cb.drawRect(frame)
        clear.drawRect(frame)

    if not hidePenSizes:
        for pen in pens:
            if isinstance(pen, ColorRect):
                pen.drawRect(frame)

    if not hideBoard:
        whiteBoard.drawRect(frame)

    if not hideText and textToDisplay:
        wrapped_text = wrap_text(textToDisplay, (cv2.FONT_HERSHEY_SIMPLEX, 1, 2), 1000)
        y_offset = 150
        for line in wrapped_text:
            cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            y_offset += 30

    colorsBtn.drawRect(frame)
    penBtn.drawRect(frame)
    boardBtn.drawRect(frame)
    textBtn.drawRect(frame)
    ccBtn.drawRect(frame)
    clear.drawRect(frame)
    eraser.drawRect(frame)
    shapeToggleBtn.drawRect(frame)  # Draw the new toggle button

    # Combine the two canvases
    if shape_recognition_enabled:
        canvas_with_shapes = recognize_and_convert_shapes(shapes_canvas.copy())
        gray = cv2.cvtColor(canvas_with_shapes, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, inv)
        frame = cv2.bitwise_or(frame, canvas_with_shapes)
    else:
        frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Paint App", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()


