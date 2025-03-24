USE bennys;

CREATE TABLE POOLTABLES (
    TableID INT NOT NULL UNIQUE,
    IsAvailable BIT NOT NULL DEFAULT 1, -- 1 = Available, 0 = Unavailable
    CONSTRAINT PK_POOLTABLES PRIMARY KEY (TableID)
);

CREATE TABLE RATES (
    RateID INT NOT NULL IDENTITY(1,1),
    RateName VARCHAR(50) NOT NULL,
    Rate DECIMAL(6,2) NOT NULL,
    CONSTRAINT PK_RATES PRIMARY KEY (RateID)
);

CREATE TABLE CUSTOMER (
    CustomerID INT NOT NULL IDENTITY(100,1),
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    PhoneNumber VARCHAR(14) NOT NULL,
    EmailAddress VARCHAR(50) NOT NULL,
    LeagueName VARCHAR(50) NULL,
    CONSTRAINT PK_CUSTOMER PRIMARY KEY (CustomerID)
);

CREATE TABLE POOLRENTAL (
    SessionID INT NOT NULL IDENTITY(1,1),
    RateID INT NOT NULL, 
    CustomerID INT NOT NULL,
    TableID INT NOT NULL,
    RentalDate DATE NOT NULL,
    RentalStart TIME NOT NULL,
    RentalEnd TIME NOT NULL,
    TotalPlayers INT NOT NULL,
    CONSTRAINT PK_POOLRENTAL PRIMARY KEY (SessionID),
    CONSTRAINT FK_POOLRENTAL_CUSTOMER FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID),
    CONSTRAINT FK_POOLRENTAL_RATES FOREIGN KEY (RateID) REFERENCES RATES(RateID),
    CONSTRAINT FK_POOLRENTAL_POOLTABLES FOREIGN KEY (TableID) REFERENCES POOLTABLES(TableID),
);

INSERT INTO POOLTABLES (TableID) 
    VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO RATES (RateName, Rate)
    VALUES 
    ('Standard Weekday', 3.00), 
    ('Standard Weekend', 3.00), 
    ('Friday and Saturday Nights', 5.00),
    ('League', 3.00), 
    ('Weekend Night Group', 15.00);
;

--Prevent overlapping bookings on the same pool table
GO
CREATE TRIGGER PreventOverlap
ON POOLRENTAL
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM POOLRENTAL r
        INNER JOIN inserted i ON r.TableID = i.TableID
        WHERE r.RentalDate = i.RentalDate
            AND (
                (i.RentalStart BETWEEN r.RentalStart AND r.RentalEnd)
                OR
                (i.RentalEnd BETWEEN r.RentalStart AND r.RentalEnd)
                OR
                (r.RentalStart BETWEEN i.RentalStart AND i.RentalEnd)
                )
    )
    BEGIN
        RAISERROR ('Table is already booked for this time.', 16, 1);
        ROLLBACK TRANSACTION;
    END

    --insert rental data if there isn't a conflict
    INSERT INTO POOLRENTAL (RateID, CustomerID, TableID, RentalDate, RentalStart, RentalEnd, TotalPlayers)
    SELECT RateID, CustomerID, TableID, RentalDate, RentalStart, RentalEnd, TotalPlayers
    FROM inserted;

END;

--update the IsAvailable attribute if a table is currently booked
GO
CREATE TRIGGER UpdateAvailabilityBooked
ON POOLRENTAL
AFTER INSERT
AS
BEGIN
    UPDATE POOLTABLES
    SET IsAvailable = 0
    WHERE TableID IN (SELECT TableID FROM inserted);
END;

--update the IsAvailable attribute if a table is no longer booked
GO
CREATE TRIGGER UpdateAvailabilityFree
ON POOLRENTAL
AFTER DELETE
AS
BEGIN
    UPDATE POOLTABLES
    SET IsAvailable = 1
    WHERE TableID IN (SELECT TableID FROM deleted)
    AND NOT EXISTS (
        SELECT 1 FROM POOLRENTAL
        WHERE POOLRENTAL.TableID = POOLTABLES.TableID
        AND RentalEnd > CAST(GETDATE() AS TIME) -- Convert GETDATE() to TIME
    );
END;
