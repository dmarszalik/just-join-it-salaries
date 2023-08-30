Aby uruchomić serwer lokalny nalezy:
1. Uzywając terminala, przejść do katalogu do którego będzie pobierana aplikacja
2. Pobrać wszystkie pliki do pustego folderu:
        git clone https://github.com/dmarszalik/just-join-it-salaries.git
3. Utworzyć wirtualne środowisko:
        python -m venv venv
4. Aktywuj wirtualne środowisko:
        venv\Scripts\activate
5. pip install -r requirements.txt
6. python manage.py runserver
7. Otwórz przeglądarkę internetową i przejdź pod adres http://127.0.0.1:8000/