___
[Auth Api Sprint 1](https://github.com/UtkinVadim/Auth_sprint_1)
___

# Auth Api

Сервис для авторизации и аутентификации пользователей.

В сервисе реализованы апи для:
- Создания пользователей.
- Входа пользователей в систему, с последующим получением токенов.
- Выхода пользователей из системы с последующим удалением токенов.
- Выхода пользователей из системы на всех устройствах с последующим удалением всех токенов принадлежащих пользователю.
- Получения логов пользователя.

Для администрирования ролей пользователя реализованы апи:
- Создание/изменение/удаление/получение ролей.
- Назначение/удаление ролей пользователя.

Перед запуском тестов и приложения необходимо создать окружение командой `make env`.
### Запуск тестов
`make run_tests`

### Для управления ролями необходимо иметь доступ администратора. Создание нового юзера с ролью администратора:
Имя, почту и пароль администратора нужно задать в .env файле. Админ создастся автоматически при поднятии контейнера.

### Запуск сервиса
`make run_prod`
