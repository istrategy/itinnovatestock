import numpy as np
from PIL import Image
import os
import glob

class csvToImage:
    def generatePixelArrayFile(self):
        print('GENERATE FILE')
        a = np.array(self.generatePixelArray())
        print(a)
        np.savetxt('colors.csv', a, delimiter=',')
        print('File generated.')


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
                    if counter > 1000000:
                        break
        return returnArray



    def convertImage(self, inputCsvFile, targetFolder, bigFiles):

        pixelArray = self.generatePixelArray();
        print('ConvertImage')
        blocksize = 50
        base_name = inputCsvFile.split('\\')[-1]
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
                    arraypos = int(col *10)
                    img.putpixel((colcounter, rowcounter), (pixelArray[int(arraypos)][1][0], pixelArray[int(arraypos)][1][1], pixelArray[int(arraypos)][1][2], 255))
                    print(pixelArray[int(arraypos)])
                    colcounter += 1

                rowcounter += 1
            #
            # img.putpixel((3, 3), (200, 200, 100, 255))
            # img.putpixel((8, 3), (200, 200, 0, 255))
            # img.putpixel((9, 3), (200, 200, 200, 255))
            img.save(os.path.join(targetFolder , saving_name))
            if bigFiles == True:
                resized_img = img.resize((cols,rows),resample=0,)
                resized_img.save(os.path.join("./data/big/" , saving_name))

    def convertImages(self, sourceFolder,targetFolder,bigFiles):
        for subdir, dirs, files in os.walk(sourceFolder):
            # print(dirs)
            for dir in dirs:
                # loopdir = os.path.join(sourceFolder,dir)
                print(dir)
                for subdir1, dirs1, files1 in  os.walk(os.path.join(sourceFolder,dir)):
                    print(files1)
                    for file in files1:
                        print(file)
                        fullfilepath = os.path.join(sourceFolder,dir,file)
                        print(fullfilepath)
                        targetpath = os.path.join(targetFolder,dir)
                        if not os.path.exists(targetpath):
                            os.makedirs(targetpath)
                        print(targetpath)
                        self.convertImage(fullfilepath,targetpath,bigFiles)





            # for sdir in dirs:
            #     print(sdir)

            # for file in files:
            #     print(file)
                # os.path.join(subdir, file)
# cObj = csvToImage()
# csvFile = "./data/SLM.JO/2015-08-07.csv"
targetFolder = "./data/SLM.JO/"


sourceFolder = "./data/csv/SLM.JO/"

cObj = csvToImage()

# cObj.convertImage(csvFile,targetFolder)


sourceFolder = "./data/csv/SLM.JO/"
targetFolder = "./data/images/SLM.JO/"
bigFiles = True
cObj.convertImages(sourceFolder,targetFolder,bigFiles)


# cObj.generatePixelArray()


# cObj.generatePixelArrayFile()


