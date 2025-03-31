import customtkinter as ctk

class InfoComponent(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3A3A3A")

        self.info_label = ctk.CTkLabel(self, text="Wybierz lokalizację na mapie",
                                       font=("Arial", 16), text_color="white")
        self.info_label.pack(pady=20)

    def update_info(self, location, pollution_data):
        if pollution_data:
            pollution_text = self.get_pollution_description(pollution_data)
        else:
            pollution_text = "Brak danych o zanieczyszczeniach"

        self.info_label.configure(text=f"Lokalizacja: {location}\n\n{pollution_text}")

    def get_pollution_description(self, pollution_data):
        descriptions = []

        if pollution_data['co'] > 1000:
            descriptions.append("CO: Bardzo wysoki poziom! Możliwe zatrucie.")
        elif pollution_data['co'] > 500:
            descriptions.append("CO: Wysoki poziom, może powodować problemy oddechowe.")

        if pollution_data['no2'] > 200:
            descriptions.append("NO₂: Bardzo wysoki poziom, zagrożenie dla astmatyków.")
        elif pollution_data['no2'] > 100:
            descriptions.append("NO₂: Średni poziom, może pogarszać stan układu oddechowego.")

        if pollution_data['pm2_5'] > 100:
            descriptions.append("PM2.5: Bardzo wysoki poziom, ryzyko chorób serca.")
        elif pollution_data['pm2_5'] > 50:
            descriptions.append("PM2.5: Średni poziom, możliwe problemy oddechowe.")

        return "\n".join(descriptions) if descriptions else "Powietrze jest czyste!"
