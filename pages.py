# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code
import time


class UrbanRoutesPage:
    # Locators
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    taxi_option_locator = (By.XPATH, '//button[contains(text(), "Chamar")]')
    comfort_icon_locator = (By.XPATH, '//img[contains(@src, "/static/media/kids.075fd8d4.svg")]')
    comfort_active_locator = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')

    # NUMERO DE TELEFONE
    number_text_locator = (By.CSS_SELECTOR, ".np-button")
    number_enter = (By.ID, "phone")
    number_confirm = (By.CSS_SELECTOR, ".button.full")
    number_code = (By.ID, "code")
    code_confirm = (By.XPATH, '//button[contains(text(),"Confirmar")]')
    number_finish = (By.CSS_SELECTOR, ".np-text")

    from selenium.webdriver.common.by import By

    # Metodo de pagamento
    add_metodo_pagamento = (By.CSS_SELECTOR, ".pp-button.filled")
    add_card = (By.CSS_SELECTOR, ".pp-plus")
    number_card = (By.ID, "number")
    code_card = (By.CSS_SELECTOR, "input.card-input#code")
    add_finish_card = (By.XPATH, '//button[contains(text(),"Adicionar")]')
    close_button_card = (By.CSS_SELECTOR, ".payment-picker.open .close-button")
    comfirn_card = (By.CSS_SELECTOR, ".pp-value-text")

    # ADICIONAR COMENTÁRIO
    add_comment = (By.ID, "comment")

    # Pedir lençóis e cobertor
    switch_blanket = (By.CSS_SELECTOR, ".switch")
    switch_blanket_active = (By.CSS_SELECTOR, "#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1)"
)

    # Pedir sorvete
    add_icecream = (By.CSS_SELECTOR, ".counter-plus")
    ant_icecream = (By.CSS_SELECTOR, ".counter-value")

    call_taxi_button = (By.CSS_SELECTOR, ".smart-button")
    pop_up = (By.CSS_SELECTOR, ".order-header-title")

    def call_taxi(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.call_taxi_button)
        )
        button.click()

    def __init__(self, driver):
        self.driver = driver

    def enter_locations(self, from_text, to_text):
        self.enter_from_location(from_text)
        self.enter_to_location(to_text)

    # Preenche o campo "from"
    def enter_from_location(self, from_text):
        from_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.from_field)
        )
        from_input.clear()
        from_input.send_keys(from_text)

    def enter_to_location(self, to_text):
        to_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.to_field)
        )
        to_input.clear()
        to_input.send_keys(to_text)

    # Pega o valor do campo "from"
    def get_from_location_value(self):
        return WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.from_field)
        ).get_attribute("value")

    # Pega o valor do campo "to"
    def get_to_location_value(self):
        return WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.to_field)
        ).get_attribute("value")

    # Clica no botão de táxi
    def click_taxi_option(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.taxi_option_locator)
        ).click()

    # Clica no ícone de conforto
    def click_comfort_icon(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_icon_locator)
        ).click()

    def click_number_text(self, telefone):
        self.driver.find_element(*self.number_text_locator).click()
        self.driver.find_element(*self.number_enter).send_keys(telefone)
        self.driver.find_element(*self.number_confirm).click()
        code = retrieve_phone_code(self.driver)
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.number_code)
        )
        code_input.clear()
        code_input.send_keys(code)
        self.driver.find_element(*self.code_confirm).click()

    def numero_confirmado(self):
        numero = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.number_finish))
        return numero.text

    def click_add_cartao(self, cartao, code):
        self.driver.find_element(*self.add_metodo_pagamento).click()
        self.driver.find_element(*self.add_card).click()
        import time
        time.sleep(1)
        self.driver.find_element(*self.number_card).send_keys(cartao)
        time.sleep(1)
        self.driver.find_element(*self.code_card).send_keys(code)
        time.sleep(1)
        self.driver.find_element(*self.add_finish_card).click()
        self.driver.find_element(*self.close_button_card).click()

    def confirm_cartao(self):
        return self.driver.find_element(*self.comfirn_card).text

    def add_comentario(self, comentario):
        self.driver.find_element(*self.add_comment).send_keys(comentario)

    def coment_confirm(self):
        return self.driver.find_element(*self.add_comment).get_attribute("value")

    def switch_cobertor(self):
        switch_ativo = self.driver.find_element(*self.switch_blanket)
        switch_ativo.click()

    def switch_cobertor_active(self):
        return self.driver.find_element(*self.switch_blanket_active).is_displayed()

    def add_ice(self):
        self.driver.find_element(*self.add_icecream).click()

    # Dentro de UrbanRoutesPage
    def get_icecream_quantity(self):
        return self.driver.find_element(*self.ant_icecream).text

    def call_taxi(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def pop_up_show(self):
        pop_up = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.pop_up)
        )
        return pop_up.text

    def is_comfort_active(self):
        try:
            active_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.comfort_active_locator)
            )
            return "active" in active_button.get_attribute("class")
        except:
            return False