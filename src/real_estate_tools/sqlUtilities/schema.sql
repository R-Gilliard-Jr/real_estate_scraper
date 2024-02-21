DROP TABLE IF EXISTS buy_data;
DROP TABLE IF EXISTS rent_data;
DROP TABLE IF EXISTS profit;
DROP TABLE IF EXISTS user;

CREATE TABLE buy_data (
    id, 
    price REAL, 
    beds INTEGER, 
    baths REAL, 
    sqft REAL, 
    lot REAL, 
    address TEXT, 
    zip TEXT, 
    latitude REAL, 
    longitude REAL, 
    url TEXT, 
    date_fetched DATE,
    PRIMARY KEY (address, zip, beds, baths)
);

CREATE TABLE rent_data (
    id, 
    price REAL, 
    beds INTEGER, 
    baths REAL, 
    sqft REAL, 
    address TEXT, 
    zip TEXT, 
    latitude REAL, 
    longitude REAL, 
    url TEXT, 
    date_fetched DATE,
    PRIMARY KEY (address, zip, beds, baths)
);

CREATE TABLE profit (
    id, 
    price REAL, 
    beds INTEGER, 
    baths REAL, 
    sqft REAL, 
    lot REAL, 
    address TEXT, 
    zip TEXT, 
    latitude REAL, 
    longitude REAL, 
    url TEXT, 
    date_fetched DATE,
    count INT, 
    min REAL,
    median REAL,
    mean REAL, 
    max REAL, 
    loan_principal REAL, 
    mortgage REAL, 
    taxes REAL,
    total_investment REAL, 
    min_cap_ex REAL, 
    min_prop_mng REAL, 
    min_profit REAL,
    min_coc REAL, 
    median_cap_ex REAL, 
    median_prop_mng REAL, 
    median_profit REAL,
    median_coc REAL, 
    mean_cap_ex REAL, 
    mean_prop_mng REAL, 
    mean_profit REAL, 
    mean_coc REAL,
    max_cap_ex REAL, 
    max_prop_mng REAL, 
    max_profit REAL, 
    max_coc REAL,
    PRIMARY KEY (address, zip, beds, baths)
);