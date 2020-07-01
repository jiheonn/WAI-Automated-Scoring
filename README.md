# WA3I PROJECT

## Project Objective
- 학생과 선생님을 위한 AI 서술형 채점 시스템 개발

## Docker run command
- 처음 개발용 서버를 docker로 구성하기 위하여 아래와 같은 명령어를 입력한다.
```bash
docker-compose up --build web db
```
- docker build가 종료되면 새로운 `선생님` 계정을 가입하여 테스트를 실시한다. 

## Project rules
- Commit는 최소기능 단위를 쪼개서 하나의 commit 으로 `squash`한후 `PR`한다.
- 하나의 기능 단위는 ISSUE로 생성되면 PR을 통해 하나이상의 ISSUE를 제거한다.


## Development Environment

- 가상환경 python 버전 3.7.3
- 가상환경 설치 파일 저장 방법
  - pip freeze > requirements.txt
- 가상환경 파일로 설치 방법
  - pip install -r requirements.txt
