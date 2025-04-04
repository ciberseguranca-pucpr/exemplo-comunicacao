CREATE DATABASE projeto;

USE projeto;

CREATE TABLE tb_tarefas (
    id int not null primary key,
    nome varchar(100) not null,
    is_completa boolean not null default 0,
    criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
