LOGIN=$(head /dev/urandom |LC_ALL=C  tr -dc A-Za-z0-9 | head -c10)
echo ${LOGIN}

USER_CREATE_INFO="{\"login\": \"${LOGIN}\", \"email\": \"test@test\", \"password\": \"password\"}"
echo ${USER_CREATE_INFO}
USER_LOGIN_INFO="{\"login\": \"${LOGIN}\", \"email\": \"test@test\", \"password\": \"password\"}"
echo ${USER_LOGIN_INFO}
ROLE="{\"title\": \"${LOGIN}\"}"
ROLE_UPDATE="{\"title\": \"${LOGIN}\", \"new_title\": \"delme_plz1\"}"


echo '***'
echo 'trying to create user'
curl http://127.0.0.1:5000/api/v1/user/sign_up -XPOST -d "${USER_CREATE_INFO}" -H 'Content-Type: application/json'
echo '***'
echo 'trying to sign_in'
TOKEN=$(curl http://127.0.0.1:5000/api/v1/user/sign_in -XPOST -d "${USER_LOGIN_INFO}" -H 'Content-Type: application/json' | tr '{":"}' '\n' | grep -v access_token | grep -ve '^$' | head -1)
echo ${TOKEN}


echo '***'
echo 'trying to sign_in (wrong login)'
curl http://127.0.0.1:5000/api/v1/user/sign_in -XPOST -d '{"login": "*", "password": "*"}' -H 'Content-Type: application/json'
echo '***'
echo 'create role'
curl http://127.0.0.1:5000/api/v1/access/role -XPOST -d "${ROLE}" -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'create role (exists)'
curl http://127.0.0.1:5000/api/v1/access/role -XPOST -d "${ROLE}" -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'get all roles'
curl http://127.0.0.1:5000/api/v1/access/role -XGET -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'update role'
curl http://127.0.0.1:5000/api/v1/access/role -XPATCH -d "${ROLE_UPDATE}" -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'get all roles'
curl http://127.0.0.1:5000/api/v1/access/role -XGET -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'delete role'
curl http://127.0.0.1:5000/api/v1/access/role -XDELETE -d '{"title": "delme_plz1"}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'get all roles'
curl http://127.0.0.1:5000/api/v1/access/role -XGET -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'
echo 'get history'
curl http://127.0.0.1:5000/api/v1/user/history -XGET -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}"
echo '***'

# Это нужно добавить до инициации алембика
# create database movies_auth;
# \c movies_auth;
#не нужно#  create schema content;

# тут инициация алембика

# Это нужно будет добавить в скрипты подъёма базы
# movies_auth=# insert into role (id, title) values ('19b7b475-81ef-47fe-9c4c-96eb440c5382', 'admin');
# movies_auth=# insert into role (id, title) values ('5d97840d-c934-447b-84f0-9b4e4863c0f2', 'subscriber');