DROP TABLE IF EXISTS Promotion;
CREATE TABLE Promotion(
   id          INTEGER  NOT NULL PRIMARY KEY,
   description VARCHAR(18) NOT NULL
);
INSERT INTO Promotion(id,description) VALUES (1,'Google Ads');
INSERT INTO Promotion(id,description) VALUES (2,'Organic Google');
INSERT INTO Promotion(id,description) VALUES (3,'Organic DuckDuckGo');
INSERT INTO Promotion(id,description) VALUES (4,'DuckDuckGo Ads');
INSERT INTO Promotion(id,description) VALUES (5,'Bing');
