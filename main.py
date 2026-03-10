# main.py
import time
import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import retrieve_phone_code

from pages import UrbanRoutesPage

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Configurar Chrome com logging
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e acessível")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from_location_value() == data.ADDRESS_FROM
        assert routes_page.get_to_location_value() == data.ADDRESS_TO
        time.sleep(3)

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        assert routes_page.is_comfort_active()
        time.sleep(3)

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        routes_page.click_number_text(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER in routes_page.numero_confirmado()
        time.sleep(3)

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        assert "Cartão" in routes_page.confirm_cartao()
        time.sleep(3)

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        routes_page.add_comentario(data.MESSAGE_FOR_DRIVER)
        assert data.MESSAGE_FOR_DRIVER in routes_page.coment_confirm()
        time.sleep(3)

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        routes_page.switch_cobertor()
        assert routes_page.switch_cobertor_active() is True
        time.sleep(3)

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        for _ in range(2):routes_page.add_ice()
        assert int(routes_page.get_icecream_quantity()) == 2
        time.sleep(3)

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_from_location(data.ADDRESS_FROM)
        routes_page.enter_to_location(data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        routes_page.click_number_text(data.PHONE_NUMBER)
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.add_comentario(data.MESSAGE_FOR_DRIVER)
        routes_page.call_taxi()
        pop_up_text = routes_page.pop_up_show()
        assert "Buscar carro" in pop_up_text
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()