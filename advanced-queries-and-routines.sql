drop trigger UpdateProductRatingAfterInsert;

/* Requête pour récupérer les produits les plus populaires (basé sur le nombre total de ventes) */
SELECT p.ProductID, p.Name, p.Description, p.Price, p.Stock,
       SUM(oi.Quantite) AS TotalSales
FROM Products p
JOIN OrderItems oi ON p.ProductID = oi.ProductID
GROUP BY p.ProductID, p.Name, p.Description, p.Price, p.Stock
ORDER BY TotalSales DESC;

/* Query to retrieve top rated products */
SELECT p.ProductID, p.Name AS ProductName, AVG(pr.Note) AS AverageRating
FROM Products p
JOIN ProductReviews pr ON p.ProductID = pr.ProductID
GROUP BY p.ProductID
ORDER BY AverageRating DESC
LIMIT 10;

/* Retrieve all products with their average review rating */
SELECT p.*, AVG(pr.Note) AS AverageRating
FROM Products p
LEFT JOIN ProductReviews pr ON p.ProductID = pr.ProductID
GROUP BY p.ProductID;

/* Retrieve users who have made the most orders */
SELECT u.UserID, u.Name, COUNT(*) AS OrderCount
FROM Users u
JOIN Commands c ON u.UserID = c.UserID
GROUP BY u.UserID
ORDER BY OrderCount DESC
LIMIT 10;

/* Retrieve products with low stock (less than 10 items) */
SELECT *
FROM Products
WHERE Stock < 10;

/* Update product quantity and create order */
DELIMITER //

CREATE PROCEDURE UpdateQuantityAndCreateOrder(
    IN productID INT,
    IN quantity INT,
    IN userID INT
)
BEGIN
    START TRANSACTION;
    
    UPDATE Products
    SET Stock = Stock - quantity
    WHERE ProductID = productID;

    INSERT INTO Commands (UserID, DateCommand, Status)
    VALUES (userID, NOW(), ‘Pending’);

    SET @orderID = LAST_INSERT_ID();

    INSERT INTO OrderItems (OrderID, ProductID, Quantite, PrixUnitaire)
    VALUES (@orderID, productID, quantity, (SELECT Prix FROM Products WHERE ProductID = productID));

    COMMIT;
END;
END //

DELIMITER ;

/* Clear user's cart and update stock after order placement */
DELIMITER //

CREATE PROCEDURE PlaceOrderAndUpdateStock(
    IN username VARCHAR(40)
)
BEGIN
    DECLARE productID INT;
    DECLARE quantity INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT ProductID, Quantity FROM CartItems WHERE Username = username;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO productID, quantity;
        IF done THEN
            LEAVE read_loop;
        END IF;

        UPDATE Products
        SET Stock = Stock - quantity
        WHERE ProductID = productID;

        DELETE FROM CartItems WHERE Username = username AND ProductID = productID;
    END LOOP;
    CLOSE cur;

    COMMIT;
END;
END //

DELIMITER ;

/* Automatically cancel orders with out-of-stock items */
DELIMITER //

CREATE PROCEDURE CancelOrdersWithOutOfStockItems()
BEGIN
    DECLARE order_id INT;
    DECLARE product_id INT;
    DECLARE quantity INT;

    -- Iterate through pending orders
    FOR order_row IN (SELECT OrderID FROM Commands WHERE Status = 'Pending') DO
        SET order_id = order_row.OrderID;

        -- Check if any item in the order is out of stock
        IF EXISTS (SELECT 1 FROM OrderItems oi JOIN Products p ON oi.ProductID = p.ProductID 
                    WHERE oi.OrderID = order_id AND oi.Quantite > p.Stock) THEN
            -- Cancel order
            UPDATE Commands SET Status = 'Cancelled' WHERE OrderID = order_id;
        END IF;
    END FOR;
END //

DELIMITER ;

/* Calculate total sales per category */
DELIMITER //

CREATE PROCEDURE CalculateTotalSalesPerCategory()
BEGIN
    SELECT c.CategoryID, c.Name AS CategoryName, SUM(oi.Quantite * oi.PrixUnitaire) AS TotalSales
    FROM OrderItems oi
    JOIN Products p ON oi.ProductID = p.ProductID
    JOIN Categories c ON p.CategoryID = c.CategoryID
    JOIN Commands o ON oi.OrderID = o.OrderID
    WHERE o.Status = 'Completed'
    GROUP BY c.CategoryID;
END //

DELIMITER ;

/* Trigger to send completion notification when order status changes to 'Completed' */
/* Note: SendCompletionNotification is a hypothetical function that would send a notification to the user */
-- Insert multiple reviews
DELIMITER //

CREATE TRIGGER UpdateStockOnOrder
AFTER INSERT ON OrderItems
FOR EACH ROW
BEGIN
    UPDATE Products
    SET Stock = Stock - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
    IF (SELECT Stock FROM Products WHERE ProductID = NEW.ProductID) < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Stock cannot go below zero.';
    END IF;
END;

DELIMITER ;
