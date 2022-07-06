import tkinter as tk
from tkinter import filedialog, messagebox
import PIL
from PIL import Image, ImageTk
from os.path import splitext
from main import bw_fill


def open_file():
    global img
    global filename

    filename = tk.filedialog.askopenfilename(
            initialdir='/',
            filetypes=(('Image Files', ('*.gif', '*.jpg', '*.jpeg', '*.png')), ('All Files', '*.*'))
        )
    img = Image.open(filename)
    display_original()


def display_original():
    global img
    global thumb
    global preview
    global confirm_button
    global cancel_button
    thumb = img.copy()
    thumb.thumbnail((130, 130))
    thumb = ImageTk.PhotoImage(thumb)
    preview.create_image(72, 72, image=thumb)
    confirm_button.config(state='active')
    cancel_button.config(state='active')
    # print(splitext(img))


def cancel():
    global thumb
    global confirm_button
    global cancel_button

    thumb = ''
    confirm_button.config(state='disabled')
    cancel_button.config(state='disabled')


def confirm():
    global img
    global processed_img
    global confirm_button
    global cancel_button
    # ask_wait()
    confirm_button.config(state='disabled')
    try:
        processed_img = bw_fill(img, protect=protect.get())
    except TypeError:
        messagebox.showerror(title='BwFill', message='There was an error. Please try another image file.')
        cancel()
        return
    except NameError:
        messagebox.showerror(title='BwFill', message='Tesseract not found. Restarting without text protection.')
        protect.set(False)
        confirm()
    else:
        popup = display_processed()
        popup.attributes('-topmost', True)
        popup.attributes('-topmost', False)

        if messagebox.askyesno(title='BwFill', message='Save image?'):
            popup.destroy()
            path, ext = splitext(filename)
            file = filedialog.asksaveasfilename(initialfile=f'{path}_bw{"_pr" if protect else ""}')
            # print(file + ext)
            processed_img.save(file + ext)
            cancel()
        else:
            popup.destroy()
            cancel_button.config(state='active')
            confirm_button.config(state='active')


def display_processed():
    global root
    global processed_img
    global bw_thumb

    bw_thumb = processed_img.copy()
    bw_thumb.thumbnail((500, 500))
    bw_thumb = ImageTk.PhotoImage(bw_thumb)

    show = tk.Toplevel(root)
    show.geometry('500x500')
    show.title('Preview')

    bw_preview = tk.Canvas(master=show, height=500, width=500)
    bw_preview.create_image(252, 252, image=bw_thumb)
    bw_preview.grid(row=0, column=0)

    return show

# Couldn't get this to work; popup appears after processing, defeating purpose
# def ask_wait():
#     global root
#     wait = tk.Toplevel(root)
#     wait.geometry('200x50')
#     wait.transient()
#     wait.title('BwFill')
#     tk.Label(wait, text='Processing, please wait...').pack(pady=10)


root = tk.Tk()
root.title('BwFill Utility')
root.config(padx=20, pady=10)
root.geometry('330x200')

filename = ''
thumb = tk.PhotoImage()
bw_thumb = tk.PhotoImage()
img = Image.Image()
processed_img = Image.Image()
# placeholders to dodge garbage collection

protect = tk.BooleanVar(value=True)

label = tk.Label(text='Select an image to\nconvert:', justify='left')
label.grid(row=0, column=0, sticky='NW')

load_button = tk.Button(text='Open', command=open_file)
load_button.grid(row=1, column=0, sticky='NW')

protect_check = tk.Checkbutton(text="Protect text?\n(requires tesseract)", justify='left',
                               variable=protect, onvalue=True, offvalue=False)
protect_check.grid(row=9, column=0)

preview = tk.Canvas(height=137, width=137, borderwidth='2', relief='groove')
preview.grid(row=0, column=1, rowspan=10, columnspan=2, padx=30)

confirm_button = tk.Button(text='Confirm', command=confirm)
confirm_button.config(state='disabled')
confirm_button.grid(row=10, column=1, sticky='E', padx=8)

cancel_button = tk.Button(text='Cancel', command=cancel)
cancel_button.config(state='disabled')
cancel_button.grid(row=10, column=2, sticky='W', padx=8)

root.mainloop()
