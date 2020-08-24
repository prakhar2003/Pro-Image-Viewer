from tkinter import Tk, Label, LabelFrame, Button, IntVar, DISABLED, X, BOTH, E, W
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from time import sleep
from pyautogui import screenshot as ss
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from cv2 import cv2
from numpy import reshape

root = Tk()
root.title("Pro Image Viewer")
root.geometry("1280x700")
root.minsize(200, 300)

toolframe = LabelFrame(root, text="Toolbar")
imageframe = LabelFrame(root, bg="black")
funcbar = LabelFrame(root)
funcframe = LabelFrame(funcbar)

global cover_img_lbl
global temp_list
global firstcall
global save_img
global curr

curr = 0

firstcall = True
pil_images = []
image_locs = []
comp_opt = []

comp_opt.append(16)
comp_opt.append(50)
for i in range(100, 401, 100):
    comp_opt.append(i)

for i in range(500, 1001, 250):
    comp_opt.append(i)

clicked = IntVar()
clicked.set(comp_opt[8])

comp_val = 1000


def blank():
    print(imageframe.winfo_width())
    print(imageframe.winfo_height())


def imageNow(tkimg):
    global cover_img_lbl
    removeCurrent()
    cover_img_lbl = Label(imageframe, image=tkimg, bd=0)
    cover_img_lbl.pack(expand=True)


def removeCurrent():
    try:
        cover_img_lbl.pack_forget()
    except:
        return


def checkDim(pil_img):
    fw = imageframe.winfo_width()
    fh = imageframe.winfo_height()
    w, h = pil_img.size
    if w <= fw and h <= fh:
        return pil_img

    ratio = fh/h
    neww = int(w*ratio)
    if h > fh:
        pil_img = pil_img.resize((neww-5, fh-5))
        return pil_img


def convertToTkimg(pil_img):
    global tkimage
    tkimage = ImageTk.PhotoImage(checkDim(pil_img))
    imageNow(tkimage)


def exploreImages():
    global preview

    preview = len(pil_images)
    root.file = filedialog.askopenfilenames(initialdir="C:/Users/Prakhar Sahu/Documents/python GUI/images", title="Select a file", filetypes=(('jpg file', '*.jpg'), ('all files', '*.*')))

    k = root.file

    for i in k:
        try:
            im = Image.open(i)
        except:
            continue
        pil_images.append(im)
        image_locs.append(i)

    try:
        convertToTkimg(pil_images[preview])
        btnPack(preview)
    except:
        return


def btnPack(image_number):
    global firstcall
    global curr
    if firstcall == True:
        firstcall = False
        return
    button_back = Button(
        funcframe, text="<<", command=lambda: back(image_number - 1))
    button_next = Button(
        funcframe, text=">>", command=lambda: next(image_number + 1))
    if image_number == len(pil_images) - 1:
        button_next = Button(funcframe, text=">>", command=back, state=DISABLED)
    if image_number == 0:
        button_back = Button(funcframe, text="<<", command=back, state=DISABLED)
    curr = image_number
    button_back.grid(row=1, column=1, ipadx=12, ipady=3)
    button_next.grid(row=1, column=3, ipadx=12, ipady=3)


def back(image_number):
    global cover_img_lbl
    global button_back
    global button_next

    convertToTkimg(pil_images[image_number])
    btnPack(image_number)


def next(image_number):
    global cover_img_lbl
    global button_back
    global button_next
    try:
        convertToTkimg(pil_images[image_number])
        btnPack(image_number)
    except:
        return


def saveThis(save_img):
    try:
        file_loc = filedialog.asksaveasfilename(defaultextension=".png", initialdir="C:/Users/Prakhar Sahu/Pictures/Saved Pictures")
        save_img.save(file_loc)
    except:
        return


def screenShot():
    global save_img
    root.wm_state('iconic')
    sleep(.2)
    img = ss()
    root.wm_deiconify()
    convertToTkimg(img)
    save_img = img


def imageCompress(comp_val):
    global img_n
    global save_img
    input_img = cv2.imread(image_locs[curr])
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    img_data = (input_img / 255.0).reshape(-1, 3)
    kmeans = MiniBatchKMeans(comp_val).fit(img_data)
    k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]
    k_img = reshape(k_colors, (input_img.shape))
    img_data = (k_img * 255.0)
    img_n = cv2.normalize(src=img_data, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img_n = Image.fromarray(img_n)
    save_img = img_n
    convertToTkimg(img_n)


def selected(event):
    global comp_val
    comp_val = int(combo.get())


def leftRotate():
    try:
        pil_images[curr] = pil_images[curr].rotate(90, expand=1)
        convertToTkimg(pil_images[curr])
    except:
        return


def rightRotate():
    try:
        pil_images[curr] = pil_images[curr].rotate(270, expand=1)
        convertToTkimg(pil_images[curr])
    except:
        return


explore_btn = Button(toolframe, text="Open", command=exploreImages)
screen_cap_btn = Button(toolframe, text="Screen Shot", command=screenShot)
compress_btn = Button(toolframe, text="Compress", bg="#EEB609", command=lambda: imageCompress(comp_val))
save_btn = Button(toolframe, text="Save as", command=lambda: saveThis(save_img))

button_back = Button(funcframe, text="<<", command=back, state=DISABLED)
button_next = Button(funcframe, text=">>", command=lambda: next(1))
exit_button = Button(funcframe, text="Exit Program", command=root.quit, bg="#FF0021", fg="white")
left_rotate_btn = Button(funcframe, text="-90°", command=leftRotate)
right_rotate_btn = Button(funcframe, text="+90°", command=rightRotate)

# BUTTONS Packing
toolframe.pack(fill=X, ipady=2)
explore_btn.grid(row=0, column=0)
screen_cap_btn.grid(row=0, column=1)
compress_btn.grid(row=0, column=3)
save_btn.grid(row=0, column=10, sticky=E)

combo = ttk.Combobox(toolframe, value=comp_opt)
combo.current(8)
combo.bind("<<ComboboxSelected>>", selected)
combo.grid(row=0, column=2, sticky=E, padx=5)


imageframe.pack(fill=BOTH, expand=True)

funcbar.pack(fill=X)
funcframe.pack(pady=5)
button_back.grid(row=1, column=1, ipadx=12, ipady=3)
exit_button.grid(row=1, column=2, ipadx=12, ipady=3)
button_next.grid(row=1, column=3, ipadx=12, ipady=3)
left_rotate_btn.grid(row=1, column=0, ipadx=12, ipady=3)
right_rotate_btn.grid(row=1, column=4, ipadx=12, ipady=3)


root.mainloop()
