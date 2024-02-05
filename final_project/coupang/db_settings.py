DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # 엔진
        "NAME": "final_project_DM",  # 데이터베이스 이름
        "USER": "bigDM",  # 사용자
        "PASSWORD": "bigDM1234@",  # 비밀번호
        "HOST": "localhost",  # 호스트
        "PORT": "3306",  # 포트번호
    }
}

# SECRET_KEY
# settings.py에서 복사하고 SECRET_KEY 주석 처리
# DATABASES 주석 처리
SECRET_KEY = "django-insecure-(2!m(8qh#m@d+ir6p+=gv336s!01(*&1ead3s1nya*y8(l#8$_"