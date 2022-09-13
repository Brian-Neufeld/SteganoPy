from turtle import bgcolor
import numpy as np
import PIL
from PIL import ImageTk,Image 
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import math
import pydub
from pydub.playback import play
import encryptionmodule
from time import perf_counter
import scipy
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from tkinter import messagebox

pygame.mixer.init(frequency=44100, size=-16, channels=1)

root = tk.Tk()
root.geometry('1500x850')
root.title("SteganoPy")


base_img_width = 0
base_img_height = 0
base_w_scale = 1
base_h_scale = 1

encoded_img_width = 0
encoded_img_height = 0
encoded_w_scale = 1
encoded_h_scale = 1


base_img_filename = 1
encoded_img_filename = 1
audio_filename = 1

encrypt_check = tk.IntVar()

tabControl = ttk.Notebook(root)
  

tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Image encoding')
tabControl.add(tab2, text ='Image decoding')
tabControl.add(tab3, text ='Audio encrypting')
tabControl.pack(expand = 1, fill ="both")

def get_digit(number, n):
    return number // 10**n % 10


class tab1_class:

    def __init__(self, master):

        global base_img_filename
        global audio_filename
        global audioarray

        global open_audio_file_btn, open_audio_file_btn, preview_btn, encode_btn

        open_img_file_btn = tk.Button(tab1, text="Open image file", height = 2, width = 20, command=self.open_img_file_fcn)
        open_img_file_btn.place(x=0, y=0)

        open_audio_file_btn = tk.Button(tab1, text='Open audio file', height = 2, width = 20, command=self.open_audio_file_fcn)
        open_audio_file_btn.place(x=0, y=55)

        preview_btn = tk.Button(tab1, text='Preview', height = 2, width = 20, command=self.preview_fcn)
        preview_btn.place(x=0, y=105)

        encode_btn = tk.Button(tab1, text='Encode', height = 2, width = 20, command=self.encode_fcn)
        encode_btn.place(x=0, y=155)



    def open_img_file_fcn(self):
        print("image file opened")

        filetypes = (
        ("Image files", ("*.jpg", "*.png")),
        ("All files", "*.*")
        )

        base_img_filename = fd.askopenfilename(
            title = "Open a File",
            initialdir="/",
            filetypes=filetypes
        )

        if base_img_filename == "":
            return

        base_img_filename = "".join(base_img_filename)

        img = Image.open(base_img_filename)
        img1 = ImageTk.PhotoImage(img)

        open_img_filename.config(text=base_img_filename.split("/")[-1])

        base_img_width = img1.width()
        base_img_height = img1.height()

        

        if base_img_width > base_img_height:
            base_w_scale = 1
            base_h_scale = base_img_height / base_img_width
        elif base_img_height > base_img_width:
            base_h_scale = 1
            base_w_scale = base_img_width / base_img_height
        elif base_img_width == base_img_height:
            base_w_scale = 1
            base_h_scale = 1
        
        print(base_w_scale)
        print(base_h_scale)

        w = int(500 * base_w_scale)
        h = int(500 * base_h_scale)
        resize_img = img.resize((w, h))
        img = ImageTk.PhotoImage(resize_img)
        disp_inputimg.config(image=img)
        disp_inputimg.image = img


        baseImgdims.config(text = f'witdth: {base_img_width} height: {base_img_height}')
        baseImgdims.place_configure(y=500*base_h_scale+120)
        
        inputimgFrame.config(width=(500*base_w_scale+8), height=(500*base_h_scale+8))
        

        if base_img_filename == 1 or audio_filename == 1:
            preview_btn.config(state="disabled")
            encode_btn.config(state="disabled")
        elif base_img_filename != 1 and audio_filename == 1:
            decode_button.config(state="normal")
        else:
            preview_btn.config(state="normal")
            encode_btn.config(state="normal")
            #decode_btn.config(state="normal")

        
        return base_img_filename

    def open_audio_file_fcn(self):
        filetypes = (
            ("Audio files", ("*.mp3", "*.wav")),
            ("All files", "*.*")
        )

        audio_filename = fd.askopenfilename(
            title = "Open a File",
            initialdir="/",
            filetypes=filetypes
        )

        if audio_filename == "":
            return

        audio_filename = "".join(audio_filename)

        if base_img_filename == 1 or audio_filename == 1:
            preview.config(state="disabled")
            encode_button.config(state="disabled")
            decode_button.config(state="disabled")
        else:
            preview.config(state="normal")
            encode_button.config(state="normal")
            decode_button.config(state="normal")

        if audio_filename != 1:
            play_audio_button.config(state="normal")
            encrypt_audio_button.config(state="normal")
            decrypt_audio_button.config(state="normal")

        open_audio_filename.config(text=audio_filename.split("/")[-1])
        open_audio_filename_tab3.config(text=audio_filename.split("/")[-1])

        audioclip = pydub.AudioSegment.from_mp3(audio_filename)
        audioarray = np.array(audioclip.get_array_of_samples())
        
        

        open_audio_length.config(text=f"{math.floor(len(audioarray)/(48000*60))}m:{(len(audioarray) % (48000*60))/48000}s")

        plotaudio()

        return audio_filename

    def preview_fcn(self):
        preview.config(state="disabled")

        im = Image.open(base_img_filename)
            
        a = np.array(im)
        a[0][0][0] = 0

        #audioclip = pydub.AudioSegment.from_mp3(audiofilename)
        #audioarray = np.array(audioclip.get_array_of_samples())
        #audioarray = audioarray + (2**16)/2
        #audioarray = np.rint((audioarray / 2**16) * 999)

        progressbar_tab1["value"] = 0
        pb_tab1_value_label['text'] = "                                            "
        root.update_idletasks()
        
        for x in range(len(a)):
            if x < 500:
                #print(x)
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

                if len(a) < 500:
                    progressbar_tab1["value"] += 1/len(a) * 100
                    pb_tab1_value_label['text'] = update_progress_label()
                    root.update_idletasks()
                else:
                    progressbar_tab1["value"] += 1/500 * 100
                    pb_tab1_value_label['text'] = update_progress_label()
                    root.update_idletasks()


        

        img_preview_out = Image.fromarray(a)
        img_preview = ImageTk.PhotoImage(img_preview_out)

        imgwidth = img_preview.width()
        imgheight = img_preview.height()


        if imgwidth >= 500 and imgheight >= 500:
            img_preview_out = img_preview_out.crop((0,0,499,499))
        elif imgwidth < 500 and imgheight >= 500:
            img_preview_out = img_preview_out.crop((0,0,imgwidth-1,499))
        elif imgwidth >= 500 and imgheight < 500:
            img_preview_out = img_preview_out.crop((0,0,499,imgheight-1))
        if imgwidth < 500 and imgheight < 500:
            img_preview_out = img_preview_out.crop((0,0,imgwidth-1,imgheight-1))
            

        
        img_preview_out = ImageTk.PhotoImage(img_preview_out)

        if imgwidth < 500:
            outputFrame.config(width=(imgwidth+8))
        else:
            outputFrame.config(width=508)
        if imgheight < 500:
            outputFrame.config(height=(imgheight+8))
        else:
            outputFrame.config(height=508)

        disp_img2.config(image=img_preview_out)
        disp_img2.image = img_preview_out

        if imgheight > 500:
            imgheight = 500

        preview_img_label.place_configure(y=imgheight+120)
        preview.config(state="normal")   

    def encode_fcn(self):
        f = fd.asksaveasfile(mode='w', defaultextension=".png")

        im = Image.open(base_img_filename)
        
        a = np.array(im)

        # popup progress bar code ######
        global general_progress_bar1, progressbar_popup, general_pb_label, progressbar_label

        progressbar_popup = tk.Toplevel(height=100, width=400)
        progressbar_label = tk.Label(progressbar_popup, text="Audio is being encoded")
        progressbar_label.place(x=150, y=25)
        
        general_progress_bar1 = ttk.Progressbar(progressbar_popup, orient="horizontal", length=350, mode='determinate')
        general_progress_bar1.place(x=25, y=50)

        general_pb_label = ttk.Label(progressbar_popup, text="0%")
        general_pb_label.place(x=150,y=75)

        progressbar_popup.update_idletasks()
        
        ###############################

        #audioclip = pydub.AudioSegment.from_mp3(audiofilename)
        #audioarray = np.array(audioclip.get_array_of_samples())
        #audioarray = audioarray + (2**16)/2
        #audioarray = np.rint((audioarray / 2**16) * 999)

        
        
        if encrypt_check.get() == 1:
            encrypt_audio()
            audioarray_to_encode = audio_array_output
            progressbar_label.config(text="Audio is being encoded")
            progressbar_popup.update_idletasks()
        elif encrypt_check.get() == 0:
            audioarray_to_encode = audioarray


        for x in range(len(a)):
            #print(x)
            for y in range(len(a[x])):
                for z in range(len(a[x][y])):
                    
                    if a[x][y][z] >= 250:
                        a[x][y][z] = 250
                        

                    a[x][y][z] = round(a[x][y][z]/10) * 10
                    
                    if x*len(a[x])+y < len(audioarray_to_encode):
                        digit = get_digit(audioarray_to_encode[x*len(a[x])+y], z)
                        if a[x][y][z] == 250 and digit > 5:
                            a[x][y][z] = 240
                        colourValue = int(a[x][y][z]) + int(digit)

                        if colourValue >= 256:
                            colourValue = 255

                        a[x][y][z] = colourValue

                    
                    #print(str(digit) + "  " + str(audioarray[x*len(a[x])+y]))
            
            general_progress_bar(x, len(a))
            progressbar_popup.update_idletasks()
            
        
                    

        #print(len(audioarray))

    

        im2 = Image.fromarray(a)
        #im2 . show()
        im2.save(str(f.name), format="png")   










def general_progress_bar(increment, total):
    general_progress_bar1["value"] = increment/total * 100
    general_pb_label["text"] = update_general_pb()
    progressbar_popup.update_idletasks()

def update_general_pb():
    return f"Current Progress: {round(general_progress_bar1['value'],1)}%"

""" def select_image_file():
    global base_img_filename
    global img
    global img1
    global base_img_width
    global base_img_height, base_w_scale, base_h_scale
    
    filetypes = (
        ("Image files", ("*.jpg", "*.png")),
        ("All files", "*.*")
    )

    base_img_filename = fd.askopenfilename(
        title = "Open a File",
        initialdir="/",
        filetypes=filetypes
    )

    if base_img_filename == "":
        return

    base_img_filename = "".join(base_img_filename)
    
    

    img = Image.open(base_img_filename)
    img1 = ImageTk.PhotoImage(img)

    open_img_filename.config(text=base_img_filename.split("/")[-1])

    base_img_width = img1.width()
    base_img_height = img1.height()

    

    if base_img_width > base_img_height:
        base_w_scale = 1
        base_h_scale = base_img_height / base_img_width
    elif base_img_height > base_img_width:
        base_h_scale = 1
        base_w_scale = base_img_width / base_img_height
    elif base_img_width == base_img_height:
        base_w_scale = 1
        base_h_scale = 1
    
    print(base_w_scale)
    print(base_h_scale)

    w = int(500 * base_w_scale)
    h = int(500 * base_h_scale)
    resize_img = img.resize((w, h))
    img = ImageTk.PhotoImage(resize_img)
    disp_inputimg.config(image=img)
    disp_inputimg.image = img


    baseImgdims.config(text = f'witdth: {base_img_width} height: {base_img_height}')
    baseImgdims.place_configure(y=500*base_h_scale+120)
    
    inputimgFrame.config(width=(500*base_w_scale+8), height=(500*base_h_scale+8))
    

    if base_img_filename == 1 or audio_filename == 1:
        preview.config(state="disabled")
        encode_button.config(state="disabled")
    elif base_img_filename != 1 and audio_filename == 1:
        decode_button.config(state="normal")
    else:
        preview.config(state="normal")
        encode_button.config(state="normal")
        decode_button.config(state="normal")

    
    return base_img_filename """

def select_encoded_image_file():
    global encoded_img_filename
    global encodedimg
    global encodedimg1
    global encoded_img_width, encoded_img_height, encoded_w_scale, encoded_h_scale

    filetypes = (
        ("Image files", ("*.jpg", "*.png")),
        ("All files", "*.*")
    )

    encoded_img_filename = fd.askopenfilename(
        title = "Open a File",
        initialdir="/",
        filetypes=filetypes
    )

    if encoded_img_filename == "":
        return

    encoded_img_filename = "".join(encoded_img_filename)
    


    encodedimg = Image.open(encoded_img_filename)
    encodedimg1 = ImageTk.PhotoImage(encodedimg)

    openencodedimgfilename.config(text=encoded_img_filename.split("/")[-1])

    encoded_img_width = encodedimg1.width()
    encoded_img_height = encodedimg1.height()

    

    if encoded_img_width > encoded_img_height:
        encoded_w_scale = 1
        encoded_h_scale = encoded_img_height / encoded_img_width
    elif encoded_img_height > encoded_img_width:
        encoded_h_scale = 1
        encoded_w_scale = encoded_img_width / encoded_img_height
    elif encoded_img_width == encoded_img_height:
        encoded_w_scale = 1
        encoded_h_scale = 1
    
    print(encoded_w_scale)
    print(encoded_h_scale)

    encodedw = int(500 * encoded_w_scale)
    encodedh = int(500 * encoded_h_scale)
    resize_img = encodedimg.resize((encodedw, encodedh))
    encodedimg = ImageTk.PhotoImage(resize_img)
    disp_encodedimg.config(image=encodedimg)
    disp_encodedimg.image = encodedimg


    baseImgdims.config(text = f'witdth: {base_img_width} height: {base_img_height}')
    baseImgdims.place_configure(y=500*base_h_scale+120)
    
    baseFrameencoded.config(width=(500*encoded_w_scale+8), height=(500*encoded_h_scale+8))

    
    return encoded_img_filename

""" def select_audio_file():
    global audio_filename
    global audioarray

    filetypes = (
        ("Audio files", ("*.mp3", "*.wav")),
        ("All files", "*.*")
    )

    audio_filename = fd.askopenfilename(
        title = "Open a File",
        initialdir="/",
        filetypes=filetypes
    )

    if audio_filename == "":
        return

    audio_filename = "".join(audio_filename)

    if base_img_filename == 1 or audio_filename == 1:
        preview.config(state="disabled")
        encode_button.config(state="disabled")
        decode_button.config(state="disabled")
    else:
        preview.config(state="normal")
        encode_button.config(state="normal")
        decode_button.config(state="normal")

    if audio_filename != 1:
        play_audio_button.config(state="normal")
        encrypt_audio_button.config(state="normal")
        decrypt_audio_button.config(state="normal")

    open_audio_filename.config(text=audio_filename.split("/")[-1])
    open_audio_filename_tab3.config(text=audio_filename.split("/")[-1])

    audioclip = pydub.AudioSegment.from_mp3(audio_filename)
    audioarray = np.array(audioclip.get_array_of_samples())
    
    

    open_audio_length.config(text=f"{math.floor(len(audioarray)/(48000*60))}m:{(len(audioarray) % (48000*60))/48000}s")

    plotaudio()

    return audio_filename """

""" def preview_encoded_image():
    preview.config(state="disabled")

    im = Image.open(base_img_filename)
          
    a = np.array(im)
    a[0][0][0] = 0

    #audioclip = pydub.AudioSegment.from_mp3(audiofilename)
    #audioarray = np.array(audioclip.get_array_of_samples())
    #audioarray = audioarray + (2**16)/2
    #audioarray = np.rint((audioarray / 2**16) * 999)

    progressbar_tab1["value"] = 0
    pb_tab1_value_label['text'] = "                                            "
    root.update_idletasks()
    
    for x in range(len(a)):
        if x < 500:
            #print(x)
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

            if len(a) < 500:
                progressbar_tab1["value"] += 1/len(a) * 100
                pb_tab1_value_label['text'] = update_progress_label()
                root.update_idletasks()
            else:
                progressbar_tab1["value"] += 1/500 * 100
                pb_tab1_value_label['text'] = update_progress_label()
                root.update_idletasks()


    

    img_preview_out = Image.fromarray(a)
    img_preview = ImageTk.PhotoImage(img_preview_out)

    imgwidth = img_preview.width()
    imgheight = img_preview.height()


    if imgwidth >= 500 and imgheight >= 500:
        img_preview_out = img_preview_out.crop((0,0,499,499))
    elif imgwidth < 500 and imgheight >= 500:
        img_preview_out = img_preview_out.crop((0,0,imgwidth-1,499))
    elif imgwidth >= 500 and imgheight < 500:
        img_preview_out = img_preview_out.crop((0,0,499,imgheight-1))
    if imgwidth < 500 and imgheight < 500:
        img_preview_out = img_preview_out.crop((0,0,imgwidth-1,imgheight-1))
        

    
    img_preview_out = ImageTk.PhotoImage(img_preview_out)

    if imgwidth < 500:
        outputFrame.config(width=(imgwidth+8))
    else:
        outputFrame.config(width=508)
    if imgheight < 500:
        outputFrame.config(height=(imgheight+8))
    else:
        outputFrame.config(height=508)

    disp_img2.config(image=img_preview_out)
    disp_img2.image = img_preview_out

    if imgheight > 500:
        imgheight = 500

    preview_img_label.place_configure(y=imgheight+120)
    preview.config(state="normal")   """ 

""" def encoding():
    #root.update_idletasks()
    f = fd.asksaveasfile(mode='w', defaultextension=".png")

    im = Image.open(base_img_filename)
     
    a = np.array(im)

    # popup progress bar code ######
    global general_progress_bar1, progressbar_popup, general_pb_label, progressbar_label

    progressbar_popup = tk.Toplevel(height=100, width=400)
    progressbar_label = tk.Label(progressbar_popup, text="Audio is being encoded")
    progressbar_label.place(x=150, y=25)
    
    general_progress_bar1 = ttk.Progressbar(progressbar_popup, orient="horizontal", length=350, mode='determinate')
    general_progress_bar1.place(x=25, y=50)

    general_pb_label = ttk.Label(progressbar_popup, text="0%")
    general_pb_label.place(x=150,y=75)

    progressbar_popup.update_idletasks()
    
    ###############################

    #audioclip = pydub.AudioSegment.from_mp3(audiofilename)
    #audioarray = np.array(audioclip.get_array_of_samples())
    #audioarray = audioarray + (2**16)/2
    #audioarray = np.rint((audioarray / 2**16) * 999)

     
    
    if encrypt_check.get() == 1:
        encrypt_audio()
        audioarray_to_encode = audio_array_output
        progressbar_label.config(text="Audio is being encoded")
        progressbar_popup.update_idletasks()
    elif encrypt_check.get() == 0:
        audioarray_to_encode = audioarray


    for x in range(len(a)):
        #print(x)
        for y in range(len(a[x])):
            for z in range(len(a[x][y])):
                
                if a[x][y][z] >= 250:
                    a[x][y][z] = 250
                    

                a[x][y][z] = round(a[x][y][z]/10) * 10
                
                if x*len(a[x])+y < len(audioarray_to_encode):
                    digit = get_digit(audioarray_to_encode[x*len(a[x])+y], z)
                    if a[x][y][z] == 250 and digit > 5:
                        a[x][y][z] = 240
                    colourValue = int(a[x][y][z]) + int(digit)

                    if colourValue >= 256:
                        colourValue = 255

                    a[x][y][z] = colourValue

                
                #print(str(digit) + "  " + str(audioarray[x*len(a[x])+y]))
        
        general_progress_bar(x, len(a))
        progressbar_popup.update_idletasks()
        
    
                

    #print(len(audioarray))

   

    im2 = Image.fromarray(a)
    #im2 . show()
    im2.save(str(f.name), format="png") """

def decoding():
    global base_img_filename
    img_decode = Image.open(base_img_filename)
    
    a = np.asarray(img_decode)

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

def update_progress_label():
    return f"Current Progress: {round(progressbar_tab1['value'],1)}%"

def update_pb2_label():
    return f"Current Progress: {round(pb2['value'],2)}%"



def encrypt_audio():
    #start = perf_counter()
    global audioarray
    global audio_array_output


    # popup progress bar code ######
    global general_progress_bar1, progressbar_popup, general_pb_label, progressbar_label

    if "progressbar_popup" in globals():
        pass
    else:
        progressbar_popup = tk.Toplevel(height=100, width=400)


    progressbar_label = tk.Label(progressbar_popup, text="Audio is being encrypted")
    progressbar_label.place(x=150, y=25)
    
    general_progress_bar1 = ttk.Progressbar(progressbar_popup, orient="horizontal", length=350, mode='determinate')
    general_progress_bar1.place(x=25, y=50)

    general_pb_label = ttk.Label(progressbar_popup, text="0%")
    general_pb_label.place(x=150,y=75)

    progressbar_popup.update_idletasks()
    
    ###############################
    

    
    audio_array_output = np.zeros(len(audioarray))
    

    percentofaudio = round(len(audio_array_output) * .001) 

    key = int(textBox.get(),16)


    if key.bit_length() < 64:
        key1 = str(bin(key))
        key1 = key1[2:]

        key1 += "1"

        while len(key1) < 64:
            key1 += "0"

        initializedKey = str(key1)
        intkey = int(key1,2)
    elif key.bit_length() == 64:
        intkey = key
    elif key.bit_length() > 64:
        messagebox.showerror('Program Error', 'Error: Key size is greater than 64 bits')
        return

    for x in range(len(audioarray)):
        audio_array_output[x] = encryptionmodule.encrypt(intkey, int(audioarray[x]), x)

        
        
        if x > 0:
            if x % percentofaudio == 0: 
                general_progress_bar(x, len(audioarray))
                progressbar_popup.update_idletasks()

        
    general_progress_bar(1, 1)
    progressbar_popup.update_idletasks()


    print(audioarray)

    
    #duration = perf_counter() - start
    #print('{} took {:.3f} seconds\n\n'.format("c++", duration))

    if "audio_array_output" in globals():
        playoutputaudiobutton.config(state="normal")
        Exportoutputaudiobutton.config(state="normal")
    
        
    #progressbar_popup.destroy()
    plotoutputaudio()
    return audio_array_output

def decrypt_audio():
    #start = perf_counter()
    global audioarray
    global audio_array_output

    pb2["value"] = 0
    pb2_label['text'] = "                                            "
    root.update_idletasks()

    #print("key:")
    #print(int(textBox.get(),16))
    
    audio_array_output = np.zeros(len(audioarray))
    

    percentofaudio = round(len(audio_array_output) * .001) 

    key = int(textBox.get(),16)

    if key.bit_length() < 64:
        key1 = str(bin(key))
        key1 = key1[2:]

        key1 += "1"

        while len(key1) < 64:
            key1 += "0"


        initializedKey = str(key1)

        intkey = int(key1,2)
    
    
    

    for x in range(len(audioarray)):
        audio_array_output[x] = encryptionmodule.decrypt(intkey, int(audioarray[x]), x)

        
        
        if x > 0:
            if x % percentofaudio == 0: 
                
                pb2["value"] += 0.1
                pb2_label['text'] = update_pb2_label()
                root.update_idletasks()


    pb2["value"] = 100
    pb2_label['text'] = update_pb2_label()
    root.update_idletasks()

    #duration = perf_counter() - start
    #print('{} took {:.3f} seconds\n\n'.format("c++", duration))

    if "audioarrayoutput" in globals():
        playoutputaudiobutton.config(state="normal")
        Exportoutputaudiobutton.config(state="normal")

    plotoutputaudio()
    return audio_array_output

def playaudio():
    audioarray_2channels = np.repeat(audioarray.reshape(len(audioarray), 1), 2, axis = 1)
    audioarray_2channels = audioarray_2channels.astype("int16")
    audiotoplay = pygame.sndarray.make_sound(audioarray_2channels)
    audiotoplay.play(loops=0)

def playoutputaudio():
    audioarray_2channels = np.repeat(audio_array_output.reshape(len(audio_array_output), 1), 2, axis = 1)
    audioarray_2channels = audioarray_2channels.astype("int16")
    audiotoplay = pygame.sndarray.make_sound(audioarray_2channels)
    audiotoplay.play(loops=0)

def stopaudio():
    pygame.mixer.stop()

def plotaudio():
    # the figure that will contain the plot
    fig = Figure(figsize = (12, 3), dpi = 100)

    fig.clear()
  
    
    Time = np.linspace(0, len(audioarray) / 48000, num=len(audioarray))
  
    # plotting the graph
    plot1 = fig.add_subplot(111)
  
    audioplt = plot1.plot(Time, audioarray)
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = tab3)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=173, y = 55)
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, tab3)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    toolbar.place(x=173, y = 355)

def plotoutputaudio():
    global audio_array_output
    
  
    # the figure that will contain the plot
    fig2 = Figure(figsize = (12, 3), dpi = 100)

    fig2.clear()
  
    # list of squares
    #y = audioarray
    
    # adding the subplot
    #plot1 = fig.add_subplot(111)

    Time = np.linspace(0, len(audioarray) / 48000, num=len(audioarray))
  
    # plotting the graph
    plot2 = fig2.add_subplot(111)
  
    audioplt = plot2.plot(Time, audio_array_output)
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig2, master = tab3)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=173, y = 405)
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, tab3)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    toolbar.place(x=173, y = 705)

def Exportaudio():
    export_audio_filename = fd.asksaveasfile(mode='w', defaultextension=".wav")
    y = np.int16(audio_array_output)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=48000, sample_width=2, channels=1)
    song.export(str(export_audio_filename.name), format="wav", bitrate="48k") 
    print(str(export_audio_filename.name))



# Progress bar window ###############################################




# Tab 1 ##############################################################
""" open_img_button = tk.Button(
    tab1,
    text='Open an image file',
    height = 2, 
    width=20,
    command=select_image_file
)
open_img_button.place(x=0, y=5) """

""" open_audio_button = tk.Button(
    tab1,
    text='Open an audio file',
    height = 2, 
    width=20,
    command=select_audio_file
)
open_audio_button.place(x=0, y=55) """

""" preview = tk.Button(
    tab1,
    text='Preview',
    height = 2, 
    width=20,
    command=preview_encoded_image
)
preview.place(x=0, y=105)

encode_button = tk.Button(
    tab1,
    text='Encode',
    height = 2, 
    width=20,
    command=encoding
)
encode_button.place(x=0, y=155) """

baseImgdims = tk.Label(
    tab1,
    text=f'width: {base_img_width} height: {base_img_height}', 
    bd=2, 
    relief="sunken"
)
baseImgdims.place(x=173, y=620)

open_img_filename = tk.Label(
    tab1,
    text="None Selected", 
    bd=2, 
    relief="sunken"
)  
open_img_filename.place(x=173, y=15)

open_audio_filename = tk.Label(
    tab1,
    text="None Selected", 
    bd=2, 
    relief="sunken"
)  
open_audio_filename.place(x=173, y=65)

inputimgFrame = tk.Frame(
    tab1,
    width=(500*base_w_scale+8), 
    height=(500*base_h_scale+8), 
    bd=2, 
    relief="sunken"
)
inputimgFrame.place(x=173, y=105)

disp_inputimg = tk.Label(tab1)
disp_inputimg.place(x=175, y=107)

outputFrame = tk.Frame(
    tab1, 
    width=(508), 
    height=(508), 
    bd=2, 
    relief="sunken"
)
outputFrame.place(x=773, y=105)

preview_img_label = tk.Label(
    tab1,
    text="1:1 scale", 
    bd=2, 
    relief="sunken"
)  
preview_img_label.place(x=773, y=620)

checkbox_excrypt = tk.Checkbutton(tab1, text = "Encrypt Audio with Key", variable=encrypt_check)
checkbox_excrypt.place(x=0, y=350)



pb2_label = ttk.Label(tab1, text="64 Bit Encryption Key:")
pb2_label.place(x=0,y=380)

inputtextkey_tab1 = tk.Entry(tab1, width=24, bd=2)
inputtextkey_tab1.place(x=0, y=405)

textBox_tab1 = tk.Entry(tab1, width=24, bd=2)
textBox_tab1.insert(0, "abc123")
textBox_tab1.place(x=0, y=405)


disp_img2 = tk.Label(tab1)
disp_img2.place(x=775, y=107)

progressbar_tab1 = ttk.Progressbar(tab1, orient="horizontal", length=150, mode='determinate')
progressbar_tab1.place(x=0,y=205)

pb_tab1_value_label = ttk.Label(tab1, text=update_progress_label())
pb_tab1_value_label.place(x=0,y=235)



# Tab 2 ##############################################################
open_encoded_img_button = tk.Button(
    tab2,
    text='Open an image file',
    height = 2, 
    width=20,
    command=select_encoded_image_file
)
open_encoded_img_button.place(x=0, y=5)

decode_button = tk.Button(
    tab2,
    text='Decode',
    height = 2, 
    width=20,
    command=decoding
)


openencodedimgfilename = tk.Label(
    tab2,
    text="None Selected", 
    bd=2, 
    relief="sunken"
)  
openencodedimgfilename.place(x=173, y=15)


baseFrameencoded = tk.Frame(
    tab2, 
    width=(500*base_w_scale+8), 
    height=(500*base_h_scale+8), 
    bd=2, 
    relief="sunken"
)

disp_encodedimg = tk.Label(tab2)
disp_encodedimg.place(x=175, y=107)

#LOD_slider = Scale(tab1, from_=0, to=10, orient=HORIZONTAL)

baseFrameencoded.place(x=173, y=105)



decode_button.place(x=0, y=55)

pb2_label = ttk.Label(tab2, text="64 Bit Encryption Key:")
pb2_label.place(x=0,y=380)

inputtextkey = tk.Entry(tab2, width=24, bd=2)
inputtextkey.place(x=0, y=405)

textBox = tk.Entry(tab2, width=24, bd=2)
textBox.insert(0, "abc123")
textBox.place(x=0, y=405)






# Tab 3 ##############################################################
""" open_audio_button2 = tk.Button(
    tab3,
    text='Open an audio file',
    height = 2, 
    width=20,
    command=open_encoded_img_button.self.open_audio_file_fcn
)
open_audio_button2.place(x=0, y=5) """

open_audio_filename_tab3 = tk.Label(
    tab3,
    text="None Selected", 
    bd=2, 
    relief="sunken"
)  
open_audio_filename_tab3.place(x=173, y=5)

open_audio_length = tk.Label(
    tab3,
    text="00m:00.00s", 
    bd=2, 
    relief="sunken"
)  
open_audio_length.place(x=173, y=25)

play_audio_button = tk.Button(
    tab3,
    text='Play audio',
    height = 2, 
    width=20,
    command=playaudio
)
play_audio_button.place(x=0, y=55)

playoutputaudiobutton = tk.Button(
    tab3,
    text='Play output audio',
    height = 2, 
    width=20,
    command=playoutputaudio
)
playoutputaudiobutton.place(x=0, y=105)

stopaudiobutton = tk.Button(
    tab3,
    text='Stop audio',
    height = 2, 
    width=20,
    command=stopaudio
)
stopaudiobutton.place(x=0, y=155)

encrypt_audio_button = tk.Button(
    tab3,
    text='Encrypt audio',
    height = 2, 
    width=20,
    command=encrypt_audio
)
encrypt_audio_button.place(x=0, y=225)

decrypt_audio_button = tk.Button(
    tab3,
    text='Decrypt audio',
    height = 2, 
    width=20,
    command=decrypt_audio
)
decrypt_audio_button.place(x=0, y=275)

Exportoutputaudiobutton = tk.Button(
    tab3,
    text='Export audio',
    height = 2, 
    width=20,
    command=Exportaudio
)
Exportoutputaudiobutton.place(x=0, y=325)

pb2_label = ttk.Label(tab3, text="64 Bit Encryption Key:")
pb2_label.place(x=0,y=380)

inputtextkey = tk.Entry(tab3, width=24, bd=2)
inputtextkey.place(x=0, y=405)

textBox = tk.Entry(tab3, width=24, bd=2)
textBox.insert(0, "abc123")
textBox.place(x=0, y=405)

pb2 = ttk.Progressbar(tab3, orient="horizontal", length=150, mode='determinate')
pb2.place(x=0,y=435)

pb2_label = ttk.Label(tab3, text=update_pb2_label())
pb2_label.place(x=0,y=465)


if base_img_filename == 1 or audio_filename == 1:
    preview.config(state="disabled")
    encode_button.config(state="disabled")
    decode_button.config(state="disabled")

if audio_filename == 1:
    play_audio_button.config(state="disabled")
    encrypt_audio_button.config(state="disabled")
    decrypt_audio_button.config(state="disabled")
    

if "audioarrayoutput" in globals():
    pass
else:
    playoutputaudiobutton.config(state="disabled")
    Exportoutputaudiobutton.config(state="disabled")

# run the application
testingclass1 = tab1_class(tab1)
root.mainloop()
