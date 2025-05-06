
# 🛍️ Naver SmartStore Review Crawler

이 프로젝트는 [네이버 스마트스토어](https://smartstore.naver.com) 특정 상품 페이지에서 리뷰 데이터를 크롤링하여 `.csv` 파일로 저장하는 Python 스크립트입니다.

---

## 📌 기능 요약

- 특정 스마트스토어 상품의 리뷰 크롤링
- 최근 특정 기간(설정 가능) 이내의 리뷰만 수집
- 작성일, 상품 옵션명, 리뷰 본문을 수집
- `navershopping_review_data.csv`로 저장

---

## 💻 실행 환경

- Python 3.8 이상
- Google Chrome (버전 136 권장)
- ChromeDriver (Chrome 버전에 맞는 버전 필요)

---

## 📦 필수 패키지 설치

```bash
pip install -r requirements.txt
```

`requirements.txt` 예시:

```txt
requests==2.31.0
beautifulsoup4==4.12.3
pandas==2.2.2
selenium==4.20.0
webdriver-manager==4.0.1
```

> ⚠️ 현재는 로컬에 있는 `chromedriver.exe`를 직접 지정하여 사용합니다. 자동 설치를 원할 경우 `webdriver-manager` 설정을 수정하세요.

---

## ⚙️ 사용 방법

1. **크롬 드라이버 경로 설정**  
   `chrome_driver_path` 변수에 크롬드라이버 실행파일 경로를 입력하세요.

2. **크롤링할 상품 페이지 지정**  
   아래 코드 부분의 상품 URL을 원하는 것으로 변경하세요.

   ```python
   driver.get('URL')
   ```

3. **스크립트 실행**

   ```bash
   python crwaling.py
   ```

---

## 📄 저장 결과 예시 (`navershopping_review_data.csv`)

| RD_ITEM_NM       | RD_CONTENT                                      | RD_WRITE_DT |
|------------------|-------------------------------------------------|-------------|
| 레몬밤차 1g x 30 | 건강을 생각해서 주문했는데 맛도 깔끔하고 좋아요 | 20240503    |
| 도라지차 2g x 20 | 따뜻하게 마시기 좋고 재구매 의사 있어요         | 20240421    |

---

## 🛠️ 주요 처리 흐름

1. 상품 페이지 진입 → 리뷰 탭 클릭
2. 리뷰 목록 HTML 파싱 (BeautifulSoup)
3. 작성일, 상품 옵션, 리뷰 내용 추출
4. 다음 페이지 버튼 클릭 (동적 페이지 탐색)
5. 1년 이전 리뷰가 나오면 종료
6. `.csv`로 저장

---

## 🔍 참고 사항

- 동작 중 리뷰 구조나 클래스명이 바뀌면 크롤링이 실패할 수 있습니다.
- 크롬 브라우저 버전과 크롬드라이버는 반드시 일치해야 합니다.
- 셀레니움 페이지 로딩이 느릴 경우 `time.sleep()`을 늘려주세요.

---

## 📬 문의

버그 신고나 개선 요청은 Issues로 남겨주세요.
