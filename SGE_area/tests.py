from django.test import TestCase, Client
from .models import Area, TipoMantenimientoArea, MantenimientoArea
from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth.models import User

class AreaModelTest(TestCase):
    def setUp(self):
        self.area = Area.objects.create(
            nombre="Área de prueba",
            tamaño="Grande",
            encargado="Juan Perez",
            teléfono_encargado="123456789",
            fecha_ultimo_mantenimiento=date.today() - timedelta(days=40),
            intervalo_mantenimiento=30
        )

    def test_dias_restantes_mantenimiento(self):
        self.assertEqual(self.area.dias_restantes_mantenimiento(), 30)

    def test_area_str(self):
        self.assertEqual(str(self.area), "Área de prueba")

class MantenimientoAreaModelTest(TestCase):
    def setUp(self):
        self.tipo_mantenimiento = TipoMantenimientoArea.objects.create(tipo="Mantenimiento preventivo")
        self.area = Area.objects.create(
            nombre="Área de prueba",
            tamaño="Grande",
            encargado="Juan Perez",
            teléfono_encargado="123456789",
            fecha_ultimo_mantenimiento=date.today() - timedelta(days=40),
            intervalo_mantenimiento=30
        )
        self.mantenimiento = MantenimientoArea.objects.create(
            area=self.area,
            tipo=self.tipo_mantenimiento,
            fecha=date.today(),
            hora="12:00:00"
        )

    def test_mantenimiento_str(self):
        self.assertEqual(str(self.mantenimiento), "Area: Área de prueba, Tipo: Mantenimiento preventivo, Fecha: {}".format(date.today()))

    def test_actualizar_fecha_ultimo_mantenimiento_signal(self):
        self.assertEqual(self.area.fecha_ultimo_mantenimiento, date.today())


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_render_area_page(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('area'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'SGE_area/area.html')

    def test_create_new_area(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('crear_area'), {'nombre': 'Nueva Área', 'descripcion': 'Descripción de prueba'})
        self.assertEqual(response.status_code, 302)  # Verifica que se redirige después de crear un área

        # Verifica que el área se haya creado en la base de datos
        new_area = Area.objects.get(nombre='Nueva Área')
        self.assertEqual(new_area.descripcion, 'Descripción de prueba')

    # Continúa con pruebas similares para las demás vistas y funcionalidades

    def test_generate_monthly_maintenance_document(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('generar_documento_mantenimientos_por_mes'), {'mes': '11', 'anio': '2023'})
        self.assertEqual(response.status_code, 200)  # Verifica que se genera el documento correctamente

    def test_generate_area_maintenance_document(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('generar_documento_mantenimientos_area', kwargs={'id': 1}), {'mes': '11', 'anio': '2023'})
        self.assertEqual(response.status_code, 200)  # Verifica que se genera el documento correctamente
