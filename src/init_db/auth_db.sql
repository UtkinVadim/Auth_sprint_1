CREATE TABLE "authapi.users_private_info"
(
    "id"         TEXT         NOT NULL,
    "user_id"    TEXT         NOT NULL UNIQUE,
    "login"      varchar(255) NOT NULL UNIQUE,
    "password"   varchar(255) NOT NULL UNIQUE,
    "email"      varchar(255),
    "first name" varchar(255),
    "last name"  varchar(255),
    CONSTRAINT "users_private_info_pk" PRIMARY KEY ("id")
);



CREATE TABLE "authapi.users"
(
    "id"              serial   NOT NULL,
    "is_active"       BINARY   NOT NULL,
    "role_id"         TEXT[] NOT NULL,
    "last_login_date" DATETIME NOT NULL,
    CONSTRAINT "users_pk" PRIMARY KEY ("id")
);



CREATE TABLE "authapi.roles"
(
    "id"    TEXT NOT NULL,
    "title" TEXT NOT NULL,
    CONSTRAINT "roles_pk" PRIMARY KEY ("id")
);



CREATE TABLE "authapi.login_history"
(
    "id"          TEXT     NOT NULL,
    "user_id"     TEXT     NOT NULL,
    "fingerprint" TEXT     NOT NULL,
    "event_date"  DATETIME NOT NULL,
    CONSTRAINT "login_history_pk" PRIMARY KEY ("id")
);



ALTER TABLE "users_private_info"
    ADD CONSTRAINT "users_private_info_fk0" FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "users"
    ADD CONSTRAINT "users_fk0" FOREIGN KEY ("role_id") REFERENCES "roles" ("id");


ALTER TABLE "login_history"
    ADD CONSTRAINT "login_history_fk0" FOREIGN KEY ("user_id") REFERENCES "users" ("id");




