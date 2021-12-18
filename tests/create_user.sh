LOGIN=`head /dev/urandom |LC_ALL=C  tr -dc A-Za-z0-9 | head -c10`
echo ${LOGIN}

USER_INFO="{\"login\": \"${LOGIN}\", \"email\": \"test@test\", \"password\": \"password\"}"
echo ${USER_INFO}

curl http://127.0.0.1:5000/api/v1/user/sign_up -XPOST -d "${USER_INFO}" -H 'Content-Type: application/json'
