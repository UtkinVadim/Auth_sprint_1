LOGIN=$(head /dev/urandom |LC_ALL=C  tr -dc A-Za-z0-9 | head -c10)
echo ${LOGIN}

USER_CREATE_INFO="{\"login\": \"${LOGIN}\", \"email\": \"test@test\", \"password\": \"password\"}"
echo ${USER_CREATE_INFO}
USER_LOGIN_INFO="{\"login\": \"${LOGIN}\", \"email\": \"test@test\", \"password\": \"password\"}"
echo ${USER_LOGIN_INFO}

echo 'trying to create user'
curl http://127.0.0.1:5000/api/v1/user/sign_up -XPOST -d "${USER_CREATE_INFO}" -H 'Content-Type: application/json'
echo 'trying to sign_in'
curl http://127.0.0.1:5000/api/v1/user/sign_in -XPOST -d "${USER_LOGIN_INFO}" -H 'Content-Type: application/json'
echo 'trying to sign_in (wrong login)'
curl http://127.0.0.1:5000/api/v1/user/sign_in -XPOST -d '{"login": "*", "password": "*"}' -H 'Content-Type: application/json'
