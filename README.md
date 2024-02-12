# bm10_tasks
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeyVolkoff/switches.git
```

```
cd switches
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
На этот момент:
В директории ** start_gns_tests** перечислены основные тесты. Тесты проходят по ПМИ, основная информация о выполняемых тестах содержится в директории **my_module/tests_all**
