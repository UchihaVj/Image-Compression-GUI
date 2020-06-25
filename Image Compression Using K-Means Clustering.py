# Import module from tkinter for UI
from tkinter import *
from tkinter import filedialog


import cv2
from skimage import io
import numpy as np

from skimage import io
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from PIL import ImageTk, Image, ImageDraw


#It will open a file dialog which will let user to select an image 
def SelectImage():
    root.filename =  filedialog.askopenfilename(title = "Select Image file to Compress",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    #print (root.filename)


#Here the Compression of the image will take place
def Compression():
    
    user=var.get() #K value is taken from the slider and stored in user

    if (user==0):
        k=1

    else:
        k = int((255*user)//100)
    
    img = io.imread(root.filename) #Selected Image is read 
    
    img_data = (img / 255.0).reshape(-1, 3) #convertered to numpy array
    
    kmeans = MiniBatchKMeans(k).fit(img_data)
    k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]
    
    '''After K-means has converged, load the large image into your program and 
    replace each of its pixels with the nearest of the centroid colors you found
    from the small image.''' 

    root.k_img = np.reshape(k_colors, (img.shape))
    
    

def SaveImage():
    
    CompressImage=Image.fromarray((root.k_img * 255).astype(np.uint8)) #converting the processed numpy array to compress image 

    fn = filedialog.asksaveasfile(mode='w', filetypes = (("jpeg files","*.jpg"),("all files","*.*")),defaultextension=".jpg")
    
    if not fn:
        return

    try:
        CompressImage.save(fn, "JPEG")
        
    except AttributeError:
        print("Couldn't save image {}".format(image))


def Terminate():
    root.destroy() #to close the GUI


#creating instance of TK
root=Tk()

#Setting Backgroud color of the window
root.configure(background="white")

#Setting title for the window
root.title("Image Compression")

var = IntVar()

# Used to display text
Label(root, text="   Image Compression using K-Means Clustering   ",font=("times new roman",20),fg="white",bg="Navy",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

# Select Image Button
Button(root,text="SELECT IMAGE",font=("times new roman",15),bg="#0D47A1",fg='white',command=SelectImage).grid(row=2,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

# Select Compression  Value
Slider = Scale(root, from_=0, to=100,activebackground="navy",label="                                                      Select the Compression Percentage",variable = var,orient=HORIZONTAL,tickinterval=10).grid(row=3,columnspan=2,sticky=E+W+S,padx=5,pady=5)

# Select Compress Button
Button(root,text="COMPRESS IMAGE",font=("times new roman",15),bg="#0D47A1",fg='white',command=Compression).grid(row=4,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

# Select Save Button
Button(root,text="SAVE COMPRESS IMAGE",font=("times new roman",15),bg="#0D47A1",fg='white',command=SaveImage).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

Button(root,text="Exit",font=('times new roman',18),bg="maroon",fg="white",command=Terminate).grid(row=6,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

# Used to run the application, wait for an event to occur and process the event till the window is not closed
root.mainloop()
