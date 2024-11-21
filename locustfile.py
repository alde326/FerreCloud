from locust import HttpUser, task, between

class FerreCloudUser(HttpUser):
    host = "http://127.0.0.1:8000"  # URL base de tu aplicación
    wait_time = between(1, 3)  # Intervalo entre tareas

    def on_start(self):
        response = self.client.get("/accounts/login/")
        csrf_token = response.cookies.get('csrftoken')
        
        if csrf_token:
            response = self.client.post(
                "/accounts/login/",
                data={"username": "test_user", "password": "test_password"},
                headers={"X-CSRFToken": csrf_token}
            )
            
        else:
            print("No se obtuvo un token CSRF.")

    @task
    def index_page(self):
        """
        Prueba la página principal.
        """
        response = self.client.get("/")
        if response.status_code != 200:
            print(f"Error en index_page: {response.status_code}, {response.text}")

    @task
    def ventas_dashboard(self):
        """
        Prueba la ruta del dashboard de ventas.
        """
        response = self.client.get("/ventas/")
        if response.status_code != 200:
            print(f"Error en ventas_dashboard: {response.status_code}, {response.text}")

    @task
    def inventario_index(self):
        """
        Prueba la ruta del inventario.
        """
        response = self.client.get("/inventario/")
        if response.status_code != 200:
            print(f"Error en inventario_index: {response.status_code}, {response.text}")

    @task
    def regimen_simple_index(self):
        """
        Prueba la ruta del RST.
        """
        response = self.client.get("/impuestos/")
        if response.status_code != 200:
            print(f"Error en RST_index: {response.status_code}, {response.text}")

