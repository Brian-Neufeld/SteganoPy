
from cgitb import enable
from cmath import nan
from faulthandler import disable
from pickletools import uint8
from sre_parse import State
import numpy as np
import PIL
from tkinter import *
from PIL import ImageTk,Image 
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import math
import pydub

imgwidth = 0
imgheight = 0
wscale = 1
hscale = 1

imgfilename = 1
audiofilename = 1


root = Tk()
root.geometry('1368x720')
#root.attributes('-fullscreen', True)
#root.resizable(0,0)
root.title("SteganoPy")

tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Image encoding')
tabControl.add(tab2, text ='Image decoding')
tabControl.add(tab3, text ='Audio encrypting')
tabControl.pack(expand = 1, fill ="both")

def get_digit(number, n):
    return number // 10**n % 10

def select_image_file():
    global imgfilename
    global img
    global img1
    global imgwidth
    global imgheight, wscale, hscale
    filetypes = (
        ("Image files", ("*.jpg", "*.png")),
        ("All files", "*.*")
    )

    imgfilename = fd.askopenfilename(
        title = "Open a File",
        initialdir="/",
        filetypes=filetypes
    )

    imgfilename = "".join(imgfilename)
    


    img = Image.open(imgfilename)
    img1 = ImageTk.PhotoImage(img)

    openimgfilename.config(text=imgfilename.split("/")[-1])

    imgwidth = img1.width()
    imgheight = img1.height()

    

    if imgwidth > imgheight:
        wscale = 1
        hscale = imgheight / imgwidth
    elif imgheight > imgwidth:
        hscale = 1
        wscale = imgwidth / imgheight
    elif imgwidth == imgheight:
        wscale = 1
        hscale = 1
    
    print(wscale)
    print(hscale)

    w = int(500 * wscale)
    h = int(500 * hscale)
    resize_img = img.resize((w, h))
    img = ImageTk.PhotoImage(resize_img)
    disp_inputimg.config(image=img)
    disp_inputimg.image = img

    #disp_img2.config(image=img)
    #disp_img2.image = img

    baseImgdims.config(text = f'witdth: {imgwidth} height: {imgheight}')
    baseImgdims.place_configure(y=500*hscale+120)
    
    inputimgFrame.config(width=(500*wscale+8), height=(500*hscale+8))
    

    if imgfilename == 1 or audiofilename == 1:
        preview.config(state="disabled")
        encode_button.config(state="disabled")
    elif imgfilename != 1 and audiofilename == 1:
        decode_button.config(state="normal")
    else:
        preview.config(state="normal")
        encode_button.config(state="normal")
        decode_button.config(state="normal")

    
    return imgfilename

def select_audio_file():
    global audiofilename
    filetypes = (
        ("Audio files", ("*.mp3")),
        ("All files", "*.*")
    )

    audiofilename = fd.askopenfilename(
        title = "Open a File",
        initialdir="/",
        filetypes=filetypes
    )

    audiofilename = "".join(audiofilename)

    if imgfilename == 1 or audiofilename == 1:
        preview.config(state="disabled")
        encode_button.config(state="disabled")
        decode_button.config(state="disabled")
    else:
        preview.config(state="normal")
        encode_button.config(state="normal")
        decode_button.config(state="normal")

    openaudiofilename.config(text=audiofilename.split("/")[-1])

    return audiofilename

def previewEncode():
    print(imgfilename)
    im = Image.open(imgfilename)
    
    a = np.array(im)

    

    a[0][0][0] = 0

    audioclip = pydub.AudioSegment.from_mp3(audiofilename)
    audioarray = np.array(audioclip.get_array_of_samples())
    audioarray = audioarray + (2**16)/2
    audioarray = np.rint((audioarray / 2**16) * 999)

    
    for x in range(len(a)):
        if x < 500:
            print(x)
            for y in range(len(a[x])):
                if y < 500:
                    for z in range(len(a[x][y])):
                        
                        if a[x][y][z] >= 250:
                            a[x][y][z] = 250
                            

                        a[x][y][z] = round(a[x][y][z]/10) * 10
                        
                        if x*len(a[x])+y < len(audioarray):
                            digit = get_digit(audioarray[x*len(a[x])+y], z)
                            if a[x][y][z] == 250 and digit > 5:
                                a[x][y][z] = 240
                            colourValue = int(a[x][y][z]) + int(digit)

                            if colourValue >= 256:
                                colourValue = 255

                            a[x][y][z] = colourValue

    

    imgPreviewout = Image.fromarray(a)
    imgPreview = ImageTk.PhotoImage(imgPreviewout)

    imgwidth = imgPreview.width()
    imgheight = imgPreview.height()


    if imgwidth >= 500 and imgheight >= 500:
        imgPreviewout = imgPreviewout.crop((0,0,499,499))
    elif imgwidth < 500 and imgheight >= 500:
        imgPreviewout = imgPreviewout.crop((0,0,imgwidth-1,499))
    elif imgwidth >= 500 and imgheight < 500:
        imgPreviewout = imgPreviewout.crop((0,0,499,imgheight-1))
    if imgwidth < 500 and imgheight < 500:
        imgPreviewout = imgPreviewout.crop((0,0,imgwidth-1,imgheight-1))
        

    
    imgPreviewout = ImageTk.PhotoImage(imgPreviewout)

    if imgwidth < 500:
        outputFrame.config(width=(imgwidth+8))
    else:
        outputFrame.config(width=508)
    if imgheight < 500:
        outputFrame.config(height=(imgheight+8))
    else:
        outputFrame.config(height=508)

    disp_img2.config(image=imgPreviewout)
    disp_img2.image = imgPreviewout

def encoding():
    f = fd.asksaveasfile(mode='w', defaultextension=".png")

    im = Image.open(imgfilename)
    
        
    a = np.array(im)

    audioclip = pydub.AudioSegment.from_mp3(audiofilename)
    audioarray = np.array(audioclip.get_array_of_samples())
    audioarray = audioarray + (2**16)/2
    audioarray = np.rint((audioarray / 2**16) * 999)

    print(len(a))

    for x in range(len(a)):
        print(x)
        for y in range(len(a[x])):
            for z in range(len(a[x][y])):
                
                if a[x][y][z] >= 250:
                    a[x][y][z] = 250
                    

                a[x][y][z] = round(a[x][y][z]/10) * 10
                
                if x*len(a[x])+y < len(audioarray):
                    digit = get_digit(audioarray[x*len(a[x])+y], z)
                    if a[x][y][z] == 250 and digit > 5:
                        a[x][y][z] = 240
                    colourValue = int(a[x][y][z]) + int(digit)

                    if colourValue >= 256:
                        colourValue = 255

                    a[x][y][z] = colourValue

                
                #print(str(digit) + "  " + str(audioarray[x*len(a[x])+y]))
                

    print(len(audioarray))

   

    im2 = Image.fromarray(a)
    #im2 . show()
    im2.save("E://Programming/Projects/audio image encoding/IMG.png", format="png")

def decoding():
    global imgfilename
    imgdecode = Image.open(imgfilename)
    
    a = np.asarray(imgdecode)

    audioarray = np.zeros(len(a)*len(a[0]))

    

    for x in range(len(a)):
        print(x)
        for y in range(len(a[x])):
            #for z in range(len(a[x][y])):
            
            audioarray[x*len(a[x])+y] = get_digit(a[x][y][0], 0) + get_digit(a[x][y][1], 0)*10 + get_digit(a[x][y][2], 0)*100
            if int(audioarray[x*len(a[x])+y]) == 0:
                audioarray[x*len(a[x])+y] += 500

    audioarray = (audioarray / 999)*(2**16) - ((2**16)/2)

   

    y = np.int16(audioarray)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=48000, sample_width=2, channels=1)
    song.export("decoded audio.mp3", format="mp3", bitrate="48k")




open_img_button = tk.Button(
    tab1,
    text='Open an image file',
    height = 2, 
    width=20,
    command=select_image_file
)

open_img_button2 = tk.Button(
    tab2,
    text='Open an image file',
    height = 2, 
    width=20,
    command=select_image_file
)

open_audio_button = tk.Button(
    tab1,
    text='Open an audio file',
    height = 2, 
    width=20,
    command=select_audio_file
)

preview = tk.Button(
    tab1,
    text='Preview',
    height = 2, 
    width=20,
    command=previewEncode
)

encode_button = tk.Button(
    tab1,
    text='Encode',
    height = 2, 
    width=20,
    command=encoding
)

decode_button = tk.Button(
    tab2,
    text='Decode',
    height = 2, 
    width=20,
    command=decoding
)

baseImgdims = tk.Label(
    tab1,
    text=f'witdth: {imgwidth} height: {imgheight}', 
    bd=2, 
    relief=SUNKEN
)  

openaudiofilename = tk.Label(
    tab1,
    text="None Selected", 
    bd=2, 
    relief=SUNKEN
)  

openimgfilename = tk.Label(
    tab1,
    text="None Selected", 
    bd=2, 
    relief=SUNKEN
)  


inputimgFrame = tk.Frame(
    tab1,
    width=(500*wscale+8), 
    height=(500*hscale+8), 
    bd=2, 
    relief=SUNKEN
)

disp_inputimg = tk.Label()

baseFramedecode = tk.Frame(
    tab2, 
    width=(500*wscale+8), 
    height=(500*hscale+8), 
    bd=2, 
    relief=SUNKEN
)

disp_img3 = tk.Label()

outputFrame = tk.Frame(
    tab1, 
    width=(508), 
    height=(508), 
    bd=2, 
    relief=SUNKEN
)

disp_img2 = tk.Label()

#LOD_slider = Scale(tab1, from_=0, to=10, orient=HORIZONTAL)

open_img_button.place(x=0, y=5)
open_img_button2.place(x=0, y=5)

open_audio_button.place(x=0, y=55)

preview.place(x=0, y=105)
if imgfilename == 1 or audiofilename == 1:
    preview.config(state=DISABLED)
    encode_button.config(state=DISABLED)
    decode_button.config(state=DISABLED)

encode_button.place(x=0, y=155)
decode_button.place(x=0, y=55)



inputimgFrame.place(x=173, y=105)
disp_inputimg.place(x=176, y=130)
baseImgdims.place(x=173, y=620)

outputFrame.place(x=773, y=105)
disp_img2.place(x=776, y=130)


openimgfilename.place(x=173, y=15)
openaudiofilename.place(x=173, y=65)

#LOD_slider.place(x=173, y=105)



#open_button.pack(expand=True)


# run the application
root.mainloop()

