from html.parser import commentclose

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code
import time

class UrbanRoutesPage:
    # Endereços
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Botão de tarifa e chamada
    comfort_plan_card = (By.XPATH,'//div[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvxwyz"), "comfort")]')
    active_plan_card = (By.CSS_SELECTOR, 'div.tcard.active div.tcard-title')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Chamar um táxi")]')

    # Número de telefone
    phone_number_control = (By.CSS_SELECTOR, '.np-button')
    phone_number_input = (By.ID, 'phone')
    phone_number_code_input = (By.ID, 'code')
    phone_number_next_button = (By.CSS_SELECTOR, 'button.full')
    phone_number_confirm_button = (By.XPATH, '//button[contains(text(), "Confirmar")]')
    phone_number = (By.CSS_SELECTOR, '.np-text')

    # Pagamentos
    payment_method_select = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card_control = (By.XPATH, '//div[contains(text(), "Adicionar cartão")]')
    card_number_input = (By.ID, 'number')
    #card_code_input = (By.CSS_SELECTOR, 'input.card-input#code')
    card_credentials_confirm_button = (By.XPATH, '//button[contains(text(), "Link")]')
    close_button_payment_method = (By.CSS_SELECTOR, '.payment-picker.open .close-button')
    current_payment_method = (By.CSS_SELECTOR, '.pp-value-text')

    # Opções
    message_for_driver = (By.ID, 'comment')
    option_switches = (By.CSS_SELECTOR, '.switch')
    option_switches_inputs = (By.CSS_SELECTOR, '.switch-input')
    add_enumerable_option = (By.CSS_SELECTOR, '.counter-plus')
    amount_of_enumerable_option = (By.CSS_SELECTOR, '.counter-value')
    # Pedido
    order_car_button = (By.CSS_SELECTOR, '.smart-button-wrapper')
    order_popup = (By.CSS_SELECTOR, '.order-body')
    #loader = (By.CSS_SELECTOR, '.loader')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_adress):
        from_field = WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.from_field))
        from_field.send_keys(from_adress)

    def set_to(self, to_adress):
        field = WebDriverWait(self.driver, timeout=15).until(EC.element_to_be_clickable(self.to_field))
        field.clear()
        field.send_keys(to_adress)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_call_taxi_button(self):
        self.wait_for_loader_to_disappear()
        button = WebDriverWait(self.driver, timeout=15).until(
            EC.element_to_be_clickable(self.call_taxi_button)
        )
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(1)

    def set_route(self, from_address, to_address):
        self.set_from_address(from_address)
        self.set_to_address(to_address)
        self.click_call_taxi_button()

    def select_comfort_plan(self):
        try:
            self.wait_for_loader_to_disappear()
            time.sleep(1)
            active_plans = self.driver.find_elements(*self.active_plan_card)
            for plan in active_plans:
                if "comfort" in plan.text.lower():
                    return


            comfort_element = WebDriverWait(self.driver, timeout=15).until(EC.presence_of_element_located(self.comfort_plan_card))
            self.driver.execute_script("arguments[0].scrollIntoView();", comfort_element)
            time.sleep(0.5)
            comfort_element.click()
            time.sleep(1)

            WebDriverWait(self.driver, timeout=5).until(
                lambda d: "active" in comfort_element.find_elemente(By.XPATH, value= "./..").get_attribute("class"))

        except Exception as e:
            print(f"Erro ao selecionar plano Confort: {str(e)}")
            raise
    def get_current_selected_plan(self):
        return WebDriverWait(self.driver, timeout=10).until(EC.visibility_of_element_located(self.active_plan_card)).text.strip()

    def set_phone(self, number):
        self.wait_for_loader_to_disappear()
        WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(self.phone_number_control)).click()

        phone_input = WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(self.phone_number_input))
        phone_input.clear()
        phone_input.send_keys(number)

        WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(self.phone_number_next_button)).click()

        code = retrieve_phone_code(self.driver)

        code_input = WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(self.phone_number_code_input))
        code_input.clear()
        code_input.send_keys(code)

        WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(self.phone_number_confirm_button)).click()
        time.sleep(1)

    def get_phone(self):
        return WebDriverWait(self.driver, timeout=10).until(EC.visibility_of_element_located(self.phone_number)).text.strip()

    def set_card(self, card_number, code):
        try:
            self.wait_for_loader_to_disappear()
            time.sleep(2)
            try:
                payment_selector = WebDriverWait(self.driver, timeout=20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.pp-button.filled')))
                self.driver.execute_script("arguments[0].click();", payment_selector)
            except Exception:
                self.driver.execute_script("document.querySelector('.pp-button.filled').click();")
            time.sleep(1.5)

            self.driver.execute_script("document.querySelector('.pp-row.disabled').click();")
            time.sleep(2)

            card_num_field = WebDriverWait(self.driver, timeout=20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#number.card-input')))
            self.driver.execute_script(f"""
                var field = arguments[0];
                var text = '{card_number.replace(' ', '')}';
                field.value = '';
                for (var i = 0; i < text.length; i++) {{
                    field.value += text[i];
                    if ((i + 1) % 4 == 0 && i + 1 != text.length) {{
                        field.value += ' ';
                    }}
                }}
                field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
            """, card_num_field)
            time.sleep(0.5)

            card_code_field = WebDriverWait(self.driver, timeout=20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#code.card-input')))
            self.driver.execute_script(f"""
                arguments[0].value = '{code}';
                arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
            """, card_code_field)
            time.sleep(1)

            self.driver.execute_script("""
                var btn = document.querySelector('.button.full.disabled');
                if (btn) {
                    var event = new Event('validate', { bubbles: true });
                    document.querySelector('form').dispatchEvent(event);
                    if (btn.disabled) {
                        btn.disabled = false;
                        btn.classList.remove('disabled');
                    }
                }
            """)
            time.sleep(1)

            try:
                confirm_btn = WebDriverWait(self.driver, timeout=10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.button.full:not(.disabled)'))
                )
                confirm_btn.click()
            except:
                self.driver.execute_script("document.querySelector('form').submit();")
            time.sleep(2)

            try:
                close_btn = WebDriverWait(self.driver, timeout=10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.section-close.close-button'))
                )
                close_btn.click()
            except:
                pass

            WebDriverWait(self.driver, timeout=10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '.payment-picker.open'))
            )
            time.sleep(1)

            try:
                element = WebDriverWait(self.driver, timeout=10).until(
                    EC.visibility_of_element_located(self.current_payment_method)
                )
                return element.text.strip()
            except Exception:
                self.driver.save_screenshot("error_get_payment_method.png")
                return ""

        except Exception as e:
            self.driver.save_screenshot("error_set_card.png")
            raise Exception(f"Falha ao configurar cartão: {str(e)}")

    def set_message_for_driver(self, message):
        field = WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(self.message_for_driver))
        field.clear()
        field.send_keys(message)
        time.sleep(0.3)

    def get_message_for_driver(self):
        return WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(self.message_for_driver)
        ).get_property('value')

    def click_blanket_and_handkerchiefs_option(self):
        try:
            self.wait_for_loader_to_disappear()
            switches = WebDriverWait(self.driver, timeout=15).until(
                EC.presence_of_all_elements_located(self.option_switches)
            )
            if not switches:
                raise Exception("Nenhum switch de opções encontrado")

            self.driver.execute_script("arguments[0].scrollIntoView();", switches[0])
            time.sleep(1)
            try:
                switches[0].click()
            except:
                self.driver.execute_script("arguments[0].click();", switches[0])
            time.sleep(1)

            switch_input = switches[0].find_element(By.CSS_SELECTOR, 'input.switch-input')
            if not switch_input.get_property('checked'):
                raise Exception("Switch não foi ativado após clique")
        except Exception as e:
            self.driver.save_screenshot("erro_blanket_option.png")
            raise

    def get_blanket_and_handkerchiefs_option_checked(self):
        switches = WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_all_elements_located(self.option_switches_inputs)
        )
        return switches[0].get_property('checked')

    def add_ice_cream(self, amount):
        self.wait_for_loader_to_disappear()
        add_buttons = WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_all_element_located(self.add_enumerable_option))
        self.driver.execute_script("arguments[0].scrollIntoView();", add_buttons[0])
        for _ in range(amount):
            add_buttons[0].click()
            time.sleep(0.2)
        time.sleep(0.5)

    def get_amount_of_ice_cream(self):
        elements = WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_all_element_located(self.amount_of_enumerable_option))
        return int(elements[0].text.strip())

    def click_order_taxi_button(self):
        self.wait_for_loader_disappear()
        button = WebDriverWait(self.driver, timeout=15).until(
            EC.element_to_be_clickable(self.order_car_button))
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(1)

    def is_order_taxi_popup(self):
        try:
            self.wait_for_loader_disappear()
            time.sleep(2)
            popup_selectors = [
                (By.CSS_SELECTOR, '.order-popup, .confirmation-modal, .order-body'),
                (By.XPATH, '//*[contains(text(), "Pedido realizado") or contains(text(), "Order placed")]')
            ]
            for selector in popup_selectors:
                try:
                    popup = WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(selector))
                    if popup.is_displayed():
                        return True
                except:
                    continue
            return False
        except Exception as e:
            self.driver.save_screenshot("error_popup_not_found.png")
            return False