CREATE DATABASE GardenExchange;

USE GardenExchange;


-- 1. GARDENER
CREATE TABLE GARDENER (
    GardenerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(20)
);

-- 2. GARDEN_PLOT
CREATE TABLE GARDEN_PLOT (
    PlotID INT AUTO_INCREMENT PRIMARY KEY,
    PlotLocation VARCHAR(100) NOT NULL,
    PlotSize DECIMAL(8,2) NOT NULL,
    GardenerID INT NOT NULL,

    CONSTRAINT chk_plot_size
        CHECK (PlotSize > 0),

    CONSTRAINT fk_plot_gardener
        FOREIGN KEY (GardenerID)
        REFERENCES GARDENER(GardenerID)
);

-- 3. CROP
CREATE TABLE CROP (
    CropID INT AUTO_INCREMENT PRIMARY KEY,
    CropName VARCHAR(60) NOT NULL,
    CropCategory VARCHAR(50) NOT NULL
);

-- 4. PLOT_CROP: bridge between plots and crops
CREATE TABLE PLOT_CROP (
    PlotCropID INT AUTO_INCREMENT PRIMARY KEY,
    PlotID INT NOT NULL,
    CropID INT NOT NULL,
    PlantingDate DATE NOT NULL,
    GrowingStatus VARCHAR(20) NOT NULL DEFAULT 'Growing',

    CONSTRAINT uq_plot_crop_planting
        UNIQUE (PlotID, CropID, PlantingDate),

    CONSTRAINT chk_growing_status
        CHECK (GrowingStatus IN
            ('Growing', 'Harvested', 'Failed')),

    CONSTRAINT fk_planting_plot
        FOREIGN KEY (PlotID)
        REFERENCES GARDEN_PLOT(PlotID),

    CONSTRAINT fk_planting_crop
        FOREIGN KEY (CropID)
        REFERENCES CROP(CropID)
);

-- 5. HARVEST
CREATE TABLE HARVEST (
    HarvestID INT AUTO_INCREMENT PRIMARY KEY,
    PlotCropID INT NOT NULL,
    QuantityHarvested DECIMAL(10,2) NOT NULL,
    HarvestDate DATE NOT NULL,

    CONSTRAINT chk_harvest_quantity
        CHECK (QuantityHarvested > 0),

    CONSTRAINT fk_harvest_planting
        FOREIGN KEY (PlotCropID)
        REFERENCES PLOT_CROP(PlotCropID)
);

-- 6. PRODUCE_EXCHANGE
CREATE TABLE PRODUCE_EXCHANGE (
    ExchangeID INT AUTO_INCREMENT PRIMARY KEY,
    HarvestID INT NOT NULL,
    QuantityContributed DECIMAL(10,2) NOT NULL,

    CONSTRAINT chk_contributed_quantity
        CHECK (QuantityContributed > 0),

    CONSTRAINT fk_exchange_harvest
        FOREIGN KEY (HarvestID)
        REFERENCES HARVEST(HarvestID)
);

-- 7. MEMBER
CREATE TABLE MEMBER (
    MemberID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(20)
);

-- 8. COLLECTION_DAY
CREATE TABLE COLLECTION_DAY (
    CollectionDayID INT AUTO_INCREMENT PRIMARY KEY,
    CollectionDate DATE NOT NULL,
    Location VARCHAR(100) NOT NULL
);

-- 9. PRODUCE_REQUEST
CREATE TABLE PRODUCE_REQUEST (
    RequestID INT AUTO_INCREMENT PRIMARY KEY,
    MemberID INT NOT NULL,
    ExchangeID INT NOT NULL,
    CollectionDayID INT NULL,
    QuantityRequested DECIMAL(10,2) NOT NULL,
    RequestDate DATE NOT NULL,
    RequestStatus VARCHAR(20) NOT NULL DEFAULT 'Pending',

    CONSTRAINT chk_requested_quantity
        CHECK (QuantityRequested > 0),

    CONSTRAINT chk_request_status
        CHECK (RequestStatus IN
            ('Pending', 'Approved', 'Rejected', 'Collected')),

    CONSTRAINT fk_request_member
        FOREIGN KEY (MemberID)
        REFERENCES MEMBER(MemberID),

    CONSTRAINT fk_request_exchange
        FOREIGN KEY (ExchangeID)
        REFERENCES PRODUCE_EXCHANGE(ExchangeID),

    CONSTRAINT fk_request_collection_day
        FOREIGN KEY (CollectionDayID)
        REFERENCES COLLECTION_DAY(CollectionDayID)
);


