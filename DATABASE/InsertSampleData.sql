
USE GardenExchange;

-- 1. Insert gardeners
INSERT INTO GARDENER
    (FirstName, LastName, Email, Phone)
VALUES
    ('Ayanda', 'Mbeki', 'ayanda@example.com', '0711111111'),
    ('Lutho', 'Ndlovu', 'lutho@example.com', '0722222222'),
    ('Zanele', 'Jacobs', 'zanele@example.com', '0733333333'),
    ('Thando', 'Peters', 'thando@example.com', '0744444444');

-- 2. Insert garden plots
INSERT INTO GARDEN_PLOT
    (PlotLocation, PlotSize, GardenerID)
VALUES
    ('North Section', 20.00, 1),
    ('South Section', 15.50, 1),
    ('East Section', 18.00, 2),
    ('West Section', 12.00, 3),
    ('Central Section', 25.00, 4);

-- 3. Insert crop types
INSERT INTO CROP
    (CropName, CropCategory)
VALUES
    ('Spinach', 'Leafy Vegetable'),
    ('Carrots', 'Root Vegetable'),
    ('Tomatoes', 'Fruit Vegetable'),
    ('Cabbage', 'Leafy Vegetable');

-- 4. Record crops planted in plots
INSERT INTO PLOT_CROP
    (PlotID, CropID, PlantingDate, GrowingStatus)
VALUES
    (1, 1, '2026-08-01', 'Growing'),
    (1, 2, '2026-08-05', 'Growing'),
    (2, 1, '2026-08-10', 'Harvested'),
    (3, 3, '2026-08-03', 'Harvested'),
    (4, 4, '2026-08-07', 'Harvested'),
    (5, 2, '2026-08-12', 'Harvested'),
    (3, 1, '2026-08-15', 'Growing');

-- 5. Record harvests
INSERT INTO HARVEST
    (PlotCropID, QuantityHarvested, HarvestDate)
VALUES
    (1, 10.00, '2026-09-10'),
    (2, 15.00, '2026-09-12'),
    (3, 20.00, '2026-09-15'),
    (4, 30.00, '2026-09-18'),
    (5, 12.00, '2026-09-20'),
    (6, 25.00, '2026-09-22');

-- 6. Contribute part of each harvest to the exchange
INSERT INTO PRODUCE_EXCHANGE
    (HarvestID, QuantityContributed)
VALUES
    (1, 8.00),
    (2, 12.00),
    (3, 15.00),
    (4, 20.00),
    (5, 10.00),
    (6, 18.00);

-- 7. Register exchange members
INSERT INTO MEMBER
    (FirstName, LastName, Email, Phone)
VALUES
    ('Nomsa', 'Dlamini', 'nomsa@example.com', '0751111111'),
    ('Sipho', 'Khumalo', 'sipho@example.com', '0762222222'),
    ('Lerato', 'Mokoena', 'lerato@example.com', '0773333333'),
    ('Aphiwe', 'Mthembu', 'aphiwe@example.com', '0784444444'),
    ('Buhle', 'Nkosi', 'buhle@example.com', '0795555555');

-- 8. Create collection days
INSERT INTO COLLECTION_DAY
    (CollectionDate, Location)
VALUES
    ('2026-10-15', 'Community Garden Hall'),
    ('2026-10-22', 'Community Garden Hall'),
    ('2026-10-29', 'Community Garden Hall');

-- 9. Record produce requests
INSERT INTO PRODUCE_REQUEST
    (MemberID, ExchangeID, CollectionDayID,
     QuantityRequested, RequestDate, RequestStatus)
VALUES
    (1, 1, 1, 2.00, '2026-10-01', 'Approved'),
    (2, 1, 1, 1.00, '2026-10-02', 'Pending'),
    (3, 2, 1, 3.00, '2026-10-03', 'Collected'),
    (1, 3, 2, 2.00, '2026-10-04', 'Approved'),
    (4, 4, 2, 5.00, '2026-10-05', 'Pending'),
    (5, 5, 3, 2.00, '2026-10-06', 'Rejected'),
    (2, 6, 3, 4.00, '2026-10-07', 'Approved'),
    (3, 3, NULL, 1.00, '2026-10-08', 'Pending');





