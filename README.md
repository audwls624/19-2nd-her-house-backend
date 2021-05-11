# 오늘의 집
house of the day Clone Project

## ⚡️ Backend
- [양명진]
- [김영훈]
- [함경재](https://github.com/hiyee-gj)

## 🐝 Period
- 2021.04.26 ~ 2021.05.07

## 🐍 Skill
- Django
- MySQL
- S3
- kakao API
- AWS EC2
- AWS RDS
- docker
- jenkins

## 💡 Implement Function
### 소셜로그인
- kakao api 사용해서 로그인
### 지도 API
- 유저 주소 정보를 url에 결합시키기
- url을 나눠서 필요한 정보를 추출하고, headers에 API_KEY 담아서 요청하기
- response 값에서 원하는 정보들 추출하기
### 업체 리스트 페이지
- query parameter로 위치 정보 받아오기
- 받아온 위치 정보로 kakao API와 통신해서 원하는 정보 추출하기
- 받아온 정보와 company 정보를 통해서 response 값 만들기
### 상품 리스트 페이지
- query parameter로 필터 값 받아오기
- 빈 Q를 사용해서 필터링
### 상품 상세 페이지
- list comprehension과 prefetch_related, select_related를 통해서 상세 페이지 구현
### 상품 리뷰 
- AWS S3에 업로드하고 url 데이터베이스 저장하기
