DROP TABLE IF EXISTS ProductReviews;
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Commands;
DROP TABLE IF EXISTS CartItems;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;



CREATE TABLE Users (
    Username varchar(40) PRIMARY KEY,
    Name VARCHAR(40),
    Email VARCHAR(40) UNIQUE,
    Password VARCHAR(400),
    Address VARCHAR(255),
    InscriptionDate DATETIME
);

CREATE TABLE Categories (
    CategorieID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Description VARCHAR(500)
);

CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Description VARCHAR(1000),
    Price DECIMAL(10, 2),
    Stock INT,
    CategorieID INT,
    FOREIGN KEY (CategorieID) REFERENCES Categories(CategorieID)
);

CREATE TABLE CartItems (
    CartItemID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(40),
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Commands (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(40),
    DateCommand DATETIME,
    Status VARCHAR(40),
    DeliveryAddress VARCHAR(255),
    Total DECIMAL(10, 2),
    FOREIGN KEY (Username) REFERENCES Users (Username)
);

CREATE TABLE OrderItems (
    OrderItemID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Commands(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE ProductReviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    Username VARCHAR(40),
    Note INT,
    Commentaire TEXT,
    Date DATETIME,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (Username) REFERENCES Users(Username)
);

INSERT INTO Users (Username,Name, Email, Password, Address, InscriptionDate) VALUES
("dasda", 'Alexandre Dubois', 'alexandre.dubois@example.com', 'dsadsadsa', '1234 Rue de la République, Paris', '2023-01-01'),
("dadsasda",'Marie Joly', 'marie.joly@example.com', 'dsadsadsa', '5678 Avenue de la Liberté, Marseille', '2023-01-02'),
("ddasdsaasda",'Lucas Martin', 'lucas.martin@example.com', 'dsadsa', '91011 Boulevard de lÉgalité, Lyon', '2023-01-03'),
("dahjgfsda",'Chloé Bernard', 'chloe.bernard@example.com', 'dsadasdsa', '1213 Rue de la Fraternité, Toulouse', '2023-01-04'),
("dadsadasda",'Maxime Petit', 'maxime.petit@example.com', 'fdsfdsfds', '1415 Avenue de la Paix, Nice', '2023-01-05'),
("ddasdasdsadasasda",'Sophie Mercier', 'sophie.mercier@example.com', 'hgfd', '1617 Boulevard de lAmour, Nantes', '2023-01-06'),
("djhgbasda",'Gabriel Rousseau', 'gabriel.rousseau@example.com', 'hashgfded_pasgfdsword', '1819 Rue du Progrès, Strasbourg', '2023-01-07'),
("dasdasda",'Emma Moreau', 'emma.moreau@example.com', 'hgfdword', '2021 Avenue de la Victoire, Bordeaux', '2023-01-08'),
("dgfsda",'Hugo Dupont', 'hugo.dupont@example.com', 'hasheddasrd', '2223 Boulevard de la Révolution, Lille', '2023-01-09'),
("dakoisda",'Inès Lefebvre', 'ines.lefebvre@example.com', 'hasgfdrd', '2425 Rue de la Libération, Rennes', '2023-01-10'),
("thom",'Thomas Girard', 'thomas.girard@example.com', 'hhfdsword', '2627 Rue de la Solidarité, Montpellier', '2023-01-11'),
("JULDAVID",'Julie David', 'julie.david@example.com', 'hword', '2829 Avenue de la Justice, Lille', '2023-01-12'),
("ANTOINEEMYGUYY",'Antoine Durand', 'antoine.durand@example.com', 'hdsard', '3031 Boulevard de la Liberté, Reims', '2023-01-13'),
("camillehashtag",'Camille Fontaine', 'camille.fontaine@example.com', 'hadsaword', '3233 Rue de la Démocratie, Saint-Étienne', '2023-01-14'),
("NicoWHiteBoy",'Nicolas Blanc', 'nicolas.blanc@example.com', 'hadsaword', '3435 Avenue de l\'Égalité, Toulon', '2023-01-15'),
("CharlotteDenisTrust",'Charlotte Denis', 'charlotte.denis@example.com', 'hasdsasword', '3637 Boulevard de lUnion, Grenoble', '2023-01-16'),
("Quentin avec un q",'Quentin Leclerc', 'quentin.leclerc@example.com', 'hasdsasword', '3839 Rue de la Fraternité, Dijon', '2023-01-17'),
("snowhite",'Clara Morin', 'clara.morin@example.com', 'hasdsaword', '4041 Avenue de la Paix, Angers', '2023-01-18'),
("guigui",'Guillaume Simon', 'guillaume.simon@example.com', 'hadsasword', '4243 Boulevard de l\'Amour, Nîmes', '2023-01-19'),
("myfriendscallmealicia",'Alicia Robert', 'alicia.robert@example.com', 'hadsassword', '4445 Rue du Progrès, Villeurbanne', '2023-01-20'),
("whatisausername",'Laurent Lemoine', 'laurent.lemoine@example.com', 'password123', '4647 Rue de la Paix, Clermont-Ferrand', '2023-01-21'),
("ameliehiihih",'Amélie Dupuis', 'amelie.dupuis@example.com', 'monMotDePasse', '4849 Avenue de Verdun, Limoges', '2023-01-22'),
("romane",'Romain Tessier', 'romain.tessier@example.com', 'superSecure', '5051 Boulevard de Strasbourg, Tours', '2023-01-23'),
("sophie",'Sophia Richard', 'sophia.richard@example.com', 'passw0rd!', '5253 Rue Victor Hugo, Amiens', '2023-01-24'),
("jesuispaspetit",'Baptiste Petit', 'baptiste.petit@example.com', 'motdepasse', '5455 Avenue Jean Jaurès, Metz', '2023-01-25'),
("lareine",'Léa Leroy', 'lea.leroy@example.com', '12345', '5657 Boulevard Voltaire, Besançon', '2023-01-26'),
("rouset",'Cédric Roussel', 'cedric.roussel@example.com', 'azerty', '5859 Rue de la République, Perpignan', '2023-01-27'),
("emyyyyy",'Émilie Morel', 'emilie.morel@example.com', 'qwerty', '6061 Avenue des États-Unis, Caen', '2023-01-28'),
("alx",'Alexis Renaud', 'alexis.renaud@example.com', 'password', '6263 Boulevard de la Liberté, Orléans', '2023-01-29'),
("Lepen",'Marine Caron', 'marine.caron@example.com', 'letmein', '6465 Rue des Martyrs, Mulhouse', '2023-01-30'),
("Berger",'Noémie Berger', 'noemie.berger@example.com', 's3cur3P@ss', '6667 Rue de la Liberté, Rouen', '2023-01-31'),
("Mercier",'Lucas Mercier', 'lucas.mercier@example.com', 'p4ssword', '6869 Avenue du Général Leclerc, Avignon', '2023-02-01'),
("Brunet",'Chloé Brunet', 'chloe.brunet@example.com', '123456789', '7071 Boulevard de Sébastopol, Nancy', '2023-02-02'),
("Blanchard",'Maxime Blanchard', 'maxime.blanchard@example.com', 'football', '7273 Rue des Rosiers, Saint-Denis', '2023-02-03'),
("bruhhhhhh",'Pauline François', 'pauline.francois@example.com', 'pa$$w0rd', '7475 Avenue de la Marne, La Rochelle', '2023-02-04'),
("jeeee",'Jérémy David', 'jeremy.david@example.com', 'myPa$$word', '7677 Boulevard Saint-Germain, Cannes', '2023-02-05'),
("maellaaaaa",'Maëlle Dupont', 'maelle.dupont@example.com', 'password1', '7879 Rue de Bretagne, Annecy', '2023-02-06'),
("theooo",'Théo Lambert', 'theo.lambert@example.com', 'qwerty123', '8081 Avenue Victor Hugo, Grenoble', '2023-02-07'),
("lvcool",'Louise Vincent', 'louise.vincent@example.com', 'sunshine', '8283 Boulevard de la Villette, Brest', '2023-02-08'),
("hug",'Hugo Martin', 'hugo.martin@example.com', 'iloveyou', '8485 Rue du Faubourg Saint-Antoine, Le Mans', '2023-02-09'),
("eva",'Eva Rousseau', 'eva.rousseau@example.com', 'secret2023', '8687 Rue de lUniversité, Nancy', '2023-02-10'),
("arthur",'Arthur Morel', 'arthur.morel@example.com', 'motdepasse2023', '8989 Avenue des Ternes, Clermont-Ferrand', '2023-02-11'),
("julietteeeeeeeee",'Juliette Petit', 'juliette.petit@example.com', '123soleil', '9091 Boulevard Haussmann, Rennes', '2023-02-12'),
("Aldsaex",'Axel Dubois', 'axel.dubois@example.com', 'pianoforte', '9293 Rue du Commerce, Brest', '2023-02-13'),
("lolav",'Lola Vincent', 'lola.vincent@example.com', 'azerty2023', '9495 Avenue de la République, Le Havre', '2023-02-14'),
("Nate",'Nathan Lefevre', 'nathan.lefevre@example.com', 'qwerty2023', '9697 Rue de Rivoli, Reims', '2023-02-15'),
("AG",'Alice Garnier', 'alice.garnier@example.com', 'aloha2023', '9899 Boulevard Saint-Michel, Saint-Étienne', '2023-02-16'),
("martyyy",'Léo Martinez', 'leo.martinez@example.com', 'welcome2023', '0001 Rue de la Libération, Toulon', '2023-02-17'),
("Royaute",'Zoé Leroy', 'zoe.leroy@example.com', 'smile2023', '0203 Avenue Jean Médecin, Grenoble', '2023-02-18'),
("valentine",'Valentin Robin', 'valentin.robin@example.com', 'spring2023', '0405 Boulevard de la Victoire, Dijon', '2023-02-19'),
("mathilda",'Mathilde Perrin', 'mathilde.perrin@example.com', 'fall2023', '0607 Rue de Paris, Nîmes', '2023-02-20'),
("simone",'Simon Bernard', 'simon.bernard@example.com', 'winter2023', '0809 Avenue de Lyon, Montpellier', '2023-02-21'),
("dsaddsadsadsadsa",'Julie Renaud', 'julie.renaud@example.com', 'summer2023', '1011 Boulevard de Marseille, Bordeaux', '2023-02-22'),
("dasdasbjhksda",'Marc Andre', 'marc.andre@example.com', 'spring2024', '1213 Rue de Toulouse, Lille', '2023-02-23'),
("poulpe",'Charlotte Lemoine', 'charlotte.lemoine@example.com', 'moon2023', '1415 Avenue de Nice, Strasbourg', '2023-02-24'),
("GUIKOO",'Guillaume Joly', 'guillaume.joly@example.com', 'stars2023', '1617 Boulevard de Montpellier, Rennes', '2023-02-25'),
("ecko",'Sarah Dubois', 'sarah.dubois@example.com', 'ocean2023', '1819 Rue de Bordeaux, Le Mans', '2023-02-26'),
("yannybnelly",'Yann Leclerc', 'yann.leclerc@example.com', 'forest2023', '2021 Avenue de Lille, Angers', '2023-02-27'),
("mariowhatisthatnamebruh",'Marion Roux', 'marion.roux@example.com', 'river2023', '2223 Boulevard de Strasbourg, Nantes', '2023-02-28'),
("nicooolaaas",'Nicolas Meyer', 'nicolas.meyer@example.com', 'mountain2023', '2425 Rue de Rennes, Clermont-Ferrand', '2023-03-01'),
("camimiy",'Camille Olivier', 'camille.olivier@example.com', 'valley2023', '2627 Avenue de Angers, Saint-Denis', '2023-03-02'),
("Bennn",'Benoit Blanchard', 'benoit.blanchard@example.com', 'lake2023', '2829 Boulevard de Nantes, Le Havre', '2023-03-03'),
("EliseAufour",'Élise Dufour', 'elise.dufour@example.com', 'sky2023', '3031 Rue de Saint-Denis, Grenoble', '2023-03-04'),
("RemRem",'Rémi Caron', 'remi.caron@example.com', 'cloud2023', '3233 Avenue de Le Havre, Dijon', '2023-03-05'),
("daAnnnnasda",'Anaïs Dupond', 'anais.dupond@example.com', 'sun2023', '3435 Boulevard de Grenoble, Aix-en-Provence', '2023-03-06'),
("LucyLuke",'Lucie Morin', 'lucie.morin@example.com', 'moonlight2023', '3637 Rue de Dijon, Brest', '2023-03-07'),
("MyguyAlex",'Alexis Girard', 'alexis.girard@example.com', 'dawn2023', '3839 Avenue de Aix-en-Provence, Villeurbanne', '2023-03-08'),
("MygirlMelanie",'Mélanie Laurent', 'melanie.laurent@example.com', 'twilight2023', '4041 Boulevard de Brest, Nice', '2023-03-09'),
("dsadsadsadsadsa",'Tristan Roy', 'tristan.roy@example.com', 'nightfall2023', '4243 Rue de Villeurbanne, Limoges', '2023-03-10'),
("Celili",'Céline Fournier', 'celine.fournier@example.com', 'daybreak2023', '4445 Avenue de Nice, Amiens', '2023-03-11'),
("FLoflo",'Florian Petit', 'florian.petit@example.com', 'dusk2023', '4647 Rue des Écoles, Caen', '2023-03-12'),
("justinBrun",'Justine Brun', 'justine.brun@example.com', 'horizon2023', '4849 Avenue des Peupliers, Rouen', '2023-03-13'),
("Lerouxpasroux",'Damien Leroux', 'damien.leroux@example.com', 'glow2023', '5051 Boulevard des Fleurs, Nancy', '2023-03-14'),
("barnrdeur",'Élodie Bernard', 'elodie.bernard@example.com', 'shine2023', '5253 Rue de la Forge, Reims', '2023-03-15'),
("sabsdubois",'Sébastien Dubois', 'sebastien.dubois@example.com', 'gleam2023', '5455 Avenue de lOpéra, Saint-Étienne', '2023-03-16'),
("clemrousss",'Clémentine Rousseau', 'clementine.rousseau@example.com', 'sparkle2023', '5657 Boulevard de la Victoire, Toulon', '2023-03-17'),
("thibhtib",'Thibault Blanc', 'thibault.blanc@example.com', 'flash2023', '5859 Rue du Lac, Grenoble', '2023-03-18'),
("audreymartinezzzzx",'Audrey Martin', 'audrey.martin@example.com', 'streak2023', '6061 Avenue des Vosges, Dijon', '2023-03-19'),
("mullerthesoccerplayer",'Maxence Muller', 'maxence.muller@example.com', 'beam2023', '6263 Boulevard de Normandie, Angers', '2023-03-20'),
("duboislouane",'Louane Dubois', 'louane.dubois@example.com', 'radiance2023', '6465 Rue des Lilas, Brest', '2023-03-21'),
("victoravecunc",'Victor Leroy', 'victor.leroy@example.com', 'luster2023', '6667 Avenue du Maine, Le Mans', '2023-03-22'),
("oceeeeee",'Océane Moreau', 'oceane.moreau@example.com', 'gleaming2023', '6869 Boulevard de lAtlantique, Nantes', '2023-03-23'),
("antooooine",'Antoine Garnier', 'antoine.garnier@example.com', 'shimmer2023', '7071 Rue de Bretagne, Clermont-Ferrand', '2023-03-24'),
("maelys",'Maëlys Lemoine', 'maelys.lemoine@example.com', 'twinkle2023', '7273 Avenue de Provence, Limoges', '2023-03-25'),
("raph",'Raphaël Gauthier', 'raphael.gauthier@example.com', 'glint2023', '7475 Boulevard du Littoral, Rouen', '2023-03-26'),
("zozo",'Zoé Poirier', 'zoe.poirier@example.com', 'scintillate2023', '7677 Rue du Marché, Nancy', '2023-03-27'),
("lucaslafontaine",'Lucas Fontaine', 'lucas.fontaine@example.com', 'glimmer2023', '7879 Avenue de la Révolution, Reims', '2023-03-28'),
("helenecool",'Hélène Dupond', 'helene.dupond@example.com', 'flicker2023', '8081 Boulevard des Étoiles, Saint-Étienne', '2023-03-29'),
("bruhhhh",'Jérôme Carpentier', 'jerome.carpentier@example.com', 'spark2023', '8283 Rue de lUniversité, Toulon', '2023-03-30'),
("datessda",'Émilie Laurent', 'emilie.laurent@example.com', 'flare2023', '8485 Avenue de la Libération, Grenoble', '2023-03-31'),
("dasdsadsadsadada",'Nina Mercier', 'nina.mercier@example.com', 'night2023', '8687 Rue des Pyrénées, Aix-en-Provence', '2023-04-01'),
("dasdhjasdkiada",'Alexis Renard', 'alexis.renard@example.com', 'dawn2024', '8889 Avenue des Tilleuls, Le Havre', '2023-04-02'),
("dasgdfsgfdda",'Margaux Colin', 'margaux.colin@example.com', 'evening2023', '9091 Rue du Soleil, Nancy', '2023-04-03'),
("oijlj",'Félix Da Silva', 'felix.dasilva@example.com', 'morning2023', '9293 Boulevard de la Mer, Reims', '2023-04-04'),
("iopuoripewpiorp",'Sarah Lefevre', 'sarah.lefevre@example.com', 'midnight2023', '9495 Avenue des Anges, Saint-Étienne', '2023-04-05'),
("ljhlknnm",'David Simon', 'david.simon@example.com', 'twilight2024', '9697 Rue de lEspoir, Toulon', '2023-04-06'),
("iuerw",'Élisa Roussel', 'elisa.roussel@example.com', 'daylight2023', '9899 Boulevard de la Paix, Grenoble', '2023-04-07'),
("gfhjdvbn",'Rémi Fontaine', 'remi.fontaine@example.com', 'sunset2023', '0001 Rue de lAurore, Dijon', '2023-04-08'),
("nmvxcz",'Chloé Perrin', 'chloe.perrin@example.com', 'sunrise2023', '0203 Avenue des Braves, Angers', '2023-04-09'),
("thomaslepetittrain",'Thomas Riviere', 'thomas.riviere@example.com', 'day2023', '0405 Boulevard du Matin, Brest', '2023-04-10'),
("lauralapetite",'Laura Petit', 'laura.petit@example.com', 'light2023', '0607 Rue de la Lumière, Le Mans', '2023-04-11'),
("sambernard",'Samuel Bernard', 'samuel.bernard@example.com', 'bright2023', '0809 Avenue de lÉclat, Nantes', '2023-04-12'),
("marieismygirl",'Marie Dubois', 'marie.dubois@example.com', 'shine2024', '1011 Rue des Lueurs, Clermont-Ferrand', '2023-04-13'),
("JulLeclerc",'Julien Leclerc', 'julien.leclerc@example.com', 'glow2024', '1213 Boulevard des Rayons, Limoges', '2023-04-14'),
("sophhhhhie",'Sophie Martin', 'sophie.martin@example.com', 'beam2024', '1415 Avenue de lIllumination, Rouen', '2023-04-15'),
("LucDurHein",'Lucas Durand', 'lucas.durand@example.com', 'luminous2023', '1617 Rue de lAube, Nancy', '2023-04-16'),
("emmaawatsonfangirl",'Emma Thibault', 'emma.thibault@example.com', 'radiant2023', '1819 Boulevard du Jour, Reims', '2023-04-17'),
("hugoposay",'Hugo Boucher', 'hugo.boucher@example.com', 'gleam2023', '2021 Avenue de lOrée, Saint-Étienne', '2023-04-18'),
("inessFOurnirerrr",'Inès Fournier', 'ines.fournier@example.com', 'glisten2023', '2223 Rue du Zenith, Toulon', '2023-04-19'),
("maxPacioretty2323",'Maxime Leroux', 'maxime.leroux@example.com', 'sparkle2024', '2425 Boulevard de lAurora, Grenoble', '2023-04-20');


INSERT INTO Categories (Name, Description) VALUES
('Men', 'Masculine-style clothing'),
('Women', 'Feminine-style clothing'),
('Kids', 'Clothing for children'),
('Accessories', 'Accessories for everyone'),
('Unisex', 'Clothing for everyone');


INSERT INTO Products (Name, Description, Price, Stock, CategorieID) VALUES
("Men's T-shirt", "A comfortable t-shirt for men.", 19.99, 100, 1),
("Women's Dress", "A beautiful summer dress for women.", 39.99, 50, 2),
("Kids' Jeans", "Durable jeans for children.", 29.99, 75, 3),
("Men's Sweater", "A warm and comfortable sweater for winter.", 49.99, 80, 1),
("Women's Running Shoes", "Lightweight and breathable sports shoes.", 89.99, 120, 2),
("Kids' Cap", "Cotton cap with a visor for sun protection.", 14.99, 150, 3),
("Unisex Backpack", "Durable backpack with multiple compartments.", 59.99, 100, 4),
("Sport Watch", "Waterproof digital watch with built-in GPS.", 199.99, 40, 4),
("Women's Jacket", "Stylish and comfortable jacket for mid-season.", 79.99, 60, 2),
("Men's Shorts", "Light fabric shorts, ideal for summer or sports.", 24.99, 90, 1),
("Kids' Sandals", "Comfortable sandals for playing or walking around.", 19.99, 110, 3),
("Unisex Scarf", "Soft and warm scarf for winter.", 29.99, 70, 4),
("Sunglasses", "UV400 protection for maximum safety.", 34.99, 85, 4),
("Women's Shirt", "Light silk shirt, perfect for the office or an outing.", 55.99, 60, 2),
("Men's Sneakers", "Ultra-comfortable sneakers for daily wear or sports.", 75.99, 90, 1),
("Kids' Hat", "Straw hat with a colorful ribbon, ideal for summer.", 12.99, 40, 3),
("Women's Leggings", "Stretch fabric leggings, support and comfort for sports.", 35.99, 80, 2),
("Men's Tie", "Silk tie, available in multiple colors.", 29.99, 50, 1),
("Kids' Gloves", "Warm gloves for winter, with fun patterns.", 9.99, 30, 3),
("Unisex Belt", "Robust leather belt, adjustable to all sizes.", 22.99, 75, 4),
("Men's Motorcycle Jacket", "Leather jacket with protections, style and safety.", 159.99, 25, 1),
("Women's Evening Dress", "Elegant dress with sparkling details, for special occasions.", 129.99, 20, 2),
("Kids' Swimsuit", "Colorful swimsuit, chlorine and salt resistant.", 19.99, 60, 3),
("Unisex Wallet", "Leather wallet with multiple compartments.", 45.99, 110, 4),
("Women's Handbag", "Genuine leather handbag, elegant and practical.", 89.99, 40, 2),
("Men's Pants", "Light fabric pants, comfortable fit.", 49.99, 70, 1),
("Kids' Beanie", "Soft wool beanie, keeps warm all winter.", 14.99, 80, 3),
("Women's Sneakers", "Trendy sneakers with arch support.", 65.99, 95, 2),
("Men's Suit", "Tailor-made suit, elegance and comfort.", 299.99, 15, 1),
("Kids' Graphic T-shirt", "T-shirt with playful prints, 100% cotton.", 15.99, 120, 3),
("Women's Midi Skirt", "Pleated midi skirt, classic and versatile style.", 42.99, 65, 2),
("Men's Cotton Socks", "Cotton blend socks, lasting comfort.", 5.99, 150, 1),
("Baby Romper", "Soft romper for baby, easy to put on.", 17.99, 50, 3),
("Kids' Swimming Goggles", "Waterproof goggles for swimming, UV protection.", 14.99, 45, 3),
("Men's Sweatshirt", "Soft cotton sweatshirt with hood, ideal for cool days.", 49.99, 55, 1),
("Unisex Umbrella", "Compact and wind-resistant umbrella, automatic opening.", 24.99, 80, 4),
("Women's Espadrilles", "Lightweight canvas espadrilles, jute sole.", 29.99, 70, 2),
("Kids' Sleeping Bag", "Themed lightweight and warm sleeping bag.", 39.99, 30, 3),
("Men's Elegant Watch", "Watch with leather strap, minimalist dial.", 199.99, 25, 1),
("Women's Jewelry", "Delicate silver necklace with crystal pendant.", 55.99, 40, 2),
("Unisex Water Bottle", "Stainless steel water bottle, 500ml, thermal insulation.", 19.99, 100, 4),
("Men's Polo", "Pique cotton polo, classic fit.", 34.99, 75, 1),
("Kids' Ski Suit", "Waterproof and insulated ski suit.", 89.99, 20, 3),
("Women's Rain Boots", "Elegant design rubber rain boots, waterproof.", 74.99, 40, 2),
("Kids' School Bag", "Durable school bag with fun patterns, multiple pockets.", 49.99, 50, 3),
("Unisex Hiking Jacket", "Waterproof and breathable jacket, multiple pockets.", 99.99, 60, 4),
("Men's Tennis Shoes", "Light tennis shoes, reinforced lateral support.", 85.99, 50, 1),
("Women's Beach Dress", "Light cotton beach dress, perfect for the beach.", 45.99, 65, 2),
("Kids' Lightweight Down Jacket", "Light but warm down jacket, easy to carry.", 59.99, 30, 3),
("Unisex Bluetooth Earphones", "Wireless earphones with charging case, high-definition sound quality.", 129.99, 90, 4),
("Women's Blouse", "Flowing blouse, long sleeves, V-neck.", 42.99, 50, 2),
("Men's Swim Shorts", "Quick-dry swim shorts, tropical patterns.", 25.99, 80, 1),
("Kids' Educational Toy", "Wooden educational toy, develops fine motor skills.", 29.99, 40, 3),
("Women's Yoga Pants", "Stretchy and breathable yoga pants, ideal for fitness.", 35.99, 60, 2),
("Unisex Weighted Blanket", "Weighted blanket for better sleep, 5kg.", 89.99, 40, 4),
("Kids' Airplane Model Kit", "Airplane model kit, paint and glue included.", 24.99, 50, 3),
("Unisex Sports Bag", "Spacious sports bag with shoe compartment.", 29.99, 70, 4),
("Women's Earrings", "Gold earrings with pearls, elegant and timeless.", 120.99, 30, 2),
("Men's Wool Scarf", "Soft wool scarf, warm for winter.", 40.99, 80, 1),
("Kids' 3D Puzzle", "3D puzzle of the solar system, educational and fun.", 35.99, 60, 3),
("Unisex Electric Scooter", "Foldable electric scooter, up to 25 km/h.", 249.99, 25, 4),
("Men's Flannel Shirt", "Soft flannel plaid shirt, comfortable.", 45.99, 55, 1),
("Women's Maxi Dress", "Light maxi dress with floral print, perfect for summer.", 55.99, 40, 2),
("Kids' Magic Kit", "Magic kit with 50 tricks, for budding magicians.", 22.99, 70, 3),
("Unisex Desk Lamp", "LED desk lamp with brightness control.", 49.99, 85, 4),
("Women's Blazer", "Fitted blazer, ideal for a professional or casual look.", 70.99, 45, 2),
("Unisex Insulated Mug", "Stainless steel insulated mug, keeps drinks at temperature.", 19.99, 100, 4),
("Men's Slim Jeans", "Slim denim jeans, comfortable and stylish.", 59.99, 75, 1),
("Kids' Binoculars", "Lightweight and durable binoculars for adventure.", 25.99, 65, 3),
("Women's Necklace", "Silver necklace with heart pendant, romantic gift.", 49.99, 50, 2),
("Unisex Notebook", "Leather notebook for your thoughts and drawings.", 14.99, 90, 4),
("Men's Basketball", "Official basketball, regulation size and weight.", 29.99, 55, 1),
("Kids' Paint Set", "Paint set with brushes, varied colors, non-toxic.", 19.99, 80, 3),
("Unisex BluetoothHeadphones", "High-quality audio headphones with noise cancellation.", 130.99, 40, 4),
("Men''s Hiking Shoes", "Sturdy and waterproof shoes, ideal for hiking.", 110.99, 35, 1),
("Women''s Sports Tank Top", "Light and breathable tank top for sports.", 25.99, 60, 2),
("Kids'' Remote-Controlled Drone with Camera", "Beginner-friendly remote-controlled drone with HD camera.", 75.99, 20,3),
("Unisex Surfboard", "Surfboard suitable for beginners and intermediates.", 299.99, 15, 4),
("Women''s Leather Handbag", "Elegant real leather handbag, multiple compartments.", 95.99, 25, 2),
("Men''s Smart Watch", "Activity tracking and notification smart watch.", 199.99, 30, 1),
("Kids'' Gardening Kit", "Gardening kit with tools, gloves, and pots, for young gardeners.", 29.99, 40, 3),
("Unisex Fitness Bracelet", "Fitness bracelet tracking steps, sleep, and heart rate.", 59.99, 50, 4),
("Kids'' Sunscreen", "SPF 50+ sunscreen, water-resistant, for sensitive skin.", 19.99, 70, 3),
("Unisex Yoga Mat", "Eco-friendly non-slip yoga mat with strap.", 49.99, 60, 4),
("Women''s Cycling Shorts", "Comfortable cycling shorts with gel padding.", 39.99, 50, 2),
("Unisex Filter Water Bottle", "Water bottle with integrated filter, purifies as you drink.", 34.99, 80, 4),
("Men''s Laptop Bag", "Stylish and functional laptop bag for up to 15-inch laptops.", 59.99, 45, 1),
("Women''s Knit Dress", "Soft and comfortable knit dress, ideal for autumn.", 65.99, 30, 2),
("Kids'' Robot Building Kit", "Build and program your own robot kit.", 45.99, 25, 3),
("Unisex Action Camera", "Waterproof 4K action camera with mounting accessories.", 120.99, 35, 4),
("Men''s Climbing Gear", "Complete climbing harness with carabiners and descender.", 99.99, 20, 1),
("Women''s Makeup Palette", "Makeup palette with a range of neutral and vibrant colors.", 29.99, 55, 2),
("Kids'' Board Games", "Educational and fun board games for the whole family.", 24.99, 65, 3),
("Unisex Recipe Book", "Healthy recipes book for every day of the week.", 29.99, 85, 4),
("Kids'' Touch Lamp", "Touch command bedside lamp, ideal for kids'' rooms.", 22.99, 40, 3),
("Men''s Minimalist Card Holder", "Real leather slim design card holder for the essentials.", 18.99, 95, 1),
("Women''s Jewelry Set", "Jewelry set with matching necklace and earrings.", 49.99, 30, 2),
("Kids'' Educational Alarm Clock", "Alarm clock with fun display to learn time.", 19.99, 50, 3),
("Unisex Beach Towel", "Large soft and absorbent beach towel with summer motifs.", 14.99, 75, 4),
("Men''s Beard Care Kit", "Kit with oil, balm, comb, and brush for beard maintenance.", 39.99, 60, 1),
("Women''s Compression Leggings", "Compression leggings for sports, optimal muscle support.", 55.99, 45, 2),
("Kids'' Advanced Magic Kit", "Magic kit for children looking to deepen their magic skills.", 34.99, 30, 3),
("Unisex Travel Journal", "Travel journal to note your adventures and keep memories.", 12.99, 85, 4),
("Men''s Casual Shirt", "Cotton casual shirt, perfect for the weekend.", 45.99, 70, 1),
("Women''s Sports Bra", "High-performance sports bra, superior support.", 29.99, 65, 2),
("Kids'' Interactive Plush", "Interactive plush that sings and tells stories.", 49.99, 40, 3),
("Unisex Hiking Backpack", "40L hiking backpack, durable and comfortable.", 69.99, 55, 4),
("Men''s Comfort Slippers", "Soft wool slippers with non-slip sole.", 24.99, 90, 1);

INSERT INTO Commands (Username, DateCommand, Status, DeliveryAddress, Total) VALUES
("marieismygirl", NOW(), 'Shipped', '1234 Rue Fictive, Ville', 59.97),
("marieismygirl", NOW(), 'Processing', '5678 Rue Imaginaire, Ville', 39.99),
("marieismygirl", NOW(), 'Delivered', '91011 Boulevard de lÉgalité, Lyon', 120.97),
("marieismygirl", NOW(), 'Cancelled', '1213 Rue de la Fraternité, Toulouse', 0.00),
("marieismygirl", NOW(), 'Awaiting Payment', '1415 Avenue de la Paix, Nice', 200.50),
("marieismygirl", NOW(), 'Shipped', '1617 Boulevard de lAmour, Nantes', 75.00);


INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)VALUES
(1, 1, 3, 19.99),
(2, 2, 1, 39.99),
(3, 3, 2, 29.99),
(3, 5, 1, 89.99),
(4, 6, 3, 14.99),
(5, 10, 2, 24.99),
(6, 12, 1, 29.99),
(6, 14, 1, 34.99);

INSERT INTO ProductReviews (ProductID, Username, Note, Commentaire, Date) VALUES
(1, "marieismygirl", 5, 'Excellent T-shirt, very comfortable!', NOW()),
(2, "marieismygirl", 4, "Love this dress, but delivery took a while.", NOW()),
(3, "marieismygirl", 4, 'Good quality but fits a bit large.', NOW()),
(5, "marieismygirl", 5, 'Perfect for running. Very comfortable.', NOW()),
(10, "marieismygirl", 2, 'The shorts are nice but the seams are fragile.', NOW()),
(12, "marieismygirl", 3, 'Scarf is pretty but thinner than I thought.', NOW());


CREATE INDEX idx_users_username ON Users (Username);
CREATE INDEX idx_users_email ON Users (Email);
CREATE INDEX idx_products_categorie_id ON Products (CategorieID);
CREATE INDEX idx_cart_items_username_product_id ON CartItems (Username, ProductID);
CREATE INDEX idx_commands_username ON Commands (Username);
CREATE INDEX idx_order_items_order_id ON OrderItems (OrderID);
CREATE INDEX idx_order_items_product_id ON OrderItems (ProductID);
CREATE INDEX idx_order_items_order_product_id ON OrderItems (OrderID, ProductID);
CREATE INDEX idx_product_reviews_product_id ON ProductReviews (ProductID);
CREATE INDEX idx_product_reviews_product_username ON ProductReviews (ProductID, Username);



