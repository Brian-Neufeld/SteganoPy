import numpy as np
import PIL
from PIL import ImageTk,Image 
import tkinter as tk
from tkinter import HORIZONTAL, Menu, StringVar, filedialog as fd
from tkinter import ttk, font
from tkinter.messagebox import showinfo
import time
import math
import pydub
from pydub.playback import play
import encryptionmodule
from time import perf_counter
import scipy
import pygame
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from tkinter import messagebox
import threading

matplotlib.rcParams['agg.path.chunksize'] = 10000

pygame.mixer.init(frequency=48000, size=-16, channels=2, allowedchanges=0)

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

audio_array = 1
audio_array_output = 1
audio_array_to_encode = 1

encrypt_check = tk.IntVar()
remove_silence_check = tk.IntVar()

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


class GUI:
    
    def __init__(self, master):
        global open_audio_file_btn, open_audio_file_btn, open_img_filename, open_audio_filename_tab1, open_audio_length_tab1, preview_btn, encode_btn, open_audio_length_tab3
        global baseImgdims, disp_inputimg, inputimgFrame, outputFrame, disp_img2, preview_img_label

        global open_audio_filename_tab3, openencodedimgfilename, disp_encodedimg, baseFrameencoded, textBox, playoutputaudiobutton, Exportoutputaudiobutton

        self.IsPaused = False
        self.current_audio = "Input"

        

        # Tab1 gui #####################################################
        open_img_file_btn = tk.Button(tab1, text="Open image file", height = 2, command=self.open_img_file_fn)
        open_img_file_btn.place(x=0, y=0, width=150)

        open_audio_file_btn = tk.Button(tab1, text='Open audio file', height = 2, command=self.open_audio_file_fn)
        open_audio_file_btn.place(x=0, y=55, width=150)

        open_img_filename = tk.Label(tab1,text="None Selected", bd=2, relief="sunken")  
        open_img_filename.place(x=173, y=15)

        open_audio_filename_tab1 = tk.Label(tab1, text="None Selected", bd=2,  relief="sunken")  
        open_audio_filename_tab1.place(x=173, y=55)

        open_audio_length_tab1 = tk.Label(tab1, text="00m:00.00s", bd=2, relief="sunken")  
        open_audio_length_tab1.place(x=173, y=75)

        preview_btn = tk.Button(tab1, text='Preview', height = 2, command=self.preview_threading_fn)
        preview_btn.place(x=0, y=105, width=150)

        encode_btn = tk.Button(tab1, text='Encode', height = 2, command=self.encode_threading_fn)
        encode_btn.place(x=0, y=155, width=150)

        additional_features = tk.Label(tab1, text="Additional Features:", font= ('TkDefaultFont 9 bold underline'))
        additional_features.place(x=0, y=210)

        additional_features_frame = tk.Frame(tab1, width=165, height=400, bd=2, relief="sunken")
        additional_features_frame.place(x=0, y=235)

        encoding_options_label = tk.Label(additional_features_frame, text="Encoding Method:", font= ('TkDefaultFont 9 bold underline'))
        encoding_options_label.place(x=0, y=0)

        encoding_options = ("16 Bit Mono", "8 Bit Mono", "16 Bit Stereo", "8 Bit Stereo")
        self.encoding_type = StringVar(root)
        self.encoding_type.set("16 Bit Mono")
        
        encoding_options_menu = tk.OptionMenu(additional_features_frame, self.encoding_type, *encoding_options, command=donothing)
        encoding_options_menu.config(justify="left")
        encoding_options_menu.place(x=0, y=20, width=160, height=25)

        encoding_options_label = tk.Label(additional_features_frame, text="Encryption:", font= ('TkDefaultFont 9 bold underline'))
        encoding_options_label.place(x=0, y=50)

        checkbox_excrypt = tk.Checkbutton(additional_features_frame, text = "Encrypt Audio with Key", variable=encrypt_check)
        checkbox_excrypt.place(x=0, y=75)

        key_entry_label = ttk.Label(additional_features_frame, text="64 Bit Encryption Key:")
        key_entry_label.place(x=0,y=100)

        inputtextkey_tab1 = tk.Entry(additional_features_frame, bd=2)
        inputtextkey_tab1.place(x=2, y=125, width=156)

        textBox_tab1 = tk.Entry(additional_features_frame, bd=2)
        textBox_tab1.insert(0, "abc123")
        textBox_tab1.place(x=2, y=125, width=156)

        encoding_options_label = tk.Label(additional_features_frame, text="Remove Silence:", font= ('TkDefaultFont 9 bold underline'))
        encoding_options_label.place(x=0, y=150)

        checkbox_remove_silence = tk.Checkbutton(additional_features_frame, text = "Remove Silence", variable=remove_silence_check)
        checkbox_remove_silence.place(x=0, y=175)

        dB_label = tk.Label(additional_features_frame, text="dB cutoff")
        dB_label.place(x=105, y=220)

        silence_dB_level = tk.Scale(additional_features_frame, from_=-60 , to=-0, orient=HORIZONTAL)
        silence_dB_level.place(x=0, y=200)

        baseImgdims = tk.Label(tab1,text=f'width: {base_img_width} height: {base_img_height}', bd=2, relief="sunken")
        baseImgdims.place(x=173, y=385)

        inputimgFrame = tk.Frame(tab1, width=(500*base_w_scale+8), height=(500*base_h_scale+8), bd=2, relief="sunken")
        inputimgFrame.place(x=173, y=105)

        disp_inputimg = tk.Label(tab1)
        disp_inputimg.place(x=175, y=107)

        outputFrame = tk.Frame(tab1, width=(508), height=(508), bd=2, relief="sunken")
        outputFrame.place(x=773, y=105)

        preview_img_label = tk.Label(tab1, text="1:1 scale", bd=2, relief="sunken")  
        preview_img_label.place(x=773, y=620)

        

        disp_img2 = tk.Label(tab1)
        disp_img2.place(x=775, y=107)



        # Tab2 gui ######################################
        open_encoded_img_button = tk.Button(tab2, text='Open an image file', height = 2, width=20, command=self.open_encoded_img_fn)
        open_encoded_img_button.place(x=0, y=5)

        decode_button = tk.Button(tab2, text='Decode', height = 2, width=20, command=decode_fn)
        decode_button.place(x=0, y=55)

        openencodedimgfilename = tk.Label(tab2, text="None Selected", bd=2, relief="sunken")  
        openencodedimgfilename.place(x=173, y=15)

        baseFrameencoded = tk.Frame(tab2, width=(500*base_w_scale+8), height=(500*base_h_scale+8), bd=2, relief="sunken")

        disp_encodedimg = tk.Label(tab2)
        disp_encodedimg.place(x=175, y=107)

        baseFrameencoded.place(x=173, y=105)

        decode_button.place(x=0, y=55)

        key_entry_label = ttk.Label(tab2, text="64 Bit Encryption Key:")
        key_entry_label.place(x=0,y=380)

        inputtextkey = tk.Entry(tab2, width=24, bd=2)
        inputtextkey.place(x=0, y=405)

        textBox = tk.Entry(tab2, width=24, bd=2)
        textBox.insert(0, "abc123")
        textBox.place(x=0, y=405)



        # Tab3 gui ########################################
        open_audio_file_tab3_btn = tk.Button(tab3, text="Open audio file", height=2, width=20, command=self.open_audio_file_fn)
        open_audio_file_tab3_btn.place(x=0, y=5)

        open_audio_filename_tab3 = tk.Label(tab3, text="None Selected", bd=2, relief="sunken")  
        open_audio_filename_tab3.place(x=173, y=5)

        open_audio_length_tab3 = tk.Label(tab3, text="00m:00.00s", bd=2, relief="sunken")  
        open_audio_length_tab3.place(x=173, y=25)

        play_audio_button = tk.Button(tab3, text='Play/pause', height = 2, width=20, command=self.play_pause_audio)
        play_audio_button.place(x=0, y=55)

        playoutputaudiobutton = tk.Button(tab3, text='Play/pause encrypted', height = 2, width=20, command=self.playoutputaudio)
        playoutputaudiobutton.place(x=0, y=105)

        stopaudiobutton = tk.Button(tab3, text='Stop audio', height = 2, width=20, command=self.stop_audio)
        stopaudiobutton.place(x=0, y=155)

        encrypt_audio_button = tk.Button(tab3, text='Encrypt audio', height = 2, width=20, command=encrypt_audio)
        encrypt_audio_button.place(x=0, y=225)

        decrypt_audio_button = tk.Button(tab3, text='Decrypt audio', height = 2, width=20, command=decrypt_audio)
        decrypt_audio_button.place(x=0, y=275)

        Exportoutputaudiobutton = tk.Button(tab3, text='Export audio', height = 2, width=20, command=self.Exportaudio)
        Exportoutputaudiobutton.place(x=0, y=325)

        key_entry_label = ttk.Label(tab3, text="64 Bit Encryption Key:")
        key_entry_label.place(x=0,y=380)

        inputtextkey = tk.Entry(tab3, width=24, bd=2)
        inputtextkey.place(x=0, y=405)

        textBox = tk.Entry(tab3, width=24, bd=2)
        textBox.insert(0, "abc123")
        textBox.place(x=0, y=405)


        plot_options = ("Input audio waveform", "Input audio spectrogram", "Output audio waveform", "Output audio spectrogram")
        self.audio_plot_type = StringVar(root)
        self.audio_plot_type.set("Input audio waveform")
        self.current_plot_type = "Input audio waveform"
        
        plot_menu = tk.OptionMenu(tab3, self.audio_plot_type, *plot_options, command=self.change_plot1)
        plot_menu.place(x=173, y=395)

        plot2_options = ("Input audio waveform", "Input audio spectrogram", "Output audio waveform", "Output audio spectrogram")
        self.audio_plot2_type = StringVar(root)
        self.audio_plot2_type.set("Output audio waveform")
        self.current_plot2_type = "Output audio waveform"
        
        plot2_menu = tk.OptionMenu(tab3, self.audio_plot2_type, *plot2_options, command=self.change_plot2)
        plot2_menu.place(x=173, y=775)


    def open_img_file_fn(self):

        global audioarray
        global base_img_filename, audio_filename
        
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
        
        #print(base_w_scale)
        #print(base_h_scale)

        w = int(500 * base_w_scale)
        h = int(500 * base_h_scale)
        resize_img = img.resize((w, h))
        img = ImageTk.PhotoImage(resize_img)
        disp_inputimg.config(image=img)
        disp_inputimg.image = img


        baseImgdims.config(text = f'witdth: {base_img_width} height: {base_img_height}')
        baseImgdims.place_configure(y=500*base_h_scale+120)
        
        inputimgFrame.config(width=(500*base_w_scale+8), height=(500*base_h_scale+8))
        
        self.audio_plot1(str(self.audio_plot_type.get()))

        #print(base_img_filename)
        return base_img_filename

    def open_audio_file_fn(self):
        global audio_array, audioclip
        global base_img_filename, audio_filename

        filetypes = (
            ("Audio files", ("*.mp3", "*.wav", "*.flac")),
            ("MP3", "*.mp3"),
            ("WAV", "*.wav"),
            ("FLAC", "*.flac"),
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

        open_audio_filename_tab1.config(text=audio_filename.split("/"[-1]))
        open_audio_filename_tab3.config(text=audio_filename.split("/")[-1])

        audioclip = pydub.AudioSegment.from_file(audio_filename)   #, format="wav")
        audio_array = np.array(audioclip.get_array_of_samples())
        
        sample_rate = audioclip.frame_rate
        number_of_channels = audioclip.channels

        # displays the length of selected audio clip as 00m:00.00s
        if number_of_channels == 1:
            open_audio_length_tab1.config(text=f"{math.floor(len(audio_array)/(sample_rate*60))}m:{round((len(audio_array) % (sample_rate*60))/sample_rate, 2)}s")
            open_audio_length_tab3.config(text=f"{math.floor(len(audio_array)/(sample_rate*60))}m:{round((len(audio_array) % (sample_rate*60))/sample_rate, 2)}s")
        elif number_of_channels == 2:
            open_audio_length_tab1.config(text=f"{math.floor((len(audio_array)/2)/(sample_rate*60))}m:{round(((len(audio_array)/2) % (sample_rate*60))/sample_rate, 2)}s")
            open_audio_length_tab3.config(text=f"{math.floor((len(audio_array)/2)/(sample_rate*60))}m:{round(((len(audio_array)/2) % (sample_rate*60))/sample_rate, 2)}s")


        self.audio_plot1(self.audio_plot_type.get())
        self.audio_plot2(self.audio_plot2_type.get())

        return audio_filename

    def preview_threading_fn(self):
        threading.Thread(target=preview_fn).start()

    def encode_threading_fn(self):
        threading.Thread(target=encode_fn).start()

    def open_encoded_img_fn(self):
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

    def play_pause_audio(self): 
        if type(audio_array).__name__ == "int":
            messagebox.showerror('Program Error', 'Error: No audio file seleted')
            return

        if self.current_audio == "Output":
            pygame.mixer.stop()
            self.current_audio = "Input"
        

        if pygame.mixer.get_busy() == False: 
            if audioclip.channels == 1:
                audioarray_2channels = np.repeat(audio_array.reshape(len(audio_array), 1), 2, axis = 1)
                audioarray_2channels = audioarray_2channels.astype("int16")

                print(audioarray_2channels)
                print(audio_array)
            elif audioclip.channels == 2:
                audioarray_2channels = np.vstack((audio_array[::2], audio_array[1::2])).T
                audioarray_2channels = np.ascontiguousarray(audioarray_2channels, dtype=np.int16)

                print(audioarray_2channels)

            audiotoplay = pygame.sndarray.make_sound(audioarray_2channels)
            audiotoplay.play(loops=0)
        elif pygame.mixer.get_busy() == True and self.IsPaused == False:
            pygame.mixer.pause()
            self.IsPaused = True
        elif pygame.mixer.get_busy() == True and self.IsPaused == True:
            pygame.mixer.unpause()
            self.IsPaused = False     

    def playoutputaudio(self):
        if type(audio_array_output).__name__ == "int":
            messagebox.showerror('Program Error', 'Error: No encrypted audio avalible')
            return

        if self.current_audio == "Input":
            pygame.mixer.stop()
            self.current_audio = "Output"

        if pygame.mixer.get_busy() == False: 
            audioarray_2channels = np.repeat(audio_array_output.reshape(len(audio_array_output), 1), 2, axis = 1)
            audioarray_2channels = audioarray_2channels.astype("int16")
            audiotoplay = pygame.sndarray.make_sound(audioarray_2channels)
            audiotoplay.play(loops=0)
        elif pygame.mixer.get_busy() == True and self.IsPaused == False:
            pygame.mixer.pause()
            self.IsPaused = True
        elif pygame.mixer.get_busy() == True and self.IsPaused == True:
            pygame.mixer.unpause()
            self.IsPaused = False    

    def stop_audio(self):
        pygame.mixer.stop()

    def Exportaudio(self):
        export_audio_filename = fd.asksaveasfile(mode='w', defaultextension=".wav")
        y = np.int16(audio_array_output)
        song = pydub.AudioSegment(y.tobytes(), frame_rate=48000, sample_width=2, channels=1)
        song.export(str(export_audio_filename.name), format="wav", bitrate="48k") 
        print(str(export_audio_filename.name))

    def change_plot1(self, *args):
        if self.current_plot_type == self.audio_plot_type.get():
            return
        else:
            self.current_plot_type = self.audio_plot_type.get()
            self.audio_plot1(str(self.current_plot_type))

    def change_plot2(self, *args):
        if self.current_plot2_type == self.audio_plot2_type.get():
            return
        else:
            self.current_plot2_type = self.audio_plot2_type.get()
            self.audio_plot2(str(self.current_plot2_type))
        
    def audio_plot1(self, format):
        #global audio_array_output, audioclip

        if format == "Input audio waveform": 
            if type(audio_array).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_to_plot = audio_array[::2]
                else:
                    audio_array_to_plot = audio_array

            # the figure that will contain the plot
            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_to_plot) / 48000, num=len(audio_array_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.plot(Time, audio_array_to_plot)

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

        elif format == "Input audio spectrogram":
            if type(audio_array).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_to_plot = audio_array[::2]
                else:
                    audio_array_to_plot = audio_array

            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_to_plot) / 48000, num=len(audio_array_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.specgram(audio_array_to_plot, Fs=48000)

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

        elif format == "Output audio waveform":
            if type(audio_array_output).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_output_to_plot = audio_array_output[::2]
                else:
                    audio_array_output_to_plot = audio_array_output

            # the figure that will contain the plot
            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_output_to_plot) / 48000, num=len(audio_array_output_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.plot(Time, audio_array_output_to_plot)

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

        elif format == "Output audio spectrogram":
            if type(audio_array_output).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_output_to_plot = audio_array_output[::2]
                else:
                    audio_array_output_to_plot = audio_array_output

            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_output_to_plot) / 48000, num=len(audio_array_output_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.specgram(audio_array_output_to_plot, Fs=48000)

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

    def audio_plot2(self, format):
        #global audio_array_output, audioclip

        if format == "Input audio waveform": 
            if type(audio_array).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_to_plot = audio_array[::2]
                else:
                    audio_array_to_plot = audio_array

            # the figure that will contain the plot
            fig2 = Figure(figsize = (12, 3), dpi = 100)

            fig2.clear()

            
            Time = np.linspace(0, len(audio_array_to_plot) / 48000, num=len(audio_array_to_plot))

            # plotting the graph
            plot2 = fig2.add_subplot(111)

            audioplt = plot2.plot(Time, audio_array_to_plot)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig2, master = tab3)  
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(x=173, y = 435)

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, tab3)
            toolbar.update()

            # placing the toolbar on the Tkinter window
            toolbar.place(x=173, y = 735) 

        elif format == "Input audio spectrogram":
            if type(audio_array).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_to_plot = audio_array[::2]
                else:
                    audio_array_to_plot = audio_array

            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_to_plot) / 48000, num=len(audio_array_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.specgram(audio_array_to_plot, Fs=48000)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master = tab3)  
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(x=173, y = 435)

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, tab3)
            toolbar.update()

            # placing the toolbar on the Tkinter window
            toolbar.place(x=173, y = 735) 

        elif format == "Output audio waveform": 
            if type(audio_array_output).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_output_to_plot = audio_array_output[::2]
                else:
                    audio_array_output_to_plot = audio_array_output

            # the figure that will contain the plot
            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_output_to_plot) / 48000, num=len(audio_array_output_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.plot(Time, audio_array_output_to_plot)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master = tab3)  
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(x=173, y = 435)

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, tab3)
            toolbar.update()

            # placing the toolbar on the Tkinter window
            toolbar.place(x=173, y = 735) 

        elif format == "Output audio spectrogram":
            if type(audio_array_output).__name__ == "int":
                return
            else:
                if audioclip.channels == 2:
                    audio_array_output_to_plot = audio_array_output[::2]
                else:
                    audio_array_output_to_plot = audio_array_output

            fig = Figure(figsize = (12, 3), dpi = 100)

            fig.clear()

            
            Time = np.linspace(0, len(audio_array_output_to_plot) / 48000, num=len(audio_array_output_to_plot))

            # plotting the graph
            plot1 = fig.add_subplot(111)

            audioplt = plot1.specgram(audio_array_output_to_plot, Fs=48000)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master = tab3)  
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(x=173, y = 435)

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, tab3)
            toolbar.update()

            # placing the toolbar on the Tkinter window
            toolbar.place(x=173, y = 735) 
        


def preview_fn():
    global audioarray
    global base_img_filename, audio_filename

    #print(base_img_filename)

    if base_img_filename == 1:
        messagebox.showerror('Program Error', 'Error: No image file seleted')
        return
    elif audio_filename == 1:
        messagebox.showerror('Program Error', 'Error: No audio file seleted')
        return


    #preview_btn.config(state="disabled")

    im = Image.open(base_img_filename)
        
    a = np.array(im)
    a[0][0][0] = 0


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

    if encrypt_check.get() == 1:
        encrypt_audio()
        audioarray_to_encode = audio_array_output
        progressbar_label.config(text="Audio is being encoded")
        progressbar_popup.update_idletasks()
    elif encrypt_check.get() == 0:
        audioarray_to_encode = audioarray

    
    
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
                general_progress_bar(x, 500)
                progressbar_popup.update_idletasks()
            else:
                general_progress_bar(x, len(a))
                progressbar_popup.update_idletasks()


        general_progress_bar(x, len(a))
        progressbar_popup.update_idletasks()

    

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
    preview_btn.config(state="normal")   

    general_progress_bar(1, 1)
    progressbar_popup.update_idletasks()
                
    progressbar_popup.destroy()

def encode_fn():
    global audio_array_to_encode
    global base_img_filename, audio_filename


    # image file to save to
    filetypes = (
        ("Image files", ("*.jpg", "*.png")),
        ("All files", "*.*")
        )

    
    img_save_name = base_img_filename.split("/")[-1].split(".")[0]

    f = fd.asksaveasfile(mode='w', filetypes = filetypes, defaultextension = filetypes, initialfile=f"{img_save_name} encoded")

    print(f)
    print(f.name)
    print("")

    if f == "" or f == None:
        return

    im = Image.open(base_img_filename)
    image_array = np.array(im)

    
    # get audio as array
    if gui_class.encoding_type.get() == "16 Bit Stereo" or gui_class.encoding_type.get() == "8 Bit Stereo":
        audioclip = pydub.AudioSegment.from_file(audio_filename, format="wav", channels=2)
        audio_array_to_encode = np.array(audioclip.get_array_of_samples(), dtype=np.int16)
    elif gui_class.encoding_type.get() == "16 Bit Mono" or gui_class.encoding_type.get() == "8 Bit Mono":
        audioclip = pydub.AudioSegment.from_file(audio_filename, format="wav", channels=1)
        audio_array_to_encode = np.array(audioclip.get_array_of_samples(), dtype=np.int16)

    

    # popup progress bar code #####################################
    global general_progress_bar1, progressbar_popup, general_pb_label, progressbar_label

    progressbar_popup = tk.Toplevel(height=100, width=400)
    progressbar_label = tk.Label(progressbar_popup, text="Audio is being encoded")
    progressbar_label.place(x=150, y=25)
    
    general_progress_bar1 = ttk.Progressbar(progressbar_popup, orient="horizontal", length=350, mode='determinate')
    general_progress_bar1.place(x=25, y=50)

    general_pb_label = ttk.Label(progressbar_popup, text="0%")
    general_pb_label.place(x=150,y=75)

    progressbar_popup.update_idletasks()
    
    ##############################################################

    # removes silence from audio
    if remove_silence_check.get() == 1:
        audio_array_to_encode = remove_silence(audio_array_to_encode)
        progressbar_label.config(text="Audio is being encoded")
        progressbar_popup.update_idletasks()
        
    # encrypts audio with key
    if encrypt_check.get() == 1:
        audio_array_to_encode = encrypt_audio(audio_array_to_encode)
        progressbar_label.config(text="Audio is being encoded")
        progressbar_popup.update_idletasks()

    elif encrypt_check.get() == 0:
        pass

        

    audio_index = 0
    audio_array_to_encode = audio_array_to_encode + ((2**16)/2)
    audio_array_to_encode = audio_array_to_encode.astype(int)
    
    for x in range(len(image_array)):
        for y in range(len(image_array[x])):
            for z in range(len(image_array[x][y])):
                if audio_index < len(audio_array_to_encode):
                    image_array[x][y][z] = round(image_array[x][y][z]/10)*10

                    if image_array[x][y][z] >= 250:
                        image_array[x][y][z] = 250

                    if (x*len(image_array[x])+y) % 2 == 0:
                        if len(str(audio_array_to_encode[audio_index])) < 6-z:
                            image_array[x][y][z] += 0
                        else:
                            image_array[x][y][z] += int(str(audio_array_to_encode[audio_index])[-6+z])

                    if (x*len(image_array[x])+y) % 2 == 1:
                        if len(str(audio_array_to_encode[audio_index])) < 3-z:
                            image_array[x][y][z] += 0
                        else:
                            image_array[x][y][z] += int(str(audio_array_to_encode[audio_index])[-3+z])

                        if z == 2 and (x*len(image_array[x])+y) % 2 == 1:
                            audio_index += 1

                    if image_array[x][y][z] >= 255:
                        image_array[x][y][z] -= 10


        general_progress_bar(x, len(image_array))
        progressbar_popup.update_idletasks()
            
    general_progress_bar(1, 1)
    progressbar_popup.update_idletasks()



    img_preview_out = Image.fromarray(image_array)
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
                


    progressbar_popup.destroy()
    

    im2 = Image.fromarray(image_array)
    im2.save(str(f.name)) #, format="png")   

def decode_fn():
    global base_img_filename
    img_decode = Image.open(base_img_filename)
    
    a = np.asarray(img_decode)
    audioarray = np.zeros(int(len(a)*len(a[0])/2))

    audio_index = 0

    for x in range(len(a)):
        for y in range(len(a[x])):
            if (x*len(a[x])+y) % 2 == 0:
                audioarray[audio_index] = get_digit(a[x][y][0], 0)*100000 + get_digit(a[x][y][1], 0)*10000 + get_digit(a[x][y][2], 0)*1000
            
            elif (x*len(a[x])+y) % 2 == 1:
                audioarray[audio_index] += get_digit(a[x][y][0], 0)*100 + get_digit(a[x][y][1], 0)*10 + get_digit(a[x][y][2], 0)*1
                audio_index += 1
    
    audio_out = audioarray - ((2**16)/2)

    audio_out = decrypt_audio(audio_out)

    audio_out = add_silence(audio_out)

    y = np.int16(audio_out)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=48000, sample_width=2, channels=1)
    song.export("decoded audio.mp3", format="mp3", bitrate="48k")

def encrypt_audio(audio_array_to_encode):
    global audio_array_output

    pygame.mixer.stop()

    # popup progress bar code #####################################
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
    
    ##############################################################
    

    
    audio_array_output = np.zeros(len(audio_array_to_encode))
    

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

    for x in range(len(audio_array_to_encode)):
        audio_array_output[x] = encryptionmodule.encrypt(intkey, int(audio_array_to_encode[x]), x)

        
        
        if x > 0:
            if x % percentofaudio == 0: 
                general_progress_bar(x, len(audio_array_to_encode))
                progressbar_popup.update_idletasks()

        
    general_progress_bar(1, 1)
    progressbar_popup.update_idletasks()


    #print(audioarray)

    
    #duration = perf_counter() - start
    #print('{} took {:.3f} seconds\n\n'.format("c++", duration))
    
        
    #progressbar_popup.destroy()
    #del progressbar_popup
    gui_class.audio_plot2(str(gui_class.current_plot2_type))
    gui_class.audio_plot1(str(gui_class.current_plot_type))

    audio_array_to_encode = audio_array_output
    return audio_array_to_encode

def decrypt_audio(audio_array_to_decode):
    global audio_array_output


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
                pass


    gui_class.audio_plot2()
    return audio_array_output

def remove_silence(audio_array_to_encode):

    # popup progress bar code #####################################
    global general_progress_bar1, progressbar_popup, general_pb_label, progressbar_label

    if "progressbar_popup" in globals():
        pass
    else:
        progressbar_popup = tk.Toplevel(height=100, width=400)


    progressbar_label = tk.Label(progressbar_popup, text="Silence is being removed")
    progressbar_label.place(x=150, y=25)
    
    general_progress_bar1 = ttk.Progressbar(progressbar_popup, orient="horizontal", length=350, mode='determinate')
    general_progress_bar1.place(x=25, y=50)

    general_pb_label = ttk.Label(progressbar_popup, text="0%")
    general_pb_label.place(x=150,y=75)

    progressbar_popup.update_idletasks()
    
    ##############################################################



    cutoff_level = -50 #dB
    max_value =  10**(cutoff_level/20)*((2**16)/2)

    for x in range(len(audio_array_to_encode)):
        if -max_value <= audio_array_to_encode[x] <= max_value:
            audio_array_to_encode[x] = 0

    zero_locations = np.where(np.array(audio_array_to_encode) == 0)
    start_index = zero_locations[0][0]
    length = 1
    array_of_zeros = []

    
    for x in range(len(zero_locations[0])):
        if x == 0:
            pass
        elif zero_locations[0][x] == zero_locations[0][x-1] + 1:
            length += 1
            if x == len(zero_locations[0])-1:
                array_of_zeros.append(start_index)
                array_of_zeros.append(length)
        elif zero_locations[0][x] != zero_locations[0][x-1] + 1:
            if length >= 600:
                array_of_zeros.append(start_index)
                array_of_zeros.append(length)
            start_index = zero_locations[0][x]
            length = 1

        general_progress_bar(x, len(zero_locations[0]))
        progressbar_popup.update_idletasks()
        
    audio_array_list = audio_array_to_encode.tolist()

    for y in range(len(array_of_zeros)-2,-1,-2):
        del audio_array_list[array_of_zeros[y]:(array_of_zeros[y]+(array_of_zeros[y+1]))]


    silence_array = []

    for z in range(len(array_of_zeros)):
        silence_array.append(math.floor(int(array_of_zeros[z])/(2**16)))
        silence_array.append(array_of_zeros[z] % (2**16))

    silence_array.append(10101)
    silence_array.append(20202)
    silence_array.append(30303)

    audio_array_to_encode = silence_array + audio_array_list

    audio_array_to_encode = np.array(audio_array_to_encode)
   
    general_progress_bar(1, 1)
    progressbar_popup.update_idletasks()

    return audio_array_to_encode

def add_silence(audio_array_to_decode):
    for x in range(len(audio_array_to_decode)):
        if audio_array_to_decode[x] == 10101 and audio_array_to_decode[x+1] == 20202 and audio_array_to_decode[x+2] == 30303:
            silence_array = audio_array_to_decode[:x]
            print(silence_array)




def general_progress_bar(increment, total):
    general_progress_bar1["value"] = increment/total * 100
    general_pb_label["text"] = update_general_pb()
    progressbar_popup.update_idletasks()

def update_general_pb():
    return f"Current Progress: {round(general_progress_bar1['value'],1)}%"


def donothing():
    pass



# run the application
gui_class = GUI(root)

root.mainloop()
