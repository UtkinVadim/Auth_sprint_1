--# создание пользователя admin
insert into user_auth (id, login, password, email)
values ('3b961301-4cae-427c-9991-5099e39733d4', 'admin',
        '853c0ad41acb039bbbca4e155a7c3b953933561262b9345f076009ff51149dc1', 'admin@admin');
--# Добавление ролей
insert into role (id, title)
values ('19b7b475-81ef-47fe-9c4c-96eb440c5382', 'admin');
insert into role (id, title)
values ('5d97840d-c934-447b-84f0-9b4e4863c0f2', 'subscriber');
--# add to admin role admin
insert into user_role (id, user_id, role_id)
values ('df529451-96c4-43da-9677-0226cbe56a03', '3b961301-4cae-427c-9991-5099e39733d4',
        '19b7b475-81ef-47fe-9c4c-96eb440c5382');
--# add to admin role admin
insert into user_role (id, user_id, role_id)
values ('af529451-96c4-43da-9677-0226cbe56a03', '3b961301-4cae-427c-9991-5099e39733d4',
        '5d97840d-c934-447b-84f0-9b4e4863c0f2');