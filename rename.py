#you can rename the file after scaping some images from website

import os


try:
    fname=input("Please insert the name for the directory：")
    #this name is for the directory where you use to save the images
    oldpath = os.path.join(os.getcwd(),fname)
    files = os.listdir(oldpath)
except:
    print("Please check if the name is correct.")
else:
    count = 1

    for file in files:
        oldname=os.path.join(oldpath,file)
        newname = os.path.join(oldpath,(fname+'_'+str(count)))
        os.rename(oldname,newname)
        count=count+1
