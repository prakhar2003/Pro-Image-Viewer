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

# Main Frame declaration
toolframe = LabelFrame(root, text="Toolbar")
imageframe = LabelFrame(root, bg="black")
funcframe = LabelFrame(root)

'''
cover_img = ImageTk.PhotoImage(Image.new('RGB', (200, 200)))
cover_img_lbl = Label(imageframe, image=cover_img, bd=0)
'''

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


def blank():
    return


def convert_to_tkimg(pil_imgs):
    global cover_img_lbl
    for i in pil_imgs:
        im = ImageTk.PhotoImage(i)
        tkimages.append(im)

    cover_img_lbl = Label(imageframe, image=tkimages[0])
    cover_img_lbl.pack()


def explore_images():

    root.file = filedialog.askopenfilenames(initialdir="C:/Users/Prakhar Sahu/Documents/python GUI/images",
                                            title="Select a file",
                                            filetypes=(('jpg file', '*.jpg'), ('all files', '*.*')))
    k = root.file
    for i in k:
        try:
            im = Image.open(i)
        except:
            continue

        pil_images.append(im)
        image_locs.append(i)
    cover_img_lbl.pack_forget()
    convert_to_tkimg(pil_images)


def back(image_number):
    global cover_img_lbl
    global button_back
    global button_next

    cover_img_lbl.pack_forget()
    cover_img_lbl = Label(imageframe, image=tkimages[image_number-1])
    button_back = Button(
        funcframe, text="<<", command=lambda: back(image_number - 1))
    button_next = Button(
        funcframe, text=">>", command=lambda: next(image_number + 1))

    if image_number == len(tkimages):
        button_back = Button(funcframe, text=">>",
                             command=back, state=DISABLED)

    cover_img_lbl.pack()
    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=2)


def next(image_number):
    global cover_img_lbl
    global button_back
    global button_next

    cover_img_lbl.pack_forget()
    cover_img_lbl = Label(imageframe, image=tkimages[image_number-1])
    button_back = Button(
        funcframe, text="<<", command=lambda: back(image_number - 1))
    button_next = Button(
        funcframe, text=">>", command=lambda: next(image_number + 1))

    if image_number == len(tkimages):
        button_next = Button(funcframe, text=">>",
                             command=next, state=DISABLED)

    cover_img_lbl.pack()
    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=2)


def save_op():
    save_btn = Button(toolframe, text="Save as")
    save_btn.grid(row=0, column=10, sticky=E)


def screenShot():
    global img
    global cover_img_lbl
    root.wm_state('iconic')
    time.sleep(.2)
    img = pg.screenshot()
    root.wm_deiconify()
    img = ImageTk.PhotoImage(img)
    cover_img_lbl = Label(imageframe, image=img)
    cover_img_lbl.pack()
    save_op()


def img_compress(comp_val):
    global nimg

    top = Toplevel()
    imgfrm = LabelFrame(top)
    imgfrm.grid(row=1, column=0, columnspan=2)
    input_img = cv.imread("1-Saint-Basils-Cathedral.jpg")
    input_img = cv.cvtColor(input_img, cv.COLOR_BGR2RGB)
    img_data = (input_img / 255.0).reshape(-1, 3)
    kmeans = MiniBatchKMeans(comp_val).fit(img_data)
    k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]
    k_img = np.reshape(k_colors, (input_img.shape))
    img_data = (k_img * 255.0)
    img_n = cv.normalize(src=img_data, dst=None, alpha=0,
                         beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    nimg = Image.fromarray(img_n)
    nimg = ImageTk.PhotoImage(nimg)
    lbl = Label(imgfrm, image=nimg)
    lbl.pack(fill=BOTH, expand=True)
    save = Button(top, text="Save")
    save.grid(row=0, column=1, sticky=E)

    #drop = OptionMenu(top, clicked, *comp_opt, command=blank)
    #drop.grid(row=0, column=0, sticky=W, padx=5, ipadx=20)

    combo = ttk.Combobox(top, value=comp_opt)
    combo.current(8)
    combo.bind("<<ComboboxSelected>>", blank)
    combo.grid(row=0, column=0, sticky=W, padx=5, ipadx=20)


def imageShow(curr_img):
    curr_img = ImageTk.PhotoImage(curr_img)


# Sub elements declarations
explore_btn = Button(toolframe, text="Open", command=explore_images)
screen_cap_btn = Button(toolframe, text="Screen Shot", command=screenShot)
compress_btn = Button(toolframe, text="Compress", bg="#EEB609",
                      command=lambda: img_compress(1000))

button_back = Button(funcframe, text="<<", command=back, state=DISABLED)
button_next = Button(funcframe, text=">>", command=lambda: next(2))
exit_button = Button(funcframe, text="Exit Program", command=root.quit)
zoom_btn = Button(funcframe, text="+")
colorpick_btn = Button(funcframe, text="?")


# BUTTONS Packing
toolframe.pack(fill=X)
explore_btn.grid(row=0, column=0)
screen_cap_btn.grid(row=0, column=1)
compress_btn.grid(row=0, column=2)

imageframe.pack(fill=BOTH, expand=True)
# cover_img_lbl.pack()

funcframe.pack(fill=X)
button_back.grid(row=1, column=2)
exit_button.grid(row=1, column=3)
button_next.grid(row=1, column=4)
zoom_btn.grid(row=1, column=0)
colorpick_btn.grid(row=1, column=1)


root.mainloop()
