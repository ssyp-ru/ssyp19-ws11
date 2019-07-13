у from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from CompletedProject import MeshLab
from CompletedProject import project3d


point_cloud = []

coordinates1 = []
coordinates2 = []

angle = 0

# Standard File Path
FilePath1 = 'C:/Users/Admin/Pictures/1.jpg'
FilePath2 = 'C:/Users/Admin/Pictures/2.jpg'

Flag = True

# Internal camera parameters
K = np.array([[450, 0, 640/2],
              [0, 450, 480/2],
              [0, 0, 1]])

# Camera movement settings
C = np.array([[0, 0, 0],
              [-15, -15, 0],
              [0, -30, 0],
              [15, -15, 0],
              [0, 0, 0]])


# Camera rotate calculation
def rot_matrix(alpha, beta, gamma):
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    cc, sc = np.cos(gamma), np.sin(gamma)
    return np.array([[cc * cb, cc * sb * sa - sc * ca, cc * sb * ca + sc * sa],
                     [sc * cb, sc * sb * sa + cc * ca, sc * sb * ca - cc * sa],
                     [-sb, cb * sa, cb * ca]])


# "Set picture" button function, where you can choose another picture
def choose_filepath():
    global FilePath1
    global Img1
    global Img2
    FilePath1 = filedialog.askopenfilename(parent=root, initialdir='~/Pictures', title='please, choose')
    Img1 = Img2
    Img2 = ImageTk.PhotoImage(Image.open(FilePath1))
    label1.config(image=Img1)
    label2.config(image=Img2)


# Calculating cords on click
def set_coords1(event):
    coordinates1.append([])
    coordinates1[-1].append([event.x])
    coordinates1[-1].append([event.y])
    coordinates1[-1].append([1])

    global Flag
    Flag = False


def set_coords2(event):
    coordinates2.append([])
    coordinates2[-1].append([event.x])
    coordinates2[-1].append([event.y])
    coordinates2[-1].append([1])

    global Flag
    Flag = True


# "-90" button function, adds 90 degrees for calculating
def addrotate():
    global angle, coordinates2, coordinates1

    for p1, p2 in zip(coordinates1, coordinates2):
        point_cloud.append(project3d.calculating(p1, p2,
                                                 rot_matrix(-np.pi/2, 0, angle*np.pi/2),
                                                 rot_matrix(-np.pi/2, 0, (angle+1)*np.pi/2),
                                                 K, K, np.concatenate((C[angle], C[angle+1]))))
    angle = (angle+1) % 4
    coordinates1.clear()
    coordinates2.clear()


# "Ready" button function, confirms coordinates
def finish():
    if Flag:
        addrotate()  # calculate the last bunch of coordinates
        pcount = len(point_cloud)
        for i in range(1, pcount):
            point_cloud.extend(project3d.linear_interpolation(point_cloud[i], point_cloud[i-1]))
        MeshLab.write(point_cloud)  # write out all the data at once
        root.destroy()
    else:
        print('Choose coords')


if __name__ == "__main__":
    root = Tk()

    # First image label
    Img1 = ImageTk.PhotoImage(Image.open(FilePath1))
    label1 = Label(image=Img1)
    label1.grid(row=0, column=0, sticky=N + W)

    # Second image label
    Img2 = ImageTk.PhotoImage(Image.open(FilePath2))
    label2 = Label(image=Img2)
    label2.grid(row=0, column=1, sticky=N + E)

    # On click functions
    label1.bind("<Button 1>", set_coords1)
    label2.bind("<Button 1>", set_coords2)

    # "Ready" button
    button = Button(root, text="Ready", command=finish)
    button.grid(row=1, column=0, sticky=S + W)

    # "-90" button
    rotate = Button(root, text='-90', command=addrotate)
    rotate.grid(row=1, column=0, sticky=S + E)

    # "Set picture" button
    spb = Button(root, text='Set picture', command=choose_filepath)
    spb.grid(row=1, column=1, sticky=S + E)

    root.mainloop()
