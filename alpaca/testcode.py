import numpy as np
from PIL import Image
import os
import glob

def ConvertCSV(inputCsvFile, OutputImageNameAndPath):
    with open(inputCsvFile) as file:
        array = np.loadtxt(file, delimiter=',', skiprows=1)
        # image = Image.fromarray(array, "L") # 'L' -> Grayscale, 'RGB' -> RGB
        image = Image.fromarray(array, "RGBA")  # 'L' -> Grayscale, 'RGB' -> RGB


        image.save(OutputImageNameAndPath)


if __name__ == "__main__":
    
    #------- For Reading all CSV Files --------#
    tpath = "./data/SLM.JO/"
    csv_generic_path = tpath + "*.csv"

    
    csv_path_array = glob.glob(csv_generic_path)
    #------------------------------------------#
    
    #------ For Saving Resultant images ------ #
    save_folder_name = "dataImages"
    
    if not os.path.exists(save_folder_name ):
        os.makedirs(save_folder_name )
    #------------------------------------------#
    
    
    for csv_path in csv_path_array:
        base_name = csv_path.split('\\')[-1]
        saving_name = base_name[0:-4]+".png"
        saving_path = "./"+save_folder_name +"/"+saving_name
        saving_path = tpath + saving_name
        print(saving_path)
        ConvertCSV(csv_path,saving_path) # Required Function , All CSV->Images through this program

    #ConvertCSV("./data/data2.csv","./TestingManualImage2.png") # [Commented yet] Required Function, Manual implementation testing
    print("DONE!")

    