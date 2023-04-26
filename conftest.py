from selenium import webdriver
import pytest
import settings


@pytest.fixture()
def browser():
    print('Browser start ...')
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get(settings.BASE_URL)

    yield browser

    print('Browser quit ...')
    browser.quit()
