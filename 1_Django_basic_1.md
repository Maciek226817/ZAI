# Zaawansowane aplikacje internetowe

## Uwagi wstępne dotyczące aplikacji

Do wykonania poniższych zadań niezbędne jest posiadanie zainstalowanego w systemie programu *Python* i pakietu *Django*. Sprawdzamy, czy mamy zainstalowany program *Python*:

<font size="2">

```python
D:\ZAI\PROJEKTY\NSTC000000>python --version
# Python 3.11.0
```

</font>

Uzyskany wynik oznacza, że mamy zainstalowany w systemie program *Python* w wersji 3.11.0. Sprawdzamy, czy mamy zainstalowany w systemie pakiet *Django*:

<font size="2">

```python
D:\ZAI\PROJEKTY\NSTC000000>django-admin --version
# 'django-admin' is not recognized as an internal or external command,
#  operable program or batch file.
```

</font>

Uzyskany wynik oznacza, że nie mamy zainstalowanego w systemie pakietu *Django*.

## Tworzenie środowiska wirtualnego i instalacja niezbędnych pakietów

<font size="2">

```python
# Tworzenie środowiska wirtualnego
D:\ZAI\PROJEKTY\NSTC000000>python -m venv env

# Aktywacja środowiska wirtualnego:
D:\ZAI\PROJEKTY\NSTC000000>env\Scripts\activate
(env) D:\ZAI\PROJEKTY\NSTC000000>
# (env) widoczne na początku znaku zachęty oznacza, że środowisko wirtualne zostało aktywowane

# instalacja pakietu Django
(env) D:\ZAI\PROJEKTY\NSTC000000>pip install django

# Sprawdzenie, czy mamy już Django (w środowisku wirtualnym)
(env) D:\ZAI\PROJEKTY\NSTC000000>django-admin --version
# 4.2
#
# Uzyskany wynik oznacza, że w środowisku wirtualnym mamy zainstalowaną wersję 4.2 pakietu Django.

```

</font>

## Tworzenie projektu i aplikacji

W poniższych poleceniach *filmweb* oznacza nazwę projektu, zaś *filmy* to nazwa aplikacji.

<font size="2">

```python
# Proszę zwrócić uwagę na kropkę na końcu pierwszego polecenia:
(env) D:\ZAI\PROJEKTY\NSTC000000>django-admin startproject filmweb .
(env) D:\ZAI\PROJEKTY\NSTC000000>django-admin startapp filmy      
```

</font>

W wyniku wydania widocznych wyżej poleceń uzyskaliśmy następującą strukturę katalogów i plików projektu *filmweb*

<details>

<summary>Struktura projektu <b>filmweb</b> i aplikacji <b>filmy</b></summary>

<font size="2">

```python

# Nazwy katalogów podano dużymi literami
# Nazwy plików podano małymi literami

D:\ZAI\PROJEKTY\NSTC000000

ENV
FILMWEB             # Nazwa projektu; 
    asgi.py         # punkt dostępowy do asynchronicznych swerwerów www, obsługujących projekt
    settings.py     # plik konfiguracyjny projektu
    urls.py         # plik zawierający listę adresów URL projektu i aplikacji
    wsgi.py         # punkt dostępowy do serwerów www, obsługujących projekt
FILMY
    MIGRATIONS
    admin.py
    apps.py
    models.py
    urls.py         # plik z adresami URL wskazującymi na kolejne widoki z pliku 'views.py'
    tests.py
    views.py        # cokolwiek z aplikacji chcesz zobaczyć w przeglądarce, musisz napisać to w tym pliku 
db.sqlite3          # plik bazy danych (powstał w wyniku przeprowadzonej migracji wstępnej)
manage.py           # uruchamiany w linii poleceń plik pozwalający na wykonywanie szeregu zadań związanych z projektem
```

</font>

</details>

<br>

Ustawienie języka i strefy czasowej w pliku *filmweb/settings.py*

<br>

<font size="2">

```python
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'pl'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Warsaw'
```

</font>

<br>

## Konfiguracja bazy danych

<br>

<font size="2">

```python
(env) D:\ZAI\PROJEKTY\NSTC000000>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:                                        
  ( ... ) ... OK                     

(env) D:\ZAI\PROJEKTY\NSTC000000>     
```

</font>

<br>

## Tworzenie superużytkownika

Użytkownik utworzony tutaj będzie miał prawa administratora aplikacji.

<font size="2">

```python
(env) D:\ZAI\PROJEKTY\NSTC000000>python manage.py createsuperuser --username admin --email admin@example.com
Password: admin
Password (again): admin
Hasło jest zbyt podobne do nazwa użytkownika.
To hasło jest za krótkie. Musi zawierać co najmniej 8 znaków.
To hasło jest zbyt powszechne.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

(env) D:\ZAI\PROJEKTY\NSTC000000>

```

</font>

<br>

## Wbudowany serwer www

(nie używać w zastosowaniach produkcyjnych)

Poniższe polecenie uruchomi wbudowany serwer www, nasłuchujący na 127.0.0.1:8000<br>
Bardziej szczegółowe informacje dotyczące tego serwera dostępne są 
 <a href="https://docs.djangoproject.com/en/4.2/intro/tutorial01/#the-development-server" target="_blank">tutaj</a> 

<font size="2">

```python
(env) D:\ZAI\PROJEKTY\NSTC000000>python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
( ... )
Django version 4.2, using settings 'filmweb.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

</font>

Uruchomienie serwera umożliwi dostęp do naszej aplikacji poprzez przeglądarkę internetową.

<br>

## Tworzenie pierwszych widoków

<br>

<details>

<summary>Zawartość pliku <b>filmy/views.py</b></summary>

<font size="2">

```python
from django.http import HttpResponse


def wszystkie(request):
    return HttpResponse("<h1>Tu będzie wyświetlana lista filmów z bazy danych.</h1>")

def szczegoly(request):
    return HttpResponse("<h1>Tu będą wyświetlane szczególy wybranego filmu.</h1>")
```

</font>

</details>

<br>

## Konfiguracja adresów URL

*Uniform Resource Locator (URL)*, potocznie zwany adresem internetowym kieruje klienta (przeglądarkę internetową) do określonego zasobu udostępnionego w sieci. Adres naszego serwera (adres hosta) to 127.0.0.1:8000. Nasza aplikacja udostępnia zasoby poprzez kolejne widoki tworzone w pliku *filmy/views.py*. W plikach *filmweb/urls.py* i *filmy/urls.py* znajdują się adresy URL kierujące klienta do udostępnianych w pliku *filmy/views.py* widoków.<br>

![""](.\1_urls.jpg)












