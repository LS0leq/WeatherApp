import tkinter as tk
from carbon_app import CarbonApp
from pollution_map import PollutionMapPage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Jakość Powietrza i Mapa")
        self.configure(bg='#2E2E2E')

        # Strony aplikacji
        self.frames = {}

        carbon_frame = CarbonApp(self, self)
        self.frames["CarbonApp"] = carbon_frame
        carbon_frame.pack(fill="both", expand=True)

        # UWAGA: NIE pakujemy tutaj pollution_frame!
        self.pollution_frame = PollutionMapPage(self, self)
        self.frames["PollutionMapPage"] = self.pollution_frame
        self.pollution_frame.pack_forget()  # Upewniamy się, że nie jest widoczna

        self.show_frame("CarbonApp")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
