# FastAPI 세미나 과제 4 — 3인 팀 프로젝트

본 과제에서는 세미나에서 다룬 내용에 대한 추가 조사 및 응용을 요구합니다.  
과제 수행 과정에서 적극적으로 공식 문서를 찾아보고, 질문해보시기를 권유드립니다.  


## 진행 방식과 필수 범위

- **3인 1조**로 와팡 서버를 구현합니다. 조별 저장소 하나에 협업한 결과를 제출합니다.
- **필수:** 회원·상점·상품·주문·리뷰의 API 21개, ERD, SQLAlchemy 모델, MySQL 마이그레이션.
- **선택:** 장바구니 모델과 API 4개. 필수 범위를 완성한 뒤 진행하며, 미구현해도 필수 과제 완료에 영향을 주지 않습니다.
- 인증·회원가입 등의 기존 코드는 출발점입니다. 제공 코드에도 명세에 맞게 보완해야 할 부분이 있으며, 처음부터 모든 테스트가 통과하는 완성본이 아닙니다.
- 배포는 이번 과제의 필수 범위에 포함하지 않습니다.

### 협업 방법

1. 구현 전에 세 명이 ERD와 모델 관계를 함께 합의합니다.
2. 기능별로 담당자가 모델·API·테스트 확인까지 맡습니다. 예시: A는 회원·상점, B는 상품·리뷰, C는 주문·내 주문 목록을 담당합니다. 내 리뷰 목록은 리뷰 담당자가 맡습니다.
3. 각자 기능 PR을 작성하고, 다른 팀원의 PR을 리뷰합니다. 각자 담당한 구현을 설명할 수 있어야 합니다.
4. 마이그레이션은 함께 통합하고, 마지막에는 상품 등록 → 주문 → 주문 조회 흐름을 검증합니다. 전체 기간의 마지막 20~30%는 통합과 수정에 남겨두는 것을 권장합니다.
5. 제출 시 README에 역할 분담과 각자의 구현·리뷰 PR 링크를 기록합니다.

### 실행 및 테스트

Python 3.12와 uv를 설치한 뒤 프로젝트 루트에서 진행합니다.

```bash
uv sync --frozen
# .env.local에 본인의 MySQL 접속 정보와 생성한 데이터베이스 이름 설정
uv run alembic upgrade head
uv run uvicorn wapang.main:app --reload
```

- API 기본 경로는 `/api`이며, 문서는 `http://127.0.0.1:8000/docs`에서 확인합니다.
- 새 모델을 작성한 뒤에는 아래 마이그레이션 안내에 따라 revision을 생성해야 합니다. 템플릿에는 완성된 마이그레이션이 없습니다.
- `.env.local`의 인증 키는 실습용 예시입니다. 실제 서비스의 비밀번호나 키를 커밋하지 마세요.

```bash
# 필수 테스트만 실행 (GitHub Actions도 동일한 범위)
ENV=test uv run pytest
# 선택 과제 테스트
ENV=test uv run pytest tests/carts
# 선택 과제를 포함한 전체 테스트
ENV=test uv run pytest tests
```

테스트는 메모리 SQLite를 사용합니다. 테스트 통과와 별도로 빈 MySQL 데이터베이스에 `alembic upgrade head`가 성공하고 서버가 실행되는지 확인해야 합니다.

## 과제 목표

- ER 다이어그램을 활용하여 도메인에 적합한 데이터베이스 모델을 설계할 수 있다.
- SQLAlchemy를 사용하여 데이터베이스를 다루고 API를 구현할 수 있다.
- 복잡한 비즈니스 로직을 포함한 실제 서비스와 유사한 API를 개발할 수 있다.

## 준비 사항

- 앞서 학습한 인증과 CRUD를 바탕으로 진행하며, 시작에 필요한 코드는 이 저장소에 제공합니다.

- 이번 과제는 `python 3.12` 버전을 기준으로 하며, `uv`를 이용해 패키지를 관리합니다.
	- `uv venv` 명령어로 가상환경을 생성하고,
	- `uv sync` 명령어로 `uv.lock` 파일에 기본 제공된 라이브러리를 설치해주세요.

- 이번 과제는 **서드파티 라이브러리 추가를 허용**합니다.
	- `pip install` 대신 `uv add`를 이용해 서드파티 라이브러리를 설치하시면 됩니다.
	- `uv add`를 이용해 설치하시면 `pyproject.toml` 파일과 `uv.lock` 파일의 내용이 수정되는데, **이 또한 함께 commit해주셔야 합니다**.
		- 그렇지 않으면 활용하신 라이브러리를 알 수 없어, 과제 채점에 차질이 생길 수 있습니다.

- `uv` 설치 및 사용에 관한 구체적인 내용은 [`uv` 공식문서](https://docs.astral.sh/uv/)를 참조하세요.

## 과제 요구 사항

### 개요
- 로켓배송으로 유명한 와팡의 서버를 개발합니다.
- SQLAlchemy를 사용하여 데이터베이스 모델을 설계하고 API를 구현합니다.  
- 제공된 스켈레톤 코드에 얽매일 필요는 없으며, 필요에 따라 파일, 함수 등을 추가 또는 제거하셔도 좋습니다.

### 1. 데이터베이스 모델 설계 (ER 다이어그램)
기획자로부터 다음과 같은 요구 사항을 전달받았습니다.  
주어진 요구 사항에 따라 데이터베이스 구조를 설계해봅시다.  
수업 시간에 소개했듯이 [www.erdcloud.com](www.erdcloud.com)를 통해서 ER 다이어그램을 그려볼 수 있습니다. 
완성된 ER 다이어그램은 **공개 상태**로 전환한 후 그 링크를 `erd_link.py`에 작성해주세요.

- 유저는 `id`, `email`, `hashed_password`, `nickname`, `address`, `phone_number` 을 가지고 있어야 합니다.
- 유저는 최대 하나의 상점만 소유할 수 있습니다.
- 상점은 `id`, `name`, `address`, `email`, `phone_number`, `delivery_fee` 를 가지고 있어야 합니다.
- 상점은 여러 개의 상품을 팔 수 있으며, 각각의 재고를 숫자로 관리합니다.
- 상품은 `id`, `name`, `price`, `stock`을 가지고 있어야 합니다.  
- 각 상품은 하나의 상점에 종속되는 것으로 합니다.  
- 유저는 여러 개의 주문을 할 수 있습니다.
- 주문은 `id`, `status`, `total_price`를 가지고 있어야 합니다.
- 주문의 `status` 속성은 진행 상태에 따라 `CANCELED`, `ORDERED`, `COMPLETE` 중 하나의 상태를 가집니다.
- 한 주문에는 여러 개의 상품이 포함될 수 있습니다.
- 유저는 상품마다 최대 한 개의 리뷰를 남길 수 있습니다.
- 리뷰는 `id`, `rating`, `comment` 를 가지고 있어야 합니다.
- 리뷰의 `rating` 속성은 1부터 5까지의 정수 값만 가질 수 있습니다.
- 상품은 여러 개의 리뷰를 가질 수 있습니다.
아래 모델 요구 사항은 **선택 과제(장바구니)** 에만 적용합니다.

- 유저는 장바구니를 하나 가지고 있습니다.
- 장바구니는 여러 개의 상품을 담을 수 있습니다.
- 장바구니에 담긴 상품의 수량을 숫자로 관리합니다.
- 한 상품은 여러 개의 장바구니에 담길 수 있습니다.

### 2. 데이터베이스 구조 작성 및 마이그레이션

과제 1에서 설계한 ER 다이어그램을 바탕으로 SQLAlchemy ORM 모델을 작성하고, 그 구조를 로컬 MySQL 데이터베이스에 반영(마이그레이션)해봅니다.  

#### SQLAlchemy ORM 작성
`./wapang/app/auth/models.py`와 `./wapang/app/users/models.py`에 SQLAlchemy ORM 모델의 예시가 제공되어 있습니다.
위 예시와 [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)를 탐구한 후 과제 1의 결과에 적합한 SQLAlchemy ORM 모델을 작성해보세요.  

#### alembic을 사용한 마이그레이션

##### 마이그레이션을 위한 환경 설정
마이그레이션에 필요한 환경 변수를 설정하기 위한 골격은 스켈레톤 코드에 함께 제공되었습니다.  
스켈레톤 코드와 [Pydantic Settings 공식 문서](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)를 탐구한 후 SQLAlchemy ORM 모델의 구조와 DB 구조를 연동하기 위한 환경 변수를 설정하세요.  
- 참고
	- 각자의 로컬 DB 환경에서 테스트하실 수 있도록 `.env.local` 파일을 수정하시면 됩니다.  
	- 수정하신 `.env.local` 파일을 commit하실 필요는 없습니다(사실 `.env` 파일을 git에 포함시키는 것은 권장되지 않습니다. 본 과제에서는 코드의 골격 제시를 위해 부득이하게 포함하였습니다).  
	- `.env.test`는 채점 시 사용되므로 **건드리지 말아주세요.**  
	- `.env.prod`는 추후 배포용 예시이며, 이번 과제에서는 설정하지 않아도 됩니다.
- 세 파일 중 실제 서버 가동에 사용될 파일을 결정하는 방법은 직접 탐구해보시기 바랍니다!  

##### 마이그레이션하기
- 힌트
	- `./wapang/database/alembic/env.py`에서 import문을 통해 SQLAlchemy ORM 모델들이 import되어야 합니다.
	- `uv run alembic revision --autogenerate -m "메시지 내용"` 명령어를 통해 마이그레이션을 위한 스크립트를 자동 생성할 수 있습니다.  
	- `uv run alembic upgrade head` 명령어를 통해 작성된 스크립트를 적용할 수 있습니다.  

### 3. API 구현

와팡의 회원가입 및 프로필 조회, 수정 API, 상점과 상품 관리 API를 구현해봅시다.  
데이터베이스를 사용하여 유저와 상점과 상품 정보를 저장하고, 조회할 수 있어야 합니다.
인증, 인가가 필요한 API에는 Authorization 헤더의 Bearer 토큰을 활용하며, 토큰 검증에는 제공된 인증 코드를 활용합니다.
로그인을 통한 토큰의 발급 로직은 스켈레톤 코드에 기본 제공되었습니다.

#### 1. `/api/users` 엔드포인트

##### 1-1) POST `/api/users` — 회원가입


- 사용자의 회원 가입 요청을 받아 검증 및 처리하며, 성공 시 데이터베이스에 저장합니다.
- 회원 가입 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- `email`과 `password`가 모두 있어야 합니다.
	- `email`: 이메일 형식이어야 합니다. 기존에 존재하는 회원과 중복되지 않는지 확인해야 합니다.
	- `password`: 8자 이상 20자 이하여야 합니다.
- 회원가입 성공 시 사용자 정보를 데이터베이스에 저장하며, 비밀번호는 argon2로 해싱하여 저장합니다.
- 각 사용자에게는 고유 식별자인 `id`(str)가 부여됩니다.

- **요청**
	- 본문 예시
		```json
		{
			"email": "waffle@example.com",
			"password": "password1234"
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 201
		- 본문: 생성된 사용자 정보 (비밀번호 제외)
		- 예시
		```json
		{
			"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
			"email": "waffle@example.com",
			"nickname": null,
			"address": null,
			"phone_number": null
		}
		```
	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|같은 이메일의 사용자가 이미 등록되어 있는 경우|409|ERR_004|EMAIL ALREADY EXISTS|
		- 예시  
			상태 코드 400과 함께 다음의 본문(application/json)이 반환됨.
			```json
			{
				"error_code": "ERR_002",
				"error_msg": "MISSING REQUIRED FIELDS"
			}
			```

##### 1-2) GET `/api/users/me` — 프로필 조회 (로그인 필요)

- 서버는 JWT 토큰을 통해 사용자의 신분 증명을 검증한 후, 사용자가 식별되면 해당 사용자의 정보를 응답 본문으로 보냅니다.
- 요청 헤더에 `Authorization: Bearer {access_token}` 형식으로 토큰이 포함되어야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 사용자 정보 (비밀번호 제외)
		- 예시
			```json
			{
				"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
				"email": "waffle@example.com",
				"nickname": "와플이",
				"address": "서울시 관악구",
				"phone_number": "010-1234-5678"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|

##### 1-3) PATCH `/api/users/me` — 프로필 수정 (로그인 필요)

- 로그인한 사용자의 프로필 정보를 수정합니다.
- 요청으로 들어온 각 필드는 다음의 방법에 따라 검증돼야 합니다. 또한 적어도 하나 이상의 필드가 포함되어야 합니다.
	- `nickname`: 20자 이하의 문자열이어야 합니다.
	- `address`: 100자 이하의 문자열이어야 합니다.
	- `phone_number`: 010-xxxx-xxxx 형식의 문자열이어야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- 본문 예시
		```json
		{
			"address": "서울시 강남구"
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 수정된 사용자 정보
		- 예시
			```json
			{
				"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
				"email": "newemail@example.com",
				"nickname": "와플이",
				"address": "서울시 강남구",
				"phone_number": "010-9876-5432"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|같은 이메일의 사용자가 이미 등록되어 있는 경우|409|ERR_004|EMAIL ALREADY EXISTS|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|

##### 1-4) GET `/api/users/me/orders` — 내 주문 목록 조회 (로그인 필요)

- 로그인한 사용자의 모든 주문 목록을 조회합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 주문 목록 배열
		- 예시
			```json
			[
				{
					"order_id": "a0debb7b-5854-4afd-8bd4-80fdffa21410",
					"total_price": 41000,
					"status": "ORDERED"
				},
				{
					"order_id": "b1f2cc8c-6965-5bge-9ce5-91geggb32521",
					"total_price": 25000,
					"status": "COMPLETE"
				}
			]
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|

##### 1-5) GET `/api/users/me/reviews` — 내 리뷰 목록 조회 (로그인 필요)

- 로그인한 사용자가 작성한 모든 리뷰 목록을 조회합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 리뷰 목록 배열
		- 예시
			```json
			[
				{
					"review_id": "rev123-uuid-4567-8901-234567890abc",
					"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
					"item_name": "와플",
					"comment": "맛있어요!",
					"rating": 5
				},
				{
					"review_id": "rev456-uuid-7890-1234-567890123def",
					"item_id": "789c1422-9063-46b9-b999-8bf4a4f8e28d",
					"item_name": "초콜릿",
					"comment": "달콤하고 좋네요.",
					"rating": 5
				}
			]
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|

#### 2. `/api/stores` 엔드포인트

##### 2-1) POST `/api/stores` — 상점 추가 (로그인 필요)

- 로그인한 사용자가 새로운 상점을 생성합니다. 한 사용자는 최대 하나의 상점만 소유할 수 있습니다.
- 상점 추가 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 필요한 필드가 모두 있어야 합니다.
	- `store_name`: 3글자 이상 20글자 이하의 문자열이어야 합니다. 기존에 존재하는 상점과 중복되지 않는지 확인해야 합니다.
	- `address`: 100자 이하의 문자열이어야 합니다.
	- `email`: 이메일 형식이어야 합니다. 기존에 존재하는 상점과 중복되지 않는지 확인해야 합니다.
	- `phone_number`: 010-xxxx-xxxx 형식의 문자열이어야 합니다. 기존에 존재하는 상점과 중복되지 않는지 확인해야 합니다.
	- `delivery_fee`: 0 이상의 정수이어야 합니다.
	- 로그인한 유저가 이미 상점을 생성한 경우, 상점을 추가할 수 없습니다.
- 각 상점에는 고유 식별자로 `id`(str)가 부여됩니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- 본문 예시
		```json
		{
			"store_name": "store1",
			"address": "address1",
			"email": "fastapi@wafflestudio.com",
			"phone_number": "010-1234-5678",
			"delivery_fee": 3000
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 201
		- 본문: 생성된 상점 정보
		- 예시
			```json
			{
				"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
				"store_name": "store1",
				"address": "address1",
				"email": "fastapi@wafflestudio.com",
				"phone_number": "010-1234-5678"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|이미 상점을 소유하고 있는 경우|409|ERR_008|STORE ALREADY EXISTS|
		|상점명/이메일/전화번호가 중복되는 경우|409|ERR_009|STORE INFO CONFLICT|

##### 2-2) PATCH `/api/stores/{store_id}` — 상점 정보 수정 (로그인 필요)

- 상점 소유자가 자신의 상점 정보를 수정합니다.
- 상점 수정 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 유저가 상점을 소유하고 있는지 확인해야 합니다.
	- 상점이 존재하는지 확인해야 합니다.
	- 유저가 소유한 상점인지 확인해야 합니다.
	- 요청 본문에 포함된 필드가 올바른지 확인해야 합니다. 또한 적어도 하나 이상의 필드가 포함되어야 합니다.
		- `store_name`: 3글자 이상 20글자 이하의 문자열이어야 합니다. 기존에 존재하는 상점과 중복되지 않는지 확인해야 합니다.
		- `address`: 100자 이하의 문자열이어야 합니다.
		- `email`: 이메일 형식이어야 합니다. 기존에 존재하는 상점과 중복되지 않는지 확인해야 합니다.
		- `phone_number`: 010-xxxx-xxxx 형식의 문자열이어야 합니다. 기존에 존재하는 상점과 중복되지 않는지 확인해야 합니다.
		- `delivery_fee`: 0 이상의 정수이어야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `store_id` (str)
	- 본문 예시
		```json
		{
			"delivery_fee": 5000
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 수정된 상점 정보
		- 예시
			```json
			{
				"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
				"store_name": "store1",
				"address": "address1",
				"email": "fastapi@wafflestudio.com",
				"phone_number": "010-1234-5678",
				"delivery_fee": 5000
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상점명/이메일/전화번호가 중복되는 경우|409|ERR_009|STORE INFO CONFLICT|
		|상점이 존재하지 않는 경우|404|ERR_010|STORE NOT FOUND|
		|상점을 소유하지 않은 경우|403|ERR_011|NO STORE OWNED|
		|다른 상점을 수정하려는 경우|403|ERR_012|NOT YOUR STORE|

##### 2-3) GET `/api/stores/{store_id}` — 상점 조회

- 지정된 ID의 상점 정보를 조회합니다.
- 상점 조회 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 상점이 존재하는지 확인해야 합니다.

- **요청**
	- URL 파라미터: `store_id` (str)

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 상점 정보
		- 예시
			```json
			{
				"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
				"store_name": "store1",
				"address": "address1",
				"email": "fastapi@wafflestudio.com",
				"phone_number": "010-1234-5678",
				"delivery_fee": 3000
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|상점이 존재하지 않는 경우|404|ERR_010|STORE NOT FOUND|

##### 2-4) GET `/api/stores/{store_id}/items` — 상점의 상품 목록 조회

- 특정 상점의 모든 상품을 조회합니다.

- **요청**
	- URL 파라미터: `store_id` (문자열)

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 상품 목록 배열
		- 예시
			```json
			[
				{
					"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
					"item_name": "와플",
					"price": 10000,
					"stock": 15
				},
				{
					"id": "a58a2711-9f60-42ea-89ed-ad91942b790a",
					"item_name": "시럽",
					"price": 3000,
					"stock": 8
				}
			]
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|상점이 존재하지 않는 경우|404|ERR_010|STORE NOT FOUND|

#### 3. `/api/items` 엔드포인트

##### 3-1) POST `/api/items` — 상품 추가 (로그인 필요)

- 상점 소유자가 자신의 상점에 새로운 상품을 추가합니다.
- 상품 추가 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 유저가 상점을 소유하고 있는지 확인해야 합니다.
	- 필요한 필드가 모두 있어야 합니다.
	- `item_name`: 2글자 이상 50글자 이하의 문자열이어야 합니다.
	- `price`: 0 이상의 정수이어야 합니다.
	- `stock`: 0 이상의 정수이어야 합니다.
- 각 상품에는 고유 식별자로 `id`(str)가 부여됩니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- 본문 예시
		```json
		{
			"item_name": "item1",
			"price": 10000,
			"stock": 10
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 201
		- 본문: 생성된 상품 정보
		- 예시
			```json
			{
				"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
				"item_name": "item1",
				"price": 10000,
				"stock": 10
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상점을 소유하지 않은 경우|403|ERR_011|NO STORE OWNED|

##### 3-2) PATCH `/api/items/{item_id}` — 상품 수정 (로그인 필요)

- 상점 소유자가 자신의 상점에 속한 상품의 정보를 수정합니다.
- 상품 수정 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 유저가 상점을 소유하고 있는지 확인해야 합니다.
	- 상품이 존재하는지 확인해야 합니다.
	- 유저가 소유한 상점의 상품인지 확인해야 합니다.
	- 요청 본문에 포함된 필드가 올바른지 확인해야 합니다. 또한 적어도 하나 이상의 필드가 포함되어야 합니다.
		- `item_name`: 2글자 이상 50글자 이하의 문자열이어야 합니다.
		- `price`: 0 이상의 정수이어야 합니다.
		- `stock`: 0 이상의 정수이어야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `item_id` (str)
	- 본문 예시
		```json
		{
			"item_name": "item1",
			"price": 15000,
			"stock": 10
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 수정된 상품 정보
		- 예시
			```json
			{
				"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
				"item_name": "item1",
				"price": 15000,
				"stock": 10
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상점을 소유하지 않은 경우|403|ERR_011|NO STORE OWNED|
		|상품이 존재하지 않는 경우|404|ERR_013|ITEM NOT FOUND|
		|다른 상점의 상품을 수정하려는 경우|403|ERR_014|NOT YOUR ITEM|

##### 3-3) GET `/api/items` — 상품 목록 조회

- 전체 상품 목록을 조회하며, 쿼리 파라미터를 통해 필터링이 가능합니다.
- 쿼리 파라미터를 이용해 다음과 같이 필터링해야 합니다.
	- `store_id`: 특정 상점의 상품만 조회할 때 사용합니다.
	- `min_price`: 지정된 최소 가격 이상의 상품을 조회할 때 사용합니다.
	- `max_price`: 지정된 최대 가격 이하의 상품을 조회할 때 사용합니다.
	- `in_stock`: 재고가 있는 상품만 조회할 때 사용합니다.
		- `true`로 설정할 경우, 재고가 있는 상품만 조회합니다.
		- `false`로 설정할 경우, 모든 상품을 조회합니다.
		- 기본값은 `false`입니다.
	- 모든 조건은 AND 조건입니다.

- **요청**
	- 쿼리 파라미터 (선택사항)
		- `store_id`: 상점 ID (문자열)
		- `min_price`: 최소 가격 (정수)
		- `max_price`: 최대 가격 (정수)
		- `in_stock`: 재고 여부 (boolean, 기본값: false)

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 상품 목록 배열
		- 예시
			```json
			[
				{
					"id": "6b5e1a9d-5f13-4cf0-b5f2-fde832c10534",
					"item_name": "item1",
					"price": 15000,
					"stock": 10,
					"store_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
					"store_name": "와플 스토어"
				},
				{
					"id": "a58a2711-9f60-42ea-89ed-ad91942b790a",
					"item_name": "item2",
					"price": 20000,
					"stock": 5,
					"store_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
					"store_name": "초콜릿 스토어"
				}
			]
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|지정된 상점이 존재하지 않는 경우|404|ERR_010|STORE NOT FOUND|

##### 3-4) DELETE `/api/items/{item_id}` — 상품 삭제 (로그인 필요)

- 로그인한 사용자가 자신의 상점의 상품을 삭제합니다. 재고를 0으로 만드는 것과 달리 상품을 완전히 삭제하여 목록에서 제거합니다.
- 상품이 삭제되어도 해당 상품에 작성된 리뷰는 독립적으로 유지되며 삭제되지 않습니다.
- 상품 삭제 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 상품이 존재하는지 확인해야 합니다.
	- 로그인한 사용자가 해당 상품의 상점 소유자인지 확인해야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `item_id` (문자열)

- **응답**
	- **성공 응답**
		- 상태 코드: 204
		- 본문: 없음

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상품이 존재하지 않는 경우|404|ERR_013|ITEM NOT FOUND|
		|상품의 소유자가 아닌 경우|403|ERR_014|NOT YOUR ITEM|

##### 3-5) POST `/api/items/{item_id}/reviews` — 리뷰 작성 (로그인 필요)

- 로그인한 사용자가 특정 상품에 대한 리뷰를 작성합니다. 한 사용자는 각 상품에 대해 최대 하나의 리뷰만 작성할 수 있습니다.
- 리뷰 작성 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 필요한 필드가 모두 있어야 합니다.
	- `rating`: 1 이상 5 이하의 정수이어야 합니다.
	- `comment`: 500자 이하의 문자열이어야 합니다.
	- 상품이 존재하는지 확인해야 합니다.
	- 사용자가 `nickname`을 설정했는지 확인해야 합니다. `nickname`이 없으면 리뷰를 작성할 수 없습니다.
	- 유저가 해당 상품에 대해 이미 리뷰를 작성한 경우, 리뷰를 추가할 수 없습니다.
- 각 리뷰에는 고유 식별자로 `id`(str)가 부여됩니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `item_id` (str)
	- 본문 예시
		```json
		{
			"rating": 5,
			"comment": "너무 좋아요!"
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 201
		- 본문: 생성된 리뷰 정보
		- 예시
			```json
			{
				"review_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
				"item_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
				"writer_nickname": "와플이",
				"is_writer": true,
				"rating": 5,
				"comment": "너무 좋아요!"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상품이 존재하지 않는 경우|404|ERR_013|ITEM NOT FOUND|
		|사용자가 nickname을 설정하지 않은 경우|422|ERR_015|NICKNAME NOT SET|
		|이미 해당 상품에 리뷰를 작성한 경우|409|ERR_016|REVIEW ALREADY EXISTS|

##### 3-6) GET `/api/items/{item_id}/reviews` — 상품 리뷰 조회 (로그인 선택)

- 특정 상품에 대한 모든 리뷰 목록을 조회합니다.
- 로그인한 경우 `is_writer` 필드가 포함되며, 비로그인 상태에서는 `is_writer` 필드가 생략됩니다.
- 상품 리뷰 조회 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 상품이 존재하는지 확인해야 합니다.

- **요청**
	- 헤더에 다음 필드가 선택적으로 포함될 수 있음
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `item_id` (정수)

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 리뷰 목록 배열
		- 로그인한 경우 예시
			```json
			[
				{
					"review_id": "10abb358-2815-4540-bcd4-5cc81f756b4d",
					"writer_nickname": "와플이",
					"is_writer": true,
					"rating": 5,
					"comment": "너무 좋아요!"
				},
				{
					"review_id": "eaefbdda-6db4-41f6-aef2-a9c87adbd03d",
					"writer_nickname": "초코",
					"is_writer": false,
					"rating": 4,
					"comment": "괜찮아요."
				}
			]
			```
		- 비로그인 상태 예시
			```json
			[
				{
					"review_id": "10abb358-2815-4540-bcd4-5cc81f756b4d",
					"writer_nickname": "와플이",
					"rating": 5,
					"comment": "너무 좋아요!"
				},
				{
					"review_id": "eaefbdda-6db4-41f6-aef2-a9c87adbd03d",
					"writer_nickname": "초코",
					"rating": 4,
					"comment": "괜찮아요."
				}
			]
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상품이 존재하지 않는 경우|404|ERR_013|ITEM NOT FOUND|

#### 4. `/api/orders` 엔드포인트

##### 4-1) POST `/api/orders` — 주문 생성 (로그인 필요)

- 로그인한 사용자가 여러 상품을 주문합니다. 주문 시 각 상품의 재고가 주문 수량만큼 감소합니다.
- 주문 생성 요청 시 다음의 사항이 검증돼야 합니다.
	- `items` 필드를 포함해야 합니다.
		- `items` 필드는 `item_id`와 `quantity`를 포함하는 배열이어야 합니다.
	- 수량은 1 이상의 정수이어야 합니다.
	- 각 상품이 존재하는지 확인해야 합니다.
	- 주문 수량이 재고보다 많지 않은지 확인해야 합니다.
- 각 주문에는 고유 식별자로 `id`(str)가 부여됩니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- 본문 예시
		```json
		{
			"items": [
				{
					"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
					"quantity": 2
				},
				{
					"item_id": "789c1422-9063-46b9-b999-8bf4a4f8e28d",
					"quantity": 1
				}
			]
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 201
		- 본문: 생성된 주문 정보
		- 예시
			```json
			{
				"order_id": "a0debb7b-5854-4afd-8bd4-80fdffa21410",
				"details": [
					{
						"store_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
						"store_name": "와플 스토어",
						"delivery_fee": 3000,
						"store_total_price": 23000,
						"items": [
							{
								"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
								"item_name": "와플",
								"price": 10000,
								"quantity": 2,
								"subtotal": 20000
							}
						]
					},
					{
						"store_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
						"store_name": "초콜릿 스토어",
						"delivery_fee": 2500,
						"store_total_price": 17500,
						"items": [
							{
								"item_id": "789c1422-9063-46b9-b999-8bf4a4f8e28d",
								"item_name": "초콜릿",
								"price": 15000,
								"quantity": 1,
								"subtotal": 15000
							}
						]
					}
				],
				"total_price": 40500,
				"status": "ORDERED"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상품이 존재하지 않는 경우|404|ERR_013|ITEM NOT FOUND|
		|재고가 부족한 경우|409|ERR_017|NOT ENOUGH STOCK|
		|items가 빈 배열인 경우|422|ERR_018|EMPTY ITEM LIST|


##### 4-2) GET `/api/orders/{order_id}` — 주문 조회 (로그인 필요)

- 로그인한 사용자가 자신의 주문 정보를 조회합니다.
- 주문 조회 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 주문이 존재하는지 확인해야 합니다.
	- 해당 주문이 로그인한 유저의 주문인지 확인해야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `order_id` (str)

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 주문 정보
		- 예시
			```json
			{
				"order_id": "a0debb7b-5854-4afd-8bd4-80fdffa21410",
				"details": [
					{
						"store_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
						"store_name": "와플 스토어",
						"delivery_fee": 3000,
						"store_total_price": 23000,
						"items": [
							{
								"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
								"item_name": "와플",
								"price": 10000,
								"quantity": 2,
								"subtotal": 20000
							}
						]
					},
					{
						"store_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
						"store_name": "초콜릿 스토어",
						"delivery_fee": 2500,
						"store_total_price": 17500,
						"items": [
							{
								"item_id": "789c1422-9063-46b9-b999-8bf4a4f8e28d",
								"item_name": "초콜릿",
								"price": 15000,
								"quantity": 1,
								"subtotal": 15000
							}
						]
					}
				],
				"total_price": 40500,
				"status": "ORDERED"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|주문이 존재하지 않는 경우|404|ERR_019|ORDER NOT FOUND|
		|다른 유저의 주문을 조회하려고 할 경우|403|ERR_020|NOT YOUR ORDER|


##### 4-3) PATCH `/api/orders/{order_id}` — 주문 상태 변경 (로그인 필요)

- 로그인한 사용자가 자신의 주문 상태를 변경합니다. 주문 취소 또는 구매 확정이 가능합니다.
- 주문 상태 변경 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 필요한 필드가 모두 있어야 합니다.
	- `status`: `CANCELED` 또는 `COMPLETE` 중 하나여야 합니다.
	- 주문이 존재하는지 확인해야 합니다.
	- 해당 주문이 로그인한 유저의 주문인지 확인해야 합니다.
	- 주문의 현재 상태가 `ORDERED`인지 확인해야 합니다. (이미 취소되었거나, 구매 확정된 주문은 변경할 수 없습니다.)

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `order_id` (문자열)
	- 본문 예시 (주문 취소)
		```json
		{
			"status": "CANCELED"
		}
		```
	- 본문 예시 (구매 확정)
		```json
		{
			"status": "COMPLETE"
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 204
		- 본문: 없음

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|주문이 존재하지 않는 경우|404|ERR_019|ORDER NOT FOUND|
		|이미 취소되었거나 완료된 주문을 변경하려고 할 경우|409|ERR_021|INVALID ORDER STATUS|
		|다른 유저의 주문을 변경하려고 할 경우|403|ERR_020|NOT YOUR ORDER|

#### 5. `/api/reviews` 엔드포인트

##### 5-1) GET `/api/reviews/{review_id}` — 리뷰 조회 (로그인 선택)

- 지정된 ID의 리뷰 정보를 조회합니다.
- 로그인한 경우 `is_writer` 필드가 포함되며, 비로그인 상태에서는 `is_writer` 필드가 생략됩니다.
- 리뷰 조회 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 리뷰가 존재하는지 확인해야 합니다.

- **요청**
	- 헤더에 다음 필드가 선택적으로 포함될 수 있음
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `review_id` (str)

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 리뷰 정보
		- 로그인한 경우 예시
			```json
			{
				"review_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
				"item_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
				"writer_nickname": "와플이",
				"is_writer": true,
				"rating": 5,
				"comment": "너무 좋아요!"
			}
			```
		- 비로그인 상태 예시
			```json
			{
				"review_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
				"item_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
				"writer_nickname": "와플이",
				"rating": 5,
				"comment": "너무 좋아요!"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|리뷰가 존재하지 않는 경우|404|ERR_022|REVIEW NOT FOUND|


##### 5-2) PATCH `/api/reviews/{review_id}` — 리뷰 수정 (로그인 필요)

- 로그인한 사용자가 자신이 작성한 리뷰를 수정합니다.
- 리뷰 수정 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 리뷰가 존재하는지 확인해야 합니다.
	- 해당 리뷰가 로그인한 유저의 리뷰인지 확인해야 합니다.
	- 요청 본문에 포함된 필드가 올바른지 확인해야 합니다. 또한 적어도 하나 이상의 필드가 포함되어야 합니다.
		- `rating`: 1 이상 5 이하의 정수이어야 합니다.
		- `comment`: 500자 이하의 문자열이어야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `review_id` (str)
	- 본문 예시
		```json
		{
			"rating": 4,
			"comment": "괜찮아요!"
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 수정된 리뷰 정보
		- 예시
			```json
			{
				"review_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
				"item_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
				"writer_nickname": "와플이",
				"is_writer": true,
				"rating": 4,
				"comment": "괜찮아요!"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|리뷰가 존재하지 않는 경우|404|ERR_022|REVIEW NOT FOUND|
		|다른 유저의 리뷰를 수정하려고 할 경우|403|ERR_023|NOT YOUR REVIEW|

##### 5-3) DELETE `/api/reviews/{review_id}` — 리뷰 삭제 (로그인 필요)

- 로그인한 사용자가 자신이 작성한 리뷰를 삭제합니다.
- 리뷰 삭제 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 리뷰가 존재하는지 확인해야 합니다.
	- 해당 리뷰가 로그인한 유저의 리뷰인지 확인해야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- URL 파라미터: `review_id` (str)

- **응답**
	- **성공 응답**
		- 상태 코드: 204
		- 본문: 없음

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|리뷰가 존재하지 않는 경우|404|ERR_022|REVIEW NOT FOUND|
		|다른 유저의 리뷰를 삭제하려고 할 경우|403|ERR_023|NOT YOUR REVIEW|

### 선택 과제: 장바구니

아래 4개 API와 관련 모델은 선택 구현입니다. 필수 21개 API 및 기본 테스트에는 포함되지 않습니다.

#### 6. `/api/carts` 엔드포인트  

##### 6-1) PATCH `/api/carts` — 장바구니 상품 추가/수정/삭제 (로그인 필요)

- 로그인한 사용자의 장바구니에 상품을 추가하거나 수정합니다. 이미 장바구니에 있는 상품의 경우 수량을 업데이트하고, 없는 상품의 경우 새로 추가합니다.
- `quantity`가 0인 경우 해당 상품을 장바구니에서 제거합니다.
- 응답에는 상점별로 그룹화된 `details` 배열이 포함되며, 각 상점에는 상점 정보(`store_id`, `store_name`), 배송비(`delivery_fee`), 해당 상점 총 결제금액(`store_total_price`), 그리고 상품 목록(`items`)이 포함됩니다. 전체 결제 금액은 `total_price`로 제공됩니다.
- 장바구니 상품 추가/수정/삭제 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 필요한 필드가 모두 있어야 합니다.
	- `item_id`: 존재하는 상품이어야 합니다.
	- `quantity`: 0 이상의 정수이어야 합니다. (0인 경우 해당 상품 삭제)

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```
	- 본문 예시 (상품 추가/수정)
		```json
		{
			"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
			"quantity": 2
		}
		```
	- 본문 예시 (상품 삭제)
		```json
		{
			"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
			"quantity": 0
		}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 업데이트된 장바구니 정보
		- 장바구니가 비어있는 경우 `details`는 빈 배열이고, `total_price`는 0으로 반환됩니다.
		- 예시
			```json
			{
				"details": [
					{
						"store_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
						"store_name": "와플 스토어",
						"delivery_fee": 3000,
						"store_total_price": 23000,
						"items": [
							{
								"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
								"item_name": "와플",
								"price": 10000,
								"quantity": 2,
								"subtotal": 20000
							}
						]
					}
				],
				"total_price": 23000
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|요청 필드가 비어있는 경우|400|ERR_002|MISSING REQUIRED FIELDS|
		|요청 필드의 형식이 올바르지 않은 경우|400|ERR_003|INVALID FIELD FORMAT|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|상품이 존재하지 않는 경우|404|ERR_013|ITEM NOT FOUND|

##### 6-2) GET `/api/carts` — 장바구니 조회 (로그인 필요)

- 로그인한 사용자의 장바구니 내용을 조회합니다.
- 응답에는 상점별로 그룹화된 `details` 배열이 포함되며, 각 상점에는 상점 정보(`store_id`, `store_name`), 배송비(`delivery_fee`), 해당 상점 총 결제금액(`store_total_price`), 그리고 상품 목록(`items`)이 포함됩니다. 전체 결제 금액은 `total_price`로 제공됩니다.
- 빈 장바구니인 경우 `details`는 빈 배열이고, `total_price`는 0으로 반환됩니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 200
		- 본문: 장바구니 정보
		- 예시
			```json
			{
				"details": [
					{
						"store_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
						"store_name": "와플 스토어",
						"delivery_fee": 3000,
						"store_total_price": 23000,
						"items": [
							{
								"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
								"item_name": "와플",
								"price": 10000,
								"quantity": 2,
								"subtotal": 20000
							}
						]
					},
					{
						"store_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
						"store_name": "초콜릿 스토어",
						"delivery_fee": 3000,
						"store_total_price": 18000,
						"items": [
							{
								"item_id": "789c1422-9063-46b9-b999-8bf4a4f8e28d",
								"item_name": "초콜릿",
								"price": 15000,
								"quantity": 1,
								"subtotal": 15000
							}
						]
					}
				],
				"total_price": 41000
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|

##### 6-3) DELETE `/api/carts` — 장바구니 전체 비우기 (로그인 필요)

- 장바구니의 모든 상품을 제거합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 204
		- 본문: 없음

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|

##### 6-4) POST `/api/carts/checkout` — 장바구니에서 주문 생성 (로그인 필요)

- 현재 장바구니의 모든 상품으로 주문을 생성하고 장바구니를 비웁니다.
- 주문 생성 요청이 들어오면 다음의 사항이 검증돼야 합니다.
	- 장바구니가 비어있지 않은지 확인해야 합니다.
	- 모든 상품의 재고가 충분한지 확인해야 합니다.

- **요청**
	- 헤더에 다음 필드가 포함됨
		```
		Authorization: Bearer {access_token}
		```

- **응답**
	- **성공 응답**
		- 상태 코드: 201
		- 본문: 생성된 주문 정보
		- 예시
			```json
			{
				"order_id": "a0debb7b-5854-4afd-8bd4-80fdffa21410",
				"details": [
					{
						"store_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
						"store_name": "와플 스토어",
						"delivery_fee": 3000,
						"store_total_price": 23000,
						"items": [
							{
								"item_id": "4a40d8f9-6d90-4189-8f93-de0d4a89d6cf",
								"item_name": "와플",
								"price": 10000,
								"quantity": 2,
								"subtotal": 20000
							}
						]
					},
					{
						"store_id": "b8e7f3a2-1c4d-5e6f-9012-345678901234",
						"store_name": "초콜릿 스토어",
						"delivery_fee": 3000,
						"store_total_price": 18000,
						"items": [
							{
								"item_id": "789c1422-9063-46b9-b999-8bf4a4f8e28d",
								"item_name": "초콜릿",
								"price": 15000,
								"quantity": 1,
								"subtotal": 15000
							}
						]
					}
				],
				"total_price": 41000,
				"status": "ORDERED"
			}
			```

	- **실패 응답**
		|상황|상태 코드|ERROR_CODE|ERROR_MSG|
		|---|---|---|---|
		|Authorization 헤더가 제시되지 않은 경우|401|ERR_005|UNAUTHENTICATED|
		|Authorization 헤더 값의 형식이 비정상적인 경우|400|ERR_006|BAD AUTHORIZATION HEADER|
		|토큰이 유효하지 않은 경우|401|ERR_007|INVALID TOKEN|
		|재고가 부족한 경우|409|ERR_017|NOT ENOUGH STOCK|
		|장바구니가 비어있는 경우|422|ERR_024|EMPTY ITEM LIST|

## 제출 방법

### 1번 과제
- [ERDCloud](www.erdcloud.com)에서 그린 ER 다이어그램을 **공개 상태**로 전환한 후 그 링크를 `erd_link.py`에 작성해주세요.

### 2번 과제
- 프로젝트 루트 디렉토리에서 `uv run alembic upgrade head` 명령어를 실행했을 때 DB 스키마가 반영될 수 있도록 `wapang/database/alembic/versions` 디렉토리에 마이그레이션 스크립트가 존재하는 상태여야 합니다.

### 3번 과제
- 완성된 코드는 프로젝트 루트 디렉토리에서 `uv run uvicorn wapang.main:app` 명령어 실행으로 서버가 가동되어야 하며, 필수 테스트(`ENV=test uv run pytest`)를 모두 통과해야 합니다. 장바구니 테스트는 선택 과제를 구현한 경우에만 확인합니다.

- 팀원이 모두 조별 저장소에 접근할 수 있는지 확인하고, 제출 시 저장소 링크·공개 ERD 링크·역할 분담·구현 및 리뷰 PR 링크를 함께 제출합니다.

## 원본

이 과제는 [2025 FastAPI 세미나 과제 3 템플릿](https://github.com/wafflestudio-2025-fastapi-seminar/assignment-3-template)을 기반으로 3인 팀 과제로 조정했습니다.
