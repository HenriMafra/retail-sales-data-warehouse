-- RODE ESTA QUERY NO PGADMIN, CONECTADO AO BANCO postgres.
-- Ela cria um banco vazio para fazer tudo do zero por codigo SQL.

DROP DATABASE IF EXISTS coffee_shop_dw_codigo;

CREATE DATABASE coffee_shop_dw_codigo
  WITH
  ENCODING = 'UTF8'
  TEMPLATE = template0;
