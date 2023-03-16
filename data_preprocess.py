from PIL import Image
from autocrop import Cropper
import os
import matplotlib.pyplot as plt
import shutil
import torchvision.transforms

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
        self.ori_nonsmoking_path = "./data/not_smoking/"

        self.clean_smoking_path = "./cleaned_data/clean_smoking/"
        self.clean_nonsmoking_path = "./cleaned_data/clean_nonsmoking/"

        self.discarded_smoking = "./discarded_data/discarded_data_smoking/discarded/"
        self.error_smoking = "./discarded_data/discarded_data_smoking/error_data/"
        
        self.discarded_nonsmoking = "./discarded_data/discarded_data_nonsmoking/discarded/"
        self.error_nonsmoking = "./discarded_data/discarded_data_nonsmoking/error_data/"

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
                shutil.copy2(self.ori_smoking_path + smoking, "./discarded_data/discarded_data_smoking/error_data/")
                pass
            if img_array is not None:
                # save the photo to cleaned_data/smoking
                filename = "smoking" + str(count)
                img = Image.fromarray(img_array)
                img.save(self.clean_smoking_path + filename + self.clean_img_type)
                count += 1
            else:
                shutil.copy2(self.ori_smoking_path + smoking, "./discarded_data/discarded_data_smoking/discarded/")

    def image_resizer_nonsmoking(self):
        """only keeps images with face facing camera
        this method losses roughly 75% of data
        """
        cropper = Cropper(width = self.resolution[0], 
                          height = self.resolution[1], 
                          face_percent = 60)
        count = 0
        for nonsmoking in os.listdir(self.ori_nonsmoking_path):
            # if count == 10:
            #     break
            try:
                img_array = cropper.crop(self.ori_nonsmoking_path + nonsmoking)
            except:
                # some problem with img
                shutil.copy2(self.ori_nonsmoking_path + nonsmoking, "./discarded_data/discarded_data_nonsmoking/error_data/")
                pass
            if img_array is not None:
                # save the photo to cleaned_data/smoking
                filename = "nonsmoking" + str(count)
                img = Image.fromarray(img_array)
                img.save(self.clean_nonsmoking_path + filename + self.clean_img_type)
                count += 1
            else:
                shutil.copy2(self.ori_nonsmoking_path + nonsmoking, "./discarded_data/discarded_data_nonsmoking/discarded/")

    def image_resizer_nonsmoking2(self):
        """only keeps images with face facing camera
        this method losses roughly 75% of data
        """
        cropper = Cropper(width = self.resolution[0], 
                          height = self.resolution[1], 
                          face_percent = 60)
        count = 0
        for nonsmoking_repo in os.listdir("./lfw_funneled"):
            if count == 5:
                break
            for nonsmoking in os.listdir("./lfw_funneled/" + nonsmoking_repo):

                try:
                    img_array = cropper.crop("./lfw_funneled/" + nonsmoking_repo + "/" +nonsmoking)
                except:
                    # some problem with img
                    shutil.copy2("./lfw_funneled/" + nonsmoking_repo + "/" + nonsmoking, "./discarded_data/discarded_data_nonsmoking/error_data/")
                    pass
                if img_array is not None:
                    # save the photo to cleaned_data/smoking
                    filename = "anonsmoking" + str(count)
                    img = Image.fromarray(img_array)
                    img.save(self.clean_nonsmoking_path + filename + self.clean_img_type)
                    count += 1
                else:
                    shutil.copy2("./lfw_funneled/" + nonsmoking_repo + "/" + nonsmoking, "./discarded_data/discarded_data_nonsmoking/discarded/")

    def image_reziser_preprocessed(self):
        """resize preprocessed data. 
        """
        transform = torchvision.transforms.Resize(size=(224, 224))
        count = 0
        for smoking in os.listdir("./manual_not_processed"):
            img = Image.open("./manual_not_processed/" + smoking)
            img = transform(img)
            # img = Image.fromarray(img)
            img.save("./cleaned_data/manual_clean_smoking/" + "msmoking" + str(count) + self.clean_img_type)
            count += 1



# raise Exception("\nAre You Sure To Run It?\nIt overwrites cleaned_data folder")
d = DataProcess()
# d.image_resizer_nonsmoking2()
# d.image_reziser_preprocessed()



