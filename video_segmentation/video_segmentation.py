import cv2
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

#setting up the window
root = Tk()
root.resizable(True, True)
root.geometry('1080x720') #default dimensions
root.title("Video Segmentation GUI")

paused = False #whether or not we have permission to scrub
clicked_points = [] #list of clicked points we'll draw 'X's on

def scrub_video(file_path):
    global paused, clicked_points
    video_capture = cv2.VideoCapture(file_path)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    current_frame = 0  #start at first frame

    def update_frame():
        global paused, clicked_points
        nonlocal current_frame
        read_correctly, frame = video_capture.read()
        if not read_correctly: return

        current_frame = max(0, min(current_frame, total_frames-1)) #bound the current_frame between the first and last frame of the video
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame) #set's the video capture from it's prev set frame to curr_frame

        #if read_correctly:
        #convert from BGR (OpenCV format) to RGB (Tkinter format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #set the size of the displayed frame to fill the root window
        frame_width = root.winfo_width()
        frame_height = root.winfo_height()
        frame = cv2.resize(frame, (frame_width, frame_height))

        #draw an 'X' for every point in the list
        if paused:
            for (x, y) in clicked_points:
                cv2.line(frame, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)  # Left-top to Right-bottom
                cv2.line(frame, (x - 10, y + 10), (x + 10, y - 10), (255, 0, 0), 2)  # Right-top to Left-bottom
                print("draw x at: ", (x,y))
            

        image = Image.fromarray(frame) #convert frame to image object
        photo = ImageTk.PhotoImage(image) #then Image format to ImageTkinter format for display
        
        stretch_widget_label.config(image=photo) #update the label with the new frame
        stretch_widget_label.image = photo  #(Keep a reference to avoid garbage collection)

    ### handle user input (used for scrubbing controls) ###
    def key_handler(event):
        nonlocal current_frame
        global paused
        if paused: return
        if event.keysym == 'j': #'j' = left 1 frame
            if current_frame > 0:
                current_frame -= 1
            update_frame()
        elif event.keysym == 'l': #'l' = right 1 frame
            current_frame += 1
            update_frame()
    
    def mouse_click_handler(event):
        if not paused: return #only count x's on selected frame
        x, y = event.x, event.y
        clicked_points.append((x, y))
        update_frame()

    #initialize label that will be used to stretch frame to window
    global stretch_widget_label
    stretch_widget_label = Label(root)
    stretch_widget_label.pack(fill=BOTH, expand=True)

    #call key_handler on j, l presses
    root.bind('<KeyPress-j>', key_handler)
    root.bind('<KeyPress-l>', key_handler)
    stretch_widget_label.bind("<Button-1>", mouse_click_handler)

    update_frame()

def upload_video():
    print("uploading video...")
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("MP4s", "*.mp4"), ("All Files", "*.*"))
    )
    if not file_path:
        print("Invalid Path to Video")
        return
    menu.add_cascade(label='Annotate Frame', command=select_frame)
    scrub_video(file_path)

def select_frame():
    print("frame selected. Frame scrubbing disabled.")
    global paused
    paused = True

#menu bar
menu = Menu(root)
item = Menu(menu)
item.add_command(label='Upload', command=upload_video)
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

root.mainloop()