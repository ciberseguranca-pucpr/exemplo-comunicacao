CREATE DATABASE projeto;

USE projeto;

CREATE TABLE tb_tarefa (
    id int primary key auto_increment,
    nome varchar(100) not null unique,
    is_completa boolean not null default 0,
    criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
