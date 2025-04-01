import tkinter as tk
from carbon_app import CarbonApp
from pollution_map import PollutionMapPage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Jakość Powietrza i Mapa")
        self.configure(bg='#ADD8E6')

        # Strony aplikacji
        self.frames = {}
        for F in (CarbonApp, PollutionMapPage):
            page_name = F.__name__
            frame = F(self, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("CarbonApp")

    def show_frame(self, page_name):
        """ Przełączanie między stronami aplikacji """
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
