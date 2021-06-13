CREATE TABLE Calories (
    product TEXT,
    proteins FLOAT,
    carbs FLOAT,
    fats FLOAT,
    cal_per_100 FLOAT
);

CREATE TABLE Measure (
    product_id INTEGER REFERENCES Calories,
    serving_size TEXT
);
