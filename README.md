
# Medical Application Program

This Python script implements a medical application that utilizes computer vision techniques to detect medicines, schedules their administration, and controls an Arduino board for delivering the medicines at the scheduled time.

## Dependencies

- cv2 (OpenCV): For computer vision tasks.
- numpy: For numerical operations.
- pyzbar: For decoding barcodes.
- tkinter: For creating the GUI.
- PIL: For image processing.
- serial: For communicating with Arduino.
- schedule: For scheduling tasks.

## Functionality

1. Medicine Detection:
   - The script uses computer vision techniques to detect medicines from a video stream.
   - Medicines are detected by identifying barcodes on the packaging.
   - Detected medicines are stored in a list along with their coordinates.

2. GUI Application:
   - The script creates a graphical user interface (GUI) for the application.
   - The GUI displays a list of available medicines detected so far.
   - Users can select a medicine from the list and schedule its administration.
   - The scheduled time is entered by the user and stored.
   - When the scheduled time arrives, the coordinates of the selected medicine are sent to the Arduino board.

3. Arduino Communication:
   - The script communicates with an Arduino board connected to the computer via a serial port (configured with ARDUINO_PORT).
   - The Arduino board receives the coordinates (x, y, z) and can perform actions based on them (e.g., move a robotic arm).

## Usage

1. Install the required dependencies (mentioned above).
2. Connect an Arduino board to the computer and configure the ARDUINO_PORT variable accordingly.
3. Run the script.
4. The GUI window will appear, displaying the available medicines.
5. Select a medicine from the list and enter a time (in HH:MM format) to schedule its administration.
6. The coordinates of the medicine will be sent to the Arduino board at the scheduled time.

Note: Make sure to have a camera connected or integrated with your system to capture the video stream for medicine detection.
