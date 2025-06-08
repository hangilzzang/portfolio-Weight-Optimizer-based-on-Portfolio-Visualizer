# 📊 portfolio Weight Optimizer based on Portfolio Visualizer

많은 투자자들이 포트폴리오를 구성할 때 **정확히 어떤 비율로 자산을 나눠야 할지** 고민합니다.  

이 크롤링 코드는 [Portfolio Visualizer](https://www.portfoliovisualizer.com/backtest-portfolio) 웹사이트에서
사용자가 선택한 종목들의 모든 비율 조합을 계산하고, 각 조합에 대한 연간 수익률, 표준편차, 최대 낙폭 등의 핵심 지표를 자동으로 수집해
CSV 파일로 깔끔하게 정리해줍니다. 

<br> 

![예시 이미지](https://i.imgur.com/mFBFTdD.png) 
 
<br>

## 🖥️ 실행 환경

- Python 3.10+
- chromedriver
- selenium
- pandas

<br>

## ⚙️ 사용법

1. `config.yaml`에 테스트할 종목 티커와 백테스트 기간등을 설정합니다: 
    ```yaml 
    ticker:
    - SCHD
    - SCHY
    step: 10 # 각 자산의 비율을 몇 % 단위로 나눌지 결정 (예: (100%, 0%),(90%, 10%), (80%, 20%), ...)
    start_year: 2010
    first_month: 1 # 1~12
    end_year: 2024
    last_month: 12 # 1~12
    ```  
2. `main.py`를 실행합니다.
3. 데이터 수집이 끝나면 `output.csv`파일이 생성되며, 엑셀 또는 구글 스프레드시트로 확인할 수 있습니다.