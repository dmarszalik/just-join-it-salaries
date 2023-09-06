import multiprocessing
from whitenoise import WhiteNoise

application = WhiteNoise(application, root=STATIC_ROOT)


# Adres i port, na którym ma działać Gunicorn
bind = "0.0.0.0:8000"

# Liczba workerów (procesów) do obsługi żądań HTTP
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)


# Ustawienia dostępne do modyfikacji
# user = "username"
# group = "groupname"
# accesslog = "/path/to/access/log/file"
# errorlog = "/path/to/error/log/file"
static_path = '/staticfiles'