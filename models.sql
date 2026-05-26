create table users (
    id serial primary key, 
    name varchar unique, 
    age int,
    birthday date,
    is_admin bool default false,
    balance float default 0,
    created_at timestamp default now(),
    created_at_tz timestamptz default now()
);
create table cities (
    id serial primary key,
    name varchar unique,
    created_at timestamp default now(),
    created_at_tz timestamptz default now()
);
