import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import settings


# TXE-001
def test_open_authentication_page(browser):
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'Авторизация', 'Fail'


# TXE-002
def test_change_mail_tab(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.mail)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'Почта'


# TXE-003
def test_change_login_tab(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.login)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'Логин'


# TXE-004
def test_change_account_tab(browser):
    browser.find_element(By.ID, 'username').send_keys('010101010101')
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'Лицевой счёт', 'FAIL'


# TXE-005
def test_authentication_vk(browser):
    browser.find_element(By.ID, 'oidc_vk').click()
    assert 'vk.com' in browser.find_element(By.XPATH, '//div[@class="oauth_head"]/a').get_attribute('href')
    assert 'vk' in browser.current_url


# TXE-006
def test_authentication_ok(browser):
    browser.find_element(By.ID, 'oidc_ok').click()
    assert 'Одноклассники' == browser.find_element(By.XPATH, '//div[@class="ext-widget_h_tx"]').text
    assert 'ok' in browser.current_url


# TXE-007
def test_authentication_mail(browser):
    browser.find_element(By.ID, 'oidc_mail').click()
    assert 'mail.ru' in browser.find_element(By.XPATH, '//span[@class="header__logo"]').text.lower()
    assert 'mail' in browser.current_url


# TXE-008
def test_authentication_google(browser):
    browser.find_element(By.ID, 'oidc_google').click()
    assert 'google' in browser.current_url


# TXE-009
def test_authentication_yandex(browser):
    browser.find_element(By.ID, 'oidc_ya').click()
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, 'passp:sign-in')))
    assert 'yandex' in browser.current_url


# TXE-010
def test_user_agreement(browser):
    browser.find_element(By.XPATH, '//div[@class="auth-policy"]/a').click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'


# TXE-011
def test_redirect_registration(browser):
    browser.find_element(By.ID, 'kc-register').click()
    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Регистрация'


# TXE-012
def test_privacy_policy(browser):
    browser.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[0].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'


# TXE-013
def test_agreements(browser):
    browser.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[1].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'


# TXE-014
def test_redirect_password_reset(browser):
    browser.find_element(By.ID, 'forgot_password').click()
    assert browser.find_element(By.CLASS_NAME, 'card-container__title').text == 'Восстановление пароля'


# TXE-015
@pytest.mark.xfail(reason='Аккаунт уже существует в системе')
def test_registration_page(browser):
    browser.find_element(By.ID, 'kc-register').click()

    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys('Иван')
    inputs[1].send_keys('Иванов')
    inputs[2].send_keys('Москва')
    inputs[3].send_keys(settings.mail)
    inputs[4].send_keys(settings.password)
    inputs[5].send_keys(settings.password)

    browser.find_element(By.NAME, 'register').click()

    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Подтверждение email', 'Такой пользователь зарегистрирован'


# TXE-016
@pytest.mark.xfail(reason='Капча не пройдена')
def test_reset_password_by_mail(browser):
    browser.find_element(By.ID, 'forgot_password').click()
    browser.find_element(By.ID, 'username').send_keys(settings.mail)

    browser.find_element(By.ID, 'captcha').send_keys()
    browser.find_element(By.ID, 'reset')

    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Восстановление пароля'


# TXE-017
def test_auth_by_mail(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.mail)
    browser.find_element(By.ID, 'password').send_keys(settings.password)
    browser.find_element(By.ID, 'kc-login').click()

    assert browser.find_element(By.ID, 'logout-btn')


# TXE-018
@pytest.mark.xfail(reason='Отобразилась капча')
def test_auth_incorrect_mail(browser):
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys(settings.invalid_mail)
    inputs[1].send_keys(settings.invalid_password)
    browser.find_element(By.ID, 'kc-login').click()

    assert browser.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


# TXE-019
def test_empty_form(browser):
    browser.find_element(By.ID, 'kc-register').click()
    browser.find_element(By.NAME, 'register').click()

    err = browser.find_elements(By.XPATH, '//span[contains(@class, "rt-input-container__meta--error")]')
    assert len(err) == 5
