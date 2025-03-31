import customtkinter as ctk
from modules.map_component import MapComponent
from modules.info_component import InfoComponent


class PollutionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mapa Zanieczyszczenia Powietrza")
        self.geometry("1000x600")
        self.configure(bg="#2E2E2E")

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.info_component = InfoComponent(self)
        self.map_component = MapComponent(self, self.info_component)

        self.map_component.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.info_component.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = PollutionApp()
    app.mainloop()
