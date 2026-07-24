CREATE DATABASE IF NOT EXISTS rental CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rental;

CREATE TABLE IF NOT EXISTS house (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(50) NOT NULL,
  rent_type VARCHAR(20) NOT NULL,
  floor INTEGER NOT NULL,
  all_floor INTEGER NOT NULL,
  house_type VARCHAR(20) NOT NULL,
  rooms VARCHAR(20) NOT NULL,
  position VARCHAR(20) NOT NULL,
  area DECIMAL(10, 2) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  intro VARCHAR(2047) NOT NULL,
  devices VARCHAR(255) NOT NULL,
  head_image VARCHAR(255) NOT NULL,
  images VARCHAR(2047) NOT NULL,
  city_id BIGINT NOT NULL,
  city_name VARCHAR(40) NOT NULL,
  region_id BIGINT NOT NULL,
  region_name VARCHAR(40) NOT NULL,
  community_name VARCHAR(80) NOT NULL,
  detail_address VARCHAR(255) NOT NULL,
  longitude DECIMAL(10, 7) NOT NULL,
  latitude DECIMAL(10, 7) NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_house_city_price (city_name, price),
  INDEX idx_house_region_price (region_name, price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
