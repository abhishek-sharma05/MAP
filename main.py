import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import schedule

ARDUINO_PORT='COM8'
medicine_locations=[]

class Medicine:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

class Application:
    def __init__(self, master, medicines):
        self.master = master
        self.medicines = medicines
        self.scheduled_time = None
        master.title("Select Medicine")
        self.listbox = tk.Listbox(master)
        self.listbox.pack()
        for medicine in self.medicines:
            self.listbox.insert(tk.END, medicine.name)
        self.button = ttk.Button(master, text="Schedule Administration", command=self.schedule_coordinates)
        self.button.pack()
        self.time_entry_label = tk.Label(master, text="Enter Time (HH:MM): ")
        self.time_entry_label.pack()
        self.time_entry = tk.Entry(master)
        self.time_entry.pack()

    def send_coordinates_to_arduino(x, y, z):
        ser = serial.Serial(ARDUINO_PORT, 9600) 
        ser.write(f"{x},{y},{z}\n".encode())
        ser.close()

    def send_coordinates_at_designated_time(x, y, z):
        print(f"Sending coordinates (x,y,z): {x}, {y}, {z} at {schedule.next_run()}")  # print scheduled time to console
        Application.send_coordinates_to_arduino(x, y, z)
        #ser = serial.Serial(ARDUINO_PORT, 9600) 
        #ser.write(f"{x},{y},{z}\n".encode())
        #ser.close()

    def schedule_coordinates(self):
        selection = self.listbox.curselection()
        if selection:
            medicine = self.medicines[selection[0]]
            print("Scheduling coordinates for medicine:", medicine.name, "to be sent to Arduino...")
            scheduled_time = self.time_entry.get()
            self.scheduled_time = scheduled_time 
            x, y, z = medicine.coordinates
            schedule.every().day.at(scheduled_time).do(Application.send_coordinates_at_designated_time, x, y, z)
            print("Coordinates for medicine:", medicine.name, "scheduled to be sent at", scheduled_time)



def detect_medicine(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_medicines = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100:
            continue
        cv2.drawContours(image, [contour], 0, (0, 0, 255), -1)
        barcode = decode(gray, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE39])
        if barcode:
            barcode_data = barcode[0].data.decode('utf-8')
            medicine = next((med for med in medicine_locations if med.name == barcode_data), None)
            if not medicine:
                medicine = Medicine(barcode_data, contour)
                medicine_locations.append(medicine)
            else:
                medicine.coordinates = contour
            detected_medicines.append(medicine)
    for medicine in detected_medicines:
        print("Detected medicine:", medicine.name, "at coordinates:", medicine.coordinates)
    return detected_medicines


def update_gui(app, frame):
    detected_medicines = detect_medicine(frame)
    print("Detected medicines:", detected_medicines)
    if detected_medicines:
        for medicine in detected_medicines:
            print("Detected medicine:", medicine.name, "at coordinates:", medicine.coordinates)
    app.medicines = medicine_locations
    app.listbox.delete(0, tk.END)
    for medicine in app.medicines:
        app.listbox.insert(tk.END, medicine.name)
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    app.label.config(image=imgtk)
    app.label.img = imgtk
    app.label.after(10, update_gui, app, frame)


def main():
    cap = cv2.VideoCapture(1)
    root = tk.Tk()
    app = Application(root, medicine_locations)
    label = tk.Label(root)
    label.pack()
    for medicine in medicine_locations:
        print("Medicine:", medicine.name, "Coordinates:", medicine.coordinates)
    def update_gui_wrapper():
        ret, frame = cap.read()
        if not ret:
            root.after(10, update_gui_wrapper)
            return
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        detected_medicines = detect_medicine(frame)
        app.medicines = medicine_locations + detected_medicines
        app.listbox.delete(0, tk.END)
        for medicine in app.medicines:
            app.listbox.insert(tk.END, medicine.name)
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        label.config(image=imgtk)
        label.img = imgtk
        root.after(10, update_gui_wrapper)
    root.after(10, update_gui_wrapper)
    root.mainloop()
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()