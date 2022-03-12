import numpy as np
from PIL import Image
import os
import glob

class csvToImage:
    def generatePixelArray(self):
        print('Generate Pixel Array')
        returnArray  = []
        counter = 0
        for r in range (0,256):
            # print(r)
            for g in range(0, 256):
                for b in range(0, 256):
                    # print(str(r),str(g), str(b))
                    returnArray.append([counter,(r,g,b)])
                    counter += 1
        return returnArray



    def convertImage(self, inputCsvFile, targetFolder):

        pixelArray = self.generatePixelArray();
        print('ConvertImage')
        blocksize = 50
        base_name = inputCsvFile.split('/')[-1]
        saving_name = base_name[0:-4] + ".png"
        print('csvToImage')
        with open(inputCsvFile) as file:
            array = np.loadtxt(file, delimiter=',', skiprows=1)
            print(array.shape)
            rows = array.shape[0] * blocksize
            cols = array.shape[1] * blocksize
            # print(rows)
            img = Image.new('RGB', (array.shape[1], array.shape[0]))
            rowcounter = 0
            for row in array:
                colcounter = 0
                print(row)
                for col in row:
                    print("LOOP:",colcounter, rowcounter)
                    # print(pixelArray[int(col)][1])
                    # print(pixelArray[int(col)][1][0])
                    # img.putpixel((colcounter, rowcounter), (100, 100, 100, 255))
                    # img.putpixel((colcounter, rowcounter), (pixelArray[col][1][0], pixelArray[col][1][1], pixelArray[col][1][2], 255))
                    # print(pixelArray[int(col)][1][1],)
                    # img.putpixel((colcounter, rowcounter), (100, 100, 100, 255))
                    img.putpixel((colcounter, rowcounter), (pixelArray[int(col*100)][1][0], pixelArray[int(col)][1][1], pixelArray[int(col)][1][2], 255))
                    colcounter += 1

                rowcounter += 1
            #
            # img.putpixel((3, 3), (200, 200, 100, 255))
            # img.putpixel((8, 3), (200, 200, 0, 255))
            # img.putpixel((9, 3), (200, 200, 200, 255))
            img.save(targetFolder+saving_name)

            resized_img = img.resize((cols,rows),resample=0,)
            resized_img.save(targetFolder+"big"+saving_name)


cObj = csvToImage()
csvFile = "./data/SLM.JO/test3.csv"
targetFolder = "./data/SLM.JO/"


cObj.convertImage(csvFile,targetFolder)
# cObj.generatePixelArray()



