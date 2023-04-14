# structure based on https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/image_example.py
import customtkinter
import os
from PIL import Image
import cv2
import numpy as np
import model_test
import torch
import joblib
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision
from facenet_pytorch import MTCNN
import torch
from PIL import Image, ImageDraw

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Are You Smoking")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "No_Smoking.png")), size=(26, 26))
        self.welcome_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bg_gradient.jpg")), size=(520-40, 450-30-40-15))
        self.upload_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "upload.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.camera_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "camera.png")), size=(20, 17))
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Are You Smoking", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=10, pady=20, sticky="w")

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.camera_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Camera",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.camera_image, anchor="w", command=self.video_frame_button_event)
        self.camera_frame_button.grid(row=2, column=0, sticky="ew")

        # create home frame
        self.image_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_label = customtkinter.CTkLabel(self.image_frame, text="Upload Your File to Get Started", image=self.welcome_image,
                                                                   height=300, width=500, compound="bottom",
                                                                   font=customtkinter.CTkFont(size=15, weight="bold"), text_color="black")
        self.image_label.grid(row=0, column=0, padx=20, pady=10, sticky="ns")

        self.upload_button = customtkinter.CTkButton(self.image_frame, text="Upload", image=self.upload_image, compound="right",
                                                     font=customtkinter.CTkFont(size=15), command=self.upload_button_event)
        self.upload_button.grid(row=4, column=0, padx=20, pady=10, sticky="s")

        # create second frame
        self.video_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.video_label = customtkinter.CTkLabel(self.video_frame, text="Waiting...", image=self.welcome_image,
                                                  height=300, width=500, compound="bottom",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"), text_color="black")
        self.video_label.grid(row=0, column=0, padx=20, pady=10)
        self.cap = None
        # select default frame
        self.select_frame_by_name("home")
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(keep_all=True, device=device)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.camera_frame_button.configure(fg_color=("gray75", "gray25") if name == "video_frame" else "transparent")

        # show selected frame
        if name == "home":
            self.image_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.image_frame.grid_forget()
        if name == "video_frame":
            self.video_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.video_frame.grid_forget()

    def home_button_event(self):
        self.cap.release()
        self.select_frame_by_name("home")

    def video_frame_button_event(self):
        self.cap = cv2.VideoCapture(1)
        self.camera()
        self.select_frame_by_name("video_frame")

    def upload_button_event(self):
        filetypes=[("Photos", ".png .jpg .jpeg"), ("Videos", ".mp4 .mov .avi")]
        
        self.filepath = customtkinter.filedialog.askopenfilename(filetypes = filetypes,
                                                            initialdir='/')
        curr_img = Image.open(self.filepath)

        w, h = curr_img.size
        w, h = self.image_dim(w, h)

        disp_img = self.model_connect(curr_img)
        disp_img = customtkinter.CTkImage(disp_img, size=(w, h))
        self.image_label.configure(image=disp_img)
        
    def image_dim(self, w, h):
        # 40 is x_padding * 2 #30 is upload button height, 40 is y_padding * 2, 15 is font height
        windows_w, windows_h = (520-40, 450-30-40-15-15) 
        aspect_ratio = float(w / h)
        if w > h:
            w = windows_w
            h = w / aspect_ratio
        else:
            h = windows_h
            w = aspect_ratio * h 
        return w, h

    def get_image_path(self):
        return self.filepath

    def smoking_detected(self, result: bool):

        if (self.cap == None or self.cap.isOpened() == False):
            # camera is on so update camera frame
            if (result):
                self.image_label.configure(text="Smoking", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="red")
            else:
                self.image_label.configure(text="Non-Smoking", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="black")
        else:
            if (result):
                self.video_label.configure(text="Smoking", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="red")
            else:
                self.video_label.configure(text="Non-Smoking", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="black")
            
    def model_connect(self, frame):
        
        # Detect faces
        boxes, _ = self.mtcnn.detect(frame)
        if (boxes is None):
            self.smoking_detected(False)
            return frame
        # Draw faces
        for box in boxes:
            frame_draw = frame.copy()
            draw = ImageDraw.Draw(frame_draw)
            for box in boxes:
                draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
            x = box[2] - box[0]
            y = box[3] - box[1]
            max_len = max(x, y) * 1.2
            box[0] -= max_len*0.1
            box[1] -= max_len*0.1
            box[2] = box[0] + max_len
            box[3] = box[1] + max_len  

        # Add to frame list
        frame = frame.crop(box=box)
        frame = frame.resize((224, 224), Image.BILINEAR)

        transform = transforms.Compose([transforms.PILToTensor()]) 
        dataset = [[transform(frame).float(), torch.tensor(0.)]]
        criterion = nn.BCEWithLogitsLoss()
        loader = torch.utils.data.DataLoader(dataset, batch_size=len(dataset), num_workers=0)

        # judge smoking here, put result in is_smoking
        print(model_test.classifier.evaluate(loader, criterion))
        is_smoking = bool(model_test.classifier.evaluate(loader, criterion)[0])

        self.smoking_detected(is_smoking)
        return frame_draw

    def camera(self):
        ret, frame = self.cap.read()
   
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            img = Image.fromarray(frame)
            w, h = img.size
            w, h = self.image_dim(w, h)

            disp_img = self.model_connect(img)
            disp_img = customtkinter.CTkImage(disp_img, size=(w, h))
            self.video_label.configure(image=disp_img)

            # self.model_connect(img)
            self.video_label.after(50, self.camera)
            

if __name__ == "__main__":

    app = GUI()
    app.mainloop()