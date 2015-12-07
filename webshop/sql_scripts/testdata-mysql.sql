USE `little_webshop` ;

INSERT INTO Category (name) VALUES ('fish');
INSERT INTO Category (name) VALUES ('bread');
INSERT INTO Category (name) VALUES ('vegetables');
INSERT INTO Category (name) VALUES ('meat');
INSERT INTO Category (name) VALUES ('dairy');

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Pike', 39, 23, 'A species of carnivorous fish of the genus Esox (the pikes). They are typical of brackish and fresh waters of the Northern Hemisphere (i.e. holarctic in distribution).', 'http://loddea.hosterspace.com/wp-content/uploads/2011/09/Gädda.jpg',
(SELECT idCategory from Category WHERE name='fish'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Dace', 29, 56, 'The common dace (Leuciscus leuciscus), the dace or the Eurasian dace, is a fresh- or brackish-water fish belonging to the family Cyprinidae. It is an inhabitant of the rivers and streams of Europe north of the Alps as well as in Asia', 'http://www.finnake.se/fiskar/fish/mort.gif',
(SELECT idCategory from Category WHERE name='fish'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Perch', 12, 186, 'Perch is a common name for fish of the genus Perca, freshwater gamefish belonging to the family Percidae. The perch, of which there are three species in different geographical areas, lend their name to a large order of vertebrates', 'http://www.finnake.se/fiskar/fish/abborre.gif',
(SELECT idCategory from Category WHERE name='fish'));



INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Light bread', 42, 6, 'Made from wheat flour from which the bran and the germ layers have been removed.', 'http://www.jonasbergqvist.se/upl/images/267022.jpg',
(SELECT idCategory from Category WHERE name='bread'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Dark bread', 39, 68, 'Bread made with various proportions of flour from rye grain', 'http://www.ninasmatrecept.se/bilder/2009/10/gojibars-brod.jpg',
(SELECT idCategory from Category WHERE name='bread'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Loaf', 29, 3, 'A fat loaf.', 'http://cdn2.cdnme.se/cdn/9-2/944009/images/2009/limpa_1169038350_27562149.jpg',
(SELECT idCategory from Category WHERE name='bread'));



INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Tomato', 19, 388, 'A red and shiny tomato.', 'http://www.felix.se/wp-content/uploads/2010/11/tomat1.png',
(SELECT idCategory from Category WHERE name='vegetables'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Carrot', 13, 88, 'A  root vegetable, usually orange in colour, though purple, red, white, and yellow varieties exist.','http://www.martastradgard.se/morot.JPG',
(SELECT idCategory from Category WHERE name='vegetables'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Cucumber', 32, 128, 'A widely cultivated plant in the gourd family.', 'https://static.mathem.se/shared/images/products/large/gurka-klass1-1.jpg',
(SELECT idCategory from Category WHERE name='vegetables'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Lettuce', 5, 32, 'An annual plant of the daisy family Asteraceae. It is most often grown as a leaf vegetable, but sometimes for its stem and seeds.', 'http://ppl.nu/wp-content/isbergssallad.jpg',
(SELECT idCategory from Category WHERE name='vegetables'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Avocado', 15, 32, 'The avocado (Persea americana) is a tree native to Mexico and Central America.', 'http://bodyandplate.se/wp-content/uploads/2015/01/avokado-namaz.jpg',
(SELECT idCategory from Category WHERE name='vegetables'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Cauliflower', 5, 111, 'One of several vegetables in the species Brassica oleracea, in the family Brassicaceae.', 'http://www.portofruit.com/img/big/cauliflowers.jpg',
(SELECT idCategory from Category WHERE name='vegetables'));


INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Butter', 35, 111, 'Butter is a solid dairy product made by churning fresh or fermented cream or milk, to separate the butterfat from the buttermilk.', 'http://www.lchf.se/portals/0/butter.jpg',
(SELECT idCategory from Category WHERE name='dairy'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Milk', 15, 76, 'What calves drink.', 'https://upload.wikimedia.org/wikipedia/commons/0/0e/Milk_glass.jpg',
(SELECT idCategory from Category WHERE name='dairy'));

INSERT INTO Asset (name, price, amount, description, imagePath, Category_idCategory)
VALUES ('Pork', 115, 11, 'Assorted body parts from a dead pig.', 'https://dtgxwmigmg3gc.cloudfront.net/files/551a1067777a425ff901310b-icon-256x256.png',
(SELECT idCategory from Category WHERE name='meat'));


INSERT INTO User (login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email, admin)
VALUES ('a', 'a', 'Admin', 'Hansson', 'Balderstensgatan', 2342, 'Falköping', 0766034933234, 'chefen@mincoolaaddress.com', 1);

INSERT INTO User (login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email, admin)
VALUES ('b', 'b', 'Johan', 'Hansson', 'Storgatan', 42, 'Falköping', 076123433234, 'chefen@mincoolaaddress.com', 0);

