USE `little_webshop` ;

INSERT INTO AssetCategory (categoryName) VALUES ('fish');
INSERT INTO AssetCategory (categoryName) VALUES ('bread');
INSERT INTO AssetCategory (categoryName) VALUES ('vegetables');
INSERT INTO AssetCategory (categoryName) VALUES ('meat');
INSERT INTO AssetCategory (categoryName) VALUES ('dairy');

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Pike', 39, 23, 'http://loddea.hosterspace.com/wp-content/uploads/2011/09/Gädda.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='fish'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Dace', 29, 56, 'http://www.finnake.se/fiskar/fish/mort.gif',
(SELECT idCategory from AssetCategory WHERE categoryName='fish'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Perch', 12, 186, 'http://www.finnake.se/fiskar/fish/abborre.gif',
(SELECT idCategory from AssetCategory WHERE categoryName='fish'));



INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Light bread', 42, 6, 'http://www.jonasbergqvist.se/upl/images/267022.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='bread'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Dark bread', 39, 68, 'http://www.ninasmatrecept.se/bilder/2009/10/gojibars-brod.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='bread'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Loaf', 29, 3, 'http://cdn2.cdnme.se/cdn/9-2/944009/images/2009/limpa_1169038350_27562149.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='bread'));



INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Tomato', 19, 388, 'http://www.felix.se/wp-content/uploads/2010/11/tomat1.png',
(SELECT idCategory from AssetCategory WHERE categoryName='vegetables'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Carrot', 13, 88, 'http://www.martastradgard.se/morot.JPG',
(SELECT idCategory from AssetCategory WHERE categoryName='vegetables'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Cucumber', 32, 128, 'https://static.mathem.se/shared/images/products/large/gurka-klass1-1.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='vegetables'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Lettuce', 5, 32, 'http://ppl.nu/wp-content/isbergssallad.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='vegetables'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Avocado', 15, 32, 'http://bodyandplate.se/wp-content/uploads/2015/01/avokado-namaz.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='vegetables'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Cauliflower', 5, 111, 'http://www.portofruit.com/img/big/cauliflowers.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='vegetables'));


INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Butter', 35, 111, 'http://www.lchf.se/portals/0/butter.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='dairy'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Milk', 15, 76, 'https://upload.wikimedia.org/wikipedia/commons/0/0e/Milk_glass.jpg',
(SELECT idCategory from AssetCategory WHERE categoryName='dairy'));

INSERT INTO Asset (name, price, amountInStore, imagePath, AssetCategory_idCategory)
VALUES ('Pork', 115, 11, 'https://dtgxwmigmg3gc.cloudfront.net/files/551a1067777a425ff901310b-icon-256x256.png',
(SELECT idCategory from AssetCategory WHERE categoryName='meat'));


INSERT INTO Customer (login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email)
VALUES ('chefen', 'password1', 'Henrik', 'Hansson', 'Balderstensgatan', 2342, 'Falköping', 0766034933234, 'chefen@mincoolaaddress.com');

INSERT INTO Customer (login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email)
VALUES ('testperson1', 'password2', 'Kalle', 'Olofsson', 'Margaretagatan', 123432, 'Falköping', 2766034933214, 'test@asdfqwersadf.com');

INSERT INTO Customer (login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email)
VALUES ('testperson2', 'password3', 'Olle', 'Karlsson', 'Westerbergsgatan', 32, 'Falköping', 7766034933234, 'test@rtutyr.com');