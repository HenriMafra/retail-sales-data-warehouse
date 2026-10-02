-- Execute este script conectado ao banco postgres:
-- psql -U postgres -d postgres -f sql/00_create_database.sql

DROP DATABASE IF EXISTS coffee_shop_dw;
CREATE DATABASE coffee_shop_dw
  WITH
  ENCODING = 'UTF8'
  TEMPLATE = template0;
