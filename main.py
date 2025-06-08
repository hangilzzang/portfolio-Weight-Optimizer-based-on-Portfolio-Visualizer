from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import *
from selenium.webdriver.support.ui import Select
import yaml
from calendar import month_name
import itertools
import pandas as pd
import random


# 설정 파일 불러오기
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

step = config["step"]

if 100 % step != 0:
    raise ValueError(
        f"Invalid step value: {step}. The step must be a number that divides 100 evenly "
        "to generate valid portfolio weight combinations. For example: 1, 5, 10, 20."
    )

# 브라우저 실행
driver = webdriver.Chrome()
driver.get("https://www.portfoliovisualizer.com/backtest-portfolio")
time.sleep(2)  # 페이지 로딩 대기

# 설정 완료
click_by_xpath(driver, xpath="//button[.//span[text()='Edit Portfolio']]") 
time.sleep(random.uniform(2.5, 5.0))
click_by_xpath(driver, xpath="//button[@id='inputSettings_btn']") 
select_by_xpath(driver, xpath="//select[@id='timePeriod']", visible_text="Month-to-Month")
select_by_xpath(driver, xpath="//select[@id='startYear']", visible_text=str(config["start_year"])) 
select_by_xpath(driver, xpath="//select[@id='firstMonth']", visible_text=month_name[config["first_month"]])
select_by_xpath(driver, xpath="//select[@id='endYear']", visible_text=str(config["end_year"])) 
select_by_xpath(driver, xpath="//select[@id='lastMonth']", visible_text=month_name[config["last_month"]])
select_by_xpath(driver, xpath="//select[@id='rebalanceType']", visible_text="No rebalancing")
click_by_xpath(driver, xpath="//button[@id='inputAssets_btn']")

# 티커수에 따라 필요한만큼 more클릭
tickers = config.get("ticker", [])
total_needed = len(tickers)
total_needed -= 10

while total_needed > 0:
    click_by_xpath(driver, xpath="//a[text()='More']")
    total_needed -= 10
    
# Asset 채워넣기
for idx, ticker in enumerate(tickers):
    click_search_icon_for_asset(driver, asset_index=idx+2) 
    type_keys(driver, ticker)
    click_first_ticker_suggestion(driver)
    click_by_xpath(driver, xpath="//button[@id='selectTicker']")


# 모든 조합생성
scale = int(100 // step) 
range_list = list(range(scale + 1))  # 예: step=5 → scale=20 → 0~20 
all_combinations = itertools.product(range_list, repeat=len(tickers)) # 모든 조합 생성 (중복 허용, 순서 고정)

valid_combinations = [
    [step * x for x in combo]
    for combo in all_combinations
    if sum(combo) == scale  # scale은 20, 즉 실제 비율 합은 20 * step = 100
]

results_df = pd.DataFrame(columns=[
    "Combination",
    "Annualized Return", 
    "Benchmark Relative",
    "Standard Deviation", 
    "Maximum Drawdown"
])

# 크롤링 시작
for idx in range(10):
    set_input_by_id(driver, f"allocation{idx+1}_1", "0")  


for combination in valid_combinations:
    
    for idx, value in enumerate(combination): # 조합값 적어 넣기
        set_input_by_id(driver, f"allocation{idx+1}_1", value)  
    click_by_xpath(driver, xpath="//input[@value='Analyze Portfolios']")    
    time.sleep(random.uniform(2.5, 5.0))
    
    annual_return, benchmark_relative, std_dev, max_drawdown = extract_performance_metrics(driver)
    combination_str = ", ".join(f"{ticker}:{weight}%" for ticker, weight in zip(tickers, combination))
    results_df.loc[len(results_df)] = [combination_str, annual_return, benchmark_relative, std_dev, max_drawdown]
    click_by_xpath(driver, xpath="//button[.//span[text()='Edit Portfolio']]") 

results_df.to_csv("output.csv", index=False)