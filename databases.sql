-- Table "comments"
DROP TABLE IF EXISTS comments;
CREATE TABLE IF NOT EXISTS comments (
  id int NOT NULL AUTO_INCREMENT,
  image_id int NOT NULL,
  user_id int NOT NULL,
  comment text NOT NULL,
  PRIMARY KEY (id),
  KEY image_id (image_id),
  KEY user_id (user_id)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table "users"
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTO_INCREMENT,
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  gender varchar(10) NOT NULL,
  dob date NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table "images"
DROP TABLE IF EXISTS images;
CREATE TABLE IF NOT EXISTS images (
  id int NOT NULL AUTO_INCREMENT,
  file_name varchar(255) NOT NULL,
  uploaded_on datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  likes int NOT NULL DEFAULT '0',
  image_data longblob,
  PRIMARY KEY (id)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--- Table 'likes '---
CREATE TABLE likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_id INT NOT NULL,
    UNIQUE (user_id, image_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (image_id) REFERENCES images(id)
);
