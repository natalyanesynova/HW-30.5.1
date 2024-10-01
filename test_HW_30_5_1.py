import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_all_my_pets(driver):
    # Здесь неявные ожидания для шага с вводом логина
    driver.implicitly_wait(3)
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('natalya.nesynova@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('1234ABC')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    # Проверяем, что мы оказались на странице с питомцами пользователя
    assert driver.find_element(By.ID, 'all_my_pets')


# Задание 1. На странице со списком питомцев пользователя присутствуют все питомцы
def test_all_pets_in_table(driver):
    driver.find_element(By.ID, 'email').send_keys('natalya.nesynova@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('1234ABC')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Считаем количество питомцев из статистики пользователя
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    # Считаем количество питомцев в таблице
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    # Проверяем, что 2 этих числа совпадают
    assert int(pets_number) == len(pets_count)


# Задание 2. На странице со списком питомцев пользователя хотя бы у половины питомцев есть фото
def test_half_pets_have_photo(driver):
    driver.find_element(By.ID, 'email').send_keys('natalya.nesynova@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('1234ABC')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Считаем количество питомцев из статистики пользователя
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    # Считаем количество питомцев с пустым значением src (то есть без фото)
    pets_count_without_photo = driver.find_elements(By.XPATH, '//tbody/tr/th/img[@src=""]')
    # Проверяем, что результат деления общего количества питомцев на количество питомцев без фото больше или равно 2
    # Это условие будет работать одинаково для четных и нечетных чмсел
    assert int(pets_number)/len(pets_count_without_photo) >= 2


# Задание 3. На странице со списком питомцев пользователя у всех питомцев есть имя, возраст и порода
def test_all_pets_with_data(driver):
    driver.find_element(By.ID, 'email').send_keys('natalya.nesynova@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('1234ABC')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    #Здесь неявные ожидания - для шага с подсчетом количества питомцев
    driver.implicitly_wait(3)
    # Считаем количество питомцев из статистики пользователя
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    # Создаем переменную для явных ожиданий
    wait = WebDriverWait(driver, 5)
    # Создаем списки имен, возрастов и пород
    # Здесь явные ожидания нужного нам элемента
    wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr/td[1]")))
    names = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    # Здесь явные ожидания нужного нам элемента
    wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr/td[2]")))
    ages = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    # Здесь явные ожидания нужного нам элемента
    wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr/td[3]")))
    breeds = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    # Проверяем, что количество элементов в каждом списке равно общему количеству питомцев
    assert len(names) == int(pets_number)
    assert len(ages) == int(pets_number)
    assert len(breeds) == int(pets_number)


# Задание 4. На странице со списком питомцев пользователя у всех питомцев разные имена
def test_unique_names_of_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('natalya.nesynova@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('1234ABC')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Создаем список имен
    names = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    list_names = [name.text for name in names]
    # Преобразуем список в множество
    unique_names = set(list_names)
    # Проверяем, что количество имен в списке равно количеству имен во множестве
    assert len(list_names) == len(unique_names)


# Задание 5. На странице со списком питомцев пользователя нет повторяющихся питомцев
# Повторяющиеся питомцы — это питомцы, у которых одинаковое имя, порода и возраст
def test_unique_data_of_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('natalya.nesynova@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('1234ABC')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Создаем список питомцев и пустой список
    pets = driver.find_elements(By.XPATH, '//tbody/tr')
    list_pets = []
    # С помощью цикла заполняем пустой список текстовыми данными вида "Имя Порода Возраст"
    for i in range(len(pets)):
        list_data = pets[i].text.split('\n')
        list_pets.append(list_data[0])
    # Преобразуем список в множество
    unique_list_pets = set(list_pets)
    # Проверяем, что количество данных в списке равно количеству данных во множестве
    assert len(list_pets) == len(unique_list_pets)
