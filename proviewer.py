from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import time
import pyautogui as pg
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
import cv2 as cv
import numpy as np

root = Tk()

root.geometry("500x500")
root.minsize(200, 300)

toolframe = LabelFrame(root, text="Toolbar")
imageframe = LabelFrame(root, bg="black")
funcframe = LabelFrame(root)

global cover_img_lbl
global temp_list
global firstcall
global save_img

firstcall = True
pil_images = []
image_locs = []
tkimages = []
comp_opt = []

comp_opt.append(16)
comp_opt.append(50)
for i in range(100, 401, 100):
    comp_opt.append(i)

for i in range(500, 2001, 250):
    comp_opt.append(i)

clicked = IntVar()
clicked.set(comp_opt[8])

comp_val = 1000


def blank():
    return


def imageNow(pil_img):
    global cover_img_lbl
    removeCurrent()
    cover_img_lbl = Label(imageframe, image=pil_img, bd=0)
    cover_img_lbl.pack()


def removeCurrent():

    try:
        cover_img_lbl.pack_forget()
    except:
        return


def convertToTkimg(pil_img_list):
    global cover_img_lbl
    if len(pil_img_list) == 0:
        return
    for i in pil_img_list:
        im = ImageTk.PhotoImage(i)
        tkimages.append(im)
    imageNow(tkimages[preview])
    btnPack(preview)


def exploreImages():
    global temp_list
    global preview

    temp_list = []
    preview = len(pil_images)
    root.file = filedialog.askopenfilenames(initialdir="C:/Users/Prakhar Sahu/Documents/python GUI/images",
                                            title="Select a file",
                                            filetypes=(('jpg file', '*.jpg'), ('all files', '*.*')))
    k = root.file
    for i in k:
        try:
            im = Image.open(i)
        except:
            continue
        temp_list.append(im)
        pil_images.append(im)
        image_locs.append(i)
    convertToTkimg(temp_list)
    temp_list.clear()


def btnPack(image_number):
    global firstcall
    if firstcall == True:
        firstcall = False
        return
    button_back = Button(
        funcframe, text="<<", command=lambda: back(image_number - 1))
    button_next = Button(
        funcframe, text=">>", command=lambda: next(image_number + 1))
    if image_number == len(tkimages) - 1:
        button_next = Button(funcframe, text=">>",
                             command=back, state=DISABLED)
    if image_number == 0:
        button_back = Button(funcframe, text="<<",
                             command=back, state=DISABLED)

    button_back.grid(row=1, column=2)
    button_next.grid(row=1, column=4)


def back(image_number):
    global cover_img_lbl
    global button_back
    global button_next

    imageNow(tkimages[image_number])
    btnPack(image_number)


def next(image_number):
    global cover_img_lbl
    global button_back
    global button_next

    imageNow(tkimages[image_number])
    btnPack(image_number)


def saveThis(save_img):
    file_loc = filedialog.asksaveasfilename(
        defaultextension=".png", initialdir="C:/Users/Prakhar Sahu/Pictures/Saved Pictures")
    save_img.save(file_loc)


def screenShot():
    global tkimg
    global save_img
    root.wm_state('iconic')
    time.sleep(.2)
    img = pg.screenshot()
    root.wm_deiconify()
    tkimg = ImageTk.PhotoImage(img)
    imageNow(tkimg)
    save_img = img


def imageCompress(comp_val):
    global nimg
    global save_img
    input_img = cv.imread(image_locs[0])
    input_img = cv.cvtColor(input_img, cv.COLOR_BGR2RGB)
    img_data = (input_img / 255.0).reshape(-1, 3)
    kmeans = MiniBatchKMeans(comp_val).fit(img_data)
    k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]
    k_img = np.reshape(k_colors, (input_img.shape))
    img_data = (k_img * 255.0)
    img_n = cv.normalize(src=img_data, dst=None, alpha=0,
                         beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    img_n = Image.fromarray(img_n)
    save_img = img_n
    nimg = ImageTk.PhotoImage(img_n)
    imageNow(nimg)


def selected(event):
    global comp_val
    comp_val = int(combo.get())


explore_btn = Button(toolframe, text="Open", command=exploreImages)
screen_cap_btn = Button(toolframe, text="Screen Shot", command=screenShot)
compress_btn = Button(toolframe, text="Compress",
                      bg="#EEB609", command=lambda: imageCompress(comp_val))
save_btn = Button(toolframe, text="Save as",
                  command=lambda: saveThis(save_img))

button_back = Button(funcframe, text="<<", command=back, state=DISABLED)
button_next = Button(funcframe, text=">>", command=lambda: next(1))
exit_button = Button(funcframe, text="Exit Program", command=root.quit)
zoom_btn = Button(funcframe, text="+")
colorpick_btn = Button(funcframe, text="?")


# BUTTONS Packing
toolframe.pack(fill=X)
explore_btn.grid(row=0, column=0)
screen_cap_btn.grid(row=0, column=1)
compress_btn.grid(row=0, column=3)
save_btn.grid(row=0, column=10, sticky=E)

combo = ttk.Combobox(toolframe, value=comp_opt)
combo.current(8)
combo.bind("<<ComboboxSelected>>", selected)
combo.grid(row=0, column=2, sticky=E, padx=5)


imageframe.pack(fill=BOTH, expand=True)

funcframe.pack(fill=X)
button_back.grid(row=1, column=2)
exit_button.grid(row=1, column=3)
button_next.grid(row=1, column=4)
zoom_btn.grid(row=1, column=0)
colorpick_btn.grid(row=1, column=1)


root.mainloop()
