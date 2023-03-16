from PIL import Image
from autocrop import Cropper
import os
import matplotlib.pyplot as plt
import shutil

class DataProcess:
    """preprocess images to 224x224 resolution
    split the data into 60% train 20% val 20% test
    """
    def __init__(self):
        # self.resolution = [width, height]
        self.resolution = [224, 224]
        # self.data_split = [train, val, test]
        self.data_split = [0.6, 0.2, 0.2] 
        self.ori_smoking_path = "./data/smoking/"
        self.nonsmoking_path = "./data/not_smoking"
        self.clean_smoking_path = "./cleaned_data/smoking/"
        self.clean_img_type = ".jpg"

    def image_resizer_smoking(self):
        """only keeps images with face facing camera
        this method losses roughly 75% of data
        """
        cropper = Cropper(width = self.resolution[0], 
                          height = self.resolution[1], 
                          face_percent = 60)
        count = 0
        for smoking in os.listdir(self.ori_smoking_path):
            # if count == 10:
            #     break
            try:
                img_array = cropper.crop(self.ori_smoking_path + smoking)
            except:
                # some problem with img
                shutil.copy2(self.ori_smoking_path + smoking, "./discarded_data_smoking/error_data/")
                pass
            if img_array is not None:
                # save the photo to cleaned_data/smoking
                filename = "smoking" + str(count)
                img = Image.fromarray(img_array)
                img.save(self.clean_smoking_path + filename + self.clean_img_type)
                count += 1
            else:
                shutil.copy2(self.ori_smoking_path + smoking, "./discarded_data_smoking/discarded/")


def main():
    raise Exception("\nAre You Sure To Run It?\nIt overwrites cleaned_data folder")
    d = DataProcess()
    d.image_resizer_smoking()

if __name__ == "__main__":
    main()

