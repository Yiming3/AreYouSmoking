# structure based on https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/image_example.py
import customtkinter
import os
from PIL import Image


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

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.home_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="Upload Your File to Get Started", image=self.welcome_image,
                                                                   height=300, width=500, compound="bottom",
                                                                   font=customtkinter.CTkFont(size=15, weight="bold"), text_color="black")
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10, sticky="ns")

        self.upload_button = customtkinter.CTkButton(self.home_frame, text="Upload", image=self.upload_image, compound="right",
                                                     font=customtkinter.CTkFont(size=15), command=self.upload_button_event)
        self.upload_button.grid(row=4, column=0, padx=20, pady=10, sticky="s")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def upload_button_event(self):
        filetypes=[("Photos", ".png .jpg .jpeg"), ("Videos", ".mp4 .mov .avi")]
        
        self.filepath = customtkinter.filedialog.askopenfilename(filetypes = filetypes,
                                                            initialdir='/')
        curr_img = Image.open(self.filepath)
        # 40 is x_padding * 2 #30 is upload button height, 40 is y_padding * 2, 15 is font height
        windows_w, windows_h = (520-40, 450-30-40-15-15) 
        w, h = curr_img.size
        aspect_ratio = float(w / h)

        if w > h:
            w = windows_w
            h = w / aspect_ratio
        else:
            h = windows_h
            w = aspect_ratio * h   

        curr_img = customtkinter.CTkImage(curr_img, size=(w, h))
        self.home_frame_large_image_label.configure(image=curr_img)
    
    def get_image_path(self):
        return self.filepath

    def smoking_detected(self, result: bool):
        if (result):
            self.home_frame_large_image_label.configure(text="Smoking", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="red")
        else:
            self.home_frame_large_image_label.configure(text="Non-Smoking", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="black")

    def model_connect(self):
        # --------------------------------------------
        # put your code below
        # to get the file path -> self.filepath or call self.get_image_path()



        # judge smoking here, put result in is_smoking
        is_smoking = True
        # put your code above
        # --------------------------------------------

        self.smoking_detected(is_smoking)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()