import tkinter as tk
from main_menu import MainMenu  
from PIL import Image, ImageTk
from game import center_window

# This Page only has a "Back" button.
# The Information is displayed through text on the background image for simplicity.

class InfoPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Information")
        self.root.geometry("600x800")
        center_window(self.root)
        image = Image.open("../images/about_us.png") 
        self.bg_image = ImageTk.PhotoImage(image) 
        self.canvas = tk.Canvas(root, width=600, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        back_button = tk.Button(self.root, text="Back", font=("Fixedsys", 12, "bold"),
                                bg="#5a7547", fg="white", borderwidth=0, highlightthickness=0,
                                activebackground="#86a340", activeforeground="white",
                                command=self.back_to_main_menu)
        back_button.place(x=10, y=10, width=80, height=40)

    def back_to_main_menu(self):
        self.root.destroy()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    InfoPage(root)
    root.mainloop()
