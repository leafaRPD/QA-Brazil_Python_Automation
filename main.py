import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        #
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        # Implementou uma pausa
        # verifique se a URL não expirou
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes.")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está em execução.")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from() == data.ADDRESS_FROM
        assert routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort_plan()

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        phone_number = data.PHONE_NUMBER
        routes_page.set_phone(phone_number)
        assert routes_page.get_phone() == phone_number

    def test_fill_card(self):
        self.driver.maximize_window()
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        # Fluxo completo necessário
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort_plan()
        routes_page.set_phone(data.PHONE_NUMBER)  # Adicionado

        # Teste do cartão
        routes_page.set_card(data.CARD_NUMBER, data.CARD_CODE)

        #print("função criada para preencher os dados do cartão")
        #pass

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        message = data.MESSAGE_FOR_DRIVER
        routes_page.set_message_for_driver(message)
        assert routes_page.set_message_for_driver() == message
        #print("função criada para comentar para o motorista")
        #pass

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort_plan()
        routes_page.click_blanket_and_handkerchiefs_option()
        assert routes_page.get_blanket_and_handkerchiefs_option_checked()
        #print("função criada para pedir cobertor e lenços")
        #pass

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort_plan()
        number_of_ice_creams = 2
        routes_page.add_ice_cream(number_of_ice_creams)
        assert routes_page.get_amount_of_ice_cream() == 2

        # print("função criada para pedir 2 sorvetes")
        # for _ in range(2):
        #     # Adicionar em S8
        #     pass

    def test_car_search_model_appears(self):
        # Adicionar em S8
        print("função criada para verificar se o modelo do carro aparece")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


