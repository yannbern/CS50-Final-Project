DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Items;

CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY,
    Username TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL,
    UNIQUE(Username, Email)
);

CREATE TABLE Categories (
    CategoryID INTEGER PRIMARY KEY,
    CategoryName TEXT NOT NULL UNIQUE
);

INSERT INTO Categories (CategoryName) VALUES
('Cars'),
('Furniture'),
('Electronics'),
('Clothing'),
('Other'),
('HomeGarden'),
('BooksMedia');

CREATE TABLE Items (
    ItemID INTEGER PRIMARY KEY,
    UserID INTEGER,
    CategoryID INTEGER,
    Title TEXT NOT NULL,
    Description TEXT,
    Price REAL,
    ImageFilePath TEXT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    Condition TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);