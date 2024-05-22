import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

sitemap_url = 'https://www.baaqmd.gov/sitemap'
xpath = '//a[@class="chrt-sub-lft"]'


def get_links_from_sitemap(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    elements = tree.xpath(xpath)
    links = [element.get('href') for element in elements if element.get('href')]
    return links


def check_status_code(url):
    response = requests.get(url)
    return response.status_code


def check_logo_displayed(url, driver):
    driver.get(url)
    try:
        logo = driver.find_element(By.XPATH, '//div[@class="top-device-logo"]')
        return logo.is_displayed()
    except Exception as e:
        return False


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

links = get_links_from_sitemap(sitemap_url)

for link in links:
    full_url = link if link.startswith('http') else f'https://www.baaqmd.gov{link}'
    status_code = check_status_code(full_url)
    logo_displayed = check_logo_displayed(full_url, driver)

    print(f'URL: {full_url}')
    print(f'Status Code: {status_code}')
    print(f'Logo Displayed: {logo_displayed}')
    print('-' * 50)

driver.quit()
