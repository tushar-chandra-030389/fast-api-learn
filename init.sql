
CREATE TABLE product (
    "name" VARCHAR(255) NOT NULL,
    price FLOAT4 NOT NULL,
    id SERIAL PRIMARY KEY
);

INSERT INTO product ("name", price) VALUES ('TV', 200);
INSERT INTO product ("name", price) VALUES ('DVD Player', 80);
INSERT INTO product ("name", price) VALUES ('Remove', 10);

-- Add sales column
ALTER TABLE product ADD COLUMN is_sale BOOLEAN DEFAULT FALSE;

INSERT INTO product ("name", price, is_sale) VALUES ('Pencil', 2, true);

-- Add invetory column without constraint
ALTER TABLE product ADD COLUMN inventory INT;

UPDATE product SET inventory=10, is_sale=true WHERE id = 1;
UPDATE product SET inventory=5 WHERE id = 2;
UPDATE product SET inventory=10 WHERE id = 3;
UPDATE product SET inventory=20 WHERE id = 4;

-- Alter inventory column to not be null
ALTER TABLE product ALTER COLUMN inventory SET NOT NULL;

-- Add added on column
ALTER TABLE product ADD COLUMN added_on TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;

SELECT * FROM product;

------- MAIN ----------

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    "content" TEXT NOT NULL,
    published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


