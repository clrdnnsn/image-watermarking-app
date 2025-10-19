import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    pass

WATERMARK_WIDTH = 60
IMAGE_HEIGHT = 675
IMAGE_WIDTH = 1200

class WatermarkApp:
    def __init__(self):
        self.frame1 = tk.Frame(root)
        self.frame1.grid(row=0, column=0, rowspan=6, columnspan=4, sticky="nsew")
        for column in range(0,4):
            self.frame1.columnconfigure(column, weight=3)
        for row in range(0,6):
            self.frame1.rowconfigure(row, weight=1)

        self.upload_button = tk.Button(self.frame1, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=0,column=0, columnspan=2, pady=(20,0))

        self.watermark_upload_button = tk.Button(self.frame1, text="Upload watermark", command=self.upload_watermark)
        self.watermark_upload_button.grid(row=0,column=3, columnspan=2, padx=(0,100) , pady=(20,0), sticky="w")

        self.text = tk.Label(self.frame1, text="Position Watermark:")
        self.text.grid(row=4, column=0, sticky="e")

        self.text = tk.Label(self.frame1, text="x: ")
        self.text.grid(row=4, column=1, sticky="e", padx=15)

        self.text = tk.Label(self.frame1, text="y : ")
        self.text.grid(row=4, column=2, sticky="e", padx=15)

        self.watermark_x_position = tk.Entry(self.frame1, width=8)
        self.watermark_x_position.grid(row=4,column=2, sticky="w")

        self.watermark_y_position = tk.Entry(self.frame1, width=8)
        self.watermark_y_position.grid(row=4,column=3, sticky="w")

        self.background_canvas = tk.Canvas(self.frame1, background="grey", bd=0)
        self.background_canvas.grid(row=1, rowspan=3, column=0, columnspan=5, padx=80, pady=25, sticky="nsew")

        self.image_label = tk.Label(self.frame1, bd=0)
        self.image_label.place(x=83,y=153)

        self.watermark_img_label = tk.Label(self.frame1, bd=0)
        self.watermark_img_label.place(x=83,y=153)

        self.apply_button = tk.Button(self.frame1,
                                      text="Apply",
                                      command=lambda: self.position_watermark(self.watermark_x_position.get(),self.watermark_y_position.get()))
        self.apply_button.grid(row=5, column=0, columnspan=5, pady=10)

        self.screenshot_button = Button(self.frame1, text="Download", command=lambda: self.capture_frame(self.image_label, self.watermark_img_label))
        self.screenshot_button.grid(row=6, column=0, columnspan=5, pady=(0,20))

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            try:
                # Open the image using Pillow
                img = Image.open(file_path)

                original_width, original_height = img.size
                new_height = IMAGE_HEIGHT
                new_width = IMAGE_WIDTH
                aspect_ratio = original_height / original_width

                if original_width > original_height:
                    original_width = new_width
                    new_height = int(new_width * aspect_ratio)
                    resized_img = img.resize((original_width, new_height), Image.LANCZOS)

                else:
                    new_width = int(new_height * aspect_ratio)
                    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # Convert to Tkinter PhotoImage
                img_tk = ImageTk.PhotoImage(resized_img)

                # Update the label with the new image
                self.image_label.config(image=img_tk, anchor="nw")
                self.image_label.image = img_tk  # Keep a reference to prevent garbage collection

            except Exception as e:
                print(f"Error loading image: {e}")

    def upload_watermark(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            try:
                # Open the image using Pillow
                watermark_img = Image.open(file_path)

                original_width, original_height = watermark_img.size
                new_width = WATERMARK_WIDTH

                aspect_ratio = original_height / original_width
                new_height = int(new_width * aspect_ratio)

                resized_img = watermark_img.resize((new_width, new_height), Image.LANCZOS)

                watermark_img_tk = ImageTk.PhotoImage(resized_img)

                self.watermark_img_label.config(image=watermark_img_tk, anchor="nw")
                self.watermark_img_label.image = watermark_img_tk

            except Exception as e:
                print(f"Error loading image: {e}")

    def position_watermark(self, x, y):
        try:
            x = int(x) if x.strip() else 83
            y = int(y) if y.strip() else 153

            if x < 83:
                x = 83

            if y < 153:
                y = 153

            if x > 1220:
                x = 1223

            if y > 765:
                y = 768

            self.watermark_img_label.place(x=x, y=y)

        except Exception as e:
            messagebox.showwarning("Error", "X and Y coordinates cannot be empty.")

    def capture_frame(self, widget1, widget2, filename="output.png"):
        # Force updates to ensure correct geometry
        widget1.update()
        widget2.update()

        # Find the bounding box that includes both widgets
        x1 = min(widget1.winfo_rootx(), widget2.winfo_rootx())
        y1 = min(widget1.winfo_rooty(), widget2.winfo_rooty())
        x2 = max(widget1.winfo_rootx() + widget1.winfo_width(),
                 widget2.winfo_rootx() + widget2.winfo_width())
        y2 = max(widget1.winfo_rooty() + widget1.winfo_height(),
                 widget2.winfo_rooty() + widget2.winfo_height())

        # Capture that combined area
        ImageGrab.grab(bbox=(x1, y1, x2, y2)).save(filename)
        print(f"Saved {filename}")

root = tk.Tk()
root.title("Image Watermark")
root.geometry("1350x1150")
for column in range(0, 4):
    root.columnconfigure(column, weight=1)
for row in range(0,6):
    root.rowconfigure(row, weight=1)
app = WatermarkApp()
root.mainloop()