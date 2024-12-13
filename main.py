from tkinter import Tk
from burgerapp import BurgerOrderingApp

if __name__=="__main__":
    root = Tk()
    app = BurgerOrderingApp(root)
    root.mainloop()