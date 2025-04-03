import customtkinter as ctk
from carbon_app import CarbonApp
from pollution_map import PollutionMapPage


class MainApp(ctk.CTk):
    frame_switch_count = 0

    def __init__(self):
        super().__init__()

        self.title("Jakość Powietrza i Mapa")
        self.configure(bg='#1E1E1E')  # Ciemne tło

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
        MainApp.frame_switch_count += 1  # Increment frame switch count
        print(f"Frame switch count: {MainApp.frame_switch_count}")  # Log the count


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
