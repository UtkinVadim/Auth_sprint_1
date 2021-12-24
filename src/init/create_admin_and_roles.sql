--# создание пользователя admin
insert into user_auth (id, login, password, email)
values ('c2c9b28d-2cd9-4bd4-8cd3-e0f7586055aa', 'admin',
        '57f044e80a3c2ae48efb66224a65d7b1bb29a7360a7327f5cbafe34dfdac0338', 'admin@admin');
--# Добавление ролей
insert into role (id, title)
values ('5d97840d-c934-447b-84f0-9b4e4863c0f2', 'subscriber'),
       ('8d6f1fd7-ed3c-4b2e-ad45-c917dc08fdaf', 'some_role'),
       ('19b7b475-81ef-47fe-9c4c-96eb440c5382', 'admin');
--# add to admin roles admin and subsriber
insert into user_role (id, user_id, role_id)
values ('df529451-96c4-43da-9677-0226cbe56a03', 'c2c9b28d-2cd9-4bd4-8cd3-e0f7586055aa',
        '19b7b475-81ef-47fe-9c4c-96eb440c5382'),
       ('af529451-96c4-43da-9677-0226cbe56a03', 'c2c9b28d-2cd9-4bd4-8cd3-e0f7586055aa',
        '5d97840d-c934-447b-84f0-9b4e4863c0f2');
