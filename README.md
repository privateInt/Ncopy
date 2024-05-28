# 프로젝트 목적

- 사용자 입력값(상품, 키워드, 톤앤매너, 연령, 성별)을 LLM API(naver hyper clova)에 전달하여 해당 광고 카피 생성

# 실험 내용

## model

- naver hyper clova API인 HCX-003, HCX-DASH-001 모델을 비교 분석함
- 분석 결과 HCX-003의 비용, 추론 속도 등은 HCX-DASH-001에 비해 부족했지만, 감당 가능한 수준이었음
- 분석 결과 HCX-DASH-001은 톤앤매너의 분위기 이해 등 품질면에서 부족한 수준이었음
- HCX-003 모델 결정

## parameter

- 품질에 영향을 미치는 parameter의 수치를 변화하는 방식으로 parameter의 영향 파악
- temperature 0.5 결정

## prompt engineering

- persona 부여, 정확한 작업 지시, 순차적 작업 지시, 예시 첨부 등 prompt engineering 진행
- 실험을 통해 예시에 따라 품질이 향상되는 것을 확인 => 예시의 길이, 분위기 등 세부적인 내용까지 구분하여 작성
- 예시를 톤앤매너에 따라 세분화 해도 품질 저하가 없음을 확인 => 예시를 톤앤매너 별로 작성하여 톤앤매너의 분위기 세분화, 토큰 사용량 감소
- 톤앤매너라는 표현이 생소할 수 있으므로 톤앤매너의 정의 입력

# 환경 설치

```sh
pip install -r requirements.txt
```

# 데모 페이지 실행

```sh
streamlit run Ncopy_test_demo.py
```

# 데모 페이지 예시

![Cap 2024-05-28 15-24-50-259](https://github.com/privateInt/Ncopy/assets/95892797/95678ae2-8006-4bd0-ab37-3c088c40c0f2)

![Cap 2024-05-28 15-24-59-237](https://github.com/privateInt/Ncopy/assets/95892797/d046cd81-61b1-4048-bd84-b053a8397e1f)

![Cap 2024-05-28 15-25-12-083](https://github.com/privateInt/Ncopy/assets/95892797/54de0e8f-cd38-4af9-84ba-80e1bce1b4c0)

![Cap 2024-05-28 15-25-18-634](https://github.com/privateInt/Ncopy/assets/95892797/bedeabbe-703c-4cea-9151-2b64be278944)

