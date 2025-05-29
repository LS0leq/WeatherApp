from locust import HttpUser, task, between

class WeatherAppUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def get_air_quality(self):
        # Przykład zapytania do endpointu jakości powietrza (dostosuj adres do swojej aplikacji)
        self.client.get("/v2/city?city=Warsaw&state=Mazovia&country=POLAND&key=TEST_API_KEY")

    @task(1)
    def get_forecast(self):
        # Przykład zapytania do endpointu prognozy pogody (dostosuj adres do swojej aplikacji)
        self.client.get("/VisualCrossingWebServices/rest/services/timeline/Warsaw?key=TEST_API_KEY&include=hours")
