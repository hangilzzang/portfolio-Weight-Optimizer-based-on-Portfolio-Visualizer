from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


def click_by_xpath(driver, xpath: str, timeout: float = 10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()

def select_by_xpath(driver, xpath: str, visible_text: str, timeout: float = 10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    select_elem = Select(driver.find_element(By.XPATH, xpath))
    select_elem.select_by_visible_text(visible_text)

def type_keys(driver, text: str, timeout: float = 10):
    def is_input_focused(d):
        try:
            el = d.switch_to.active_element
            return el.tag_name == "input" and el.is_enabled()
        except StaleElementReferenceException:
            return False

    WebDriverWait(driver, timeout).until(is_input_focused)
    active_elem = driver.switch_to.active_element
    active_elem.send_keys(text)

def click_first_ticker_suggestion(driver, timeout: float = 10):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tt-selectable')]"))
    ).click()

def click_search_icon_for_asset(driver, asset_index: int):
    xpath = f"(//span[@title='Find ticker symbol'])[{asset_index}]"
    click_by_xpath(driver, xpath)


def set_input_by_id(driver, element_id: str, value: str, timeout: float = 10):
    input_elem = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, element_id))  # ✅ 클릭 가능한 상태까지 기다림
    )
    input_elem.clear()
    input_elem.send_keys(str(value))
    
def extract_performance_metrics(driver, timeout: float = 10) -> tuple[float, float, float]:
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ph-data-value"))
    )
    # 텍스트 추출 후 % 제거하고 float 변환
    values = [float(el.text.strip().replace("%", "")) for el in elements]
    if len(values) < 3:
        raise ValueError(f"Expected at least 3 performance values, got {len(values)}: {values}")
    return values[0], values[1], values[2], values[3]  # annual_return, std_dev, max_drawdown