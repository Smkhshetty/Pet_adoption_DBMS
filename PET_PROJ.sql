CREATE DATABASE PET_PROJ;
USE PET_PROJ;
	CREATE TABLE Users (
		user_id INT PRIMARY KEY AUTO_INCREMENT,
		username VARCHAR(255) NOT NULL UNIQUE,
		password VARCHAR(255) NOT NULL,
		email VARCHAR(255) NOT NULL ,
		first_name VARCHAR(255),
		last_name VARCHAR(255),
		city VARCHAR(255),
		CHECK (CHAR_LENGTH(password) >= 6)
	);
CREATE TABLE Pets (
    pet_id INT PRIMARY KEY AUTO_INCREMENT,
    pet_name VARCHAR(255) NOT NULL,
    breed VARCHAR(255),
    age INT,
    is_lost_found BOOLEAN NOT NULL,
    image_data LONGBLOB 
);


CREATE TABLE AdoptionApplication (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    pet_id INT,
    user_id INT,
    FOREIGN KEY (pet_id) REFERENCES Pets(pet_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_location VARCHAR(255),
    event_description TEXT
);

CREATE TABLE Volunteers (
    volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    event_id INT,

    FOREIGN KEY (user_id) REFERENCES Users(user_id), 
    FOREIGN KEY (event_id) REFERENCES Events(event_id) 
);

show tables in pet_proj;
use pet_proj;


INSERT INTO users (username, password, email,first_name,last_name,city, role)
VALUES ('Admin', 'admin123', 'admin@google.com', 'Sam','Samuel', 'Bangalore', 'ADMIN');


ALTER TABLE users
ADD COLUMN role VARCHAR(50) NOT NULL DEFAULT 'USER';

UPDATE users
SET role = 'USER'
WHERE role IS NULL;

DELIMITER //

CREATE PROCEDURE create_adoption_application_and_update_status(
    IN p_username VARCHAR(255),
    IN p_pet_id INT
)
BEGIN
    DECLARE v_user_id INT;
    DECLARE v_pet_status BOOLEAN;

    -- Get the user_id based on the provided username
    SELECT user_id INTO v_user_id FROM users WHERE username = p_username;

    -- Verify if the pet with the given pet_id is not lost or found
    SELECT is_lost_found INTO v_pet_status FROM pets WHERE pet_id = p_pet_id;

    IF v_user_id IS NOT NULL AND v_pet_status = 0 THEN
        -- Insert the adoption application into the adoptionapplication table
        INSERT INTO adoptionapplication (user_id, pet_id) VALUES (v_user_id, p_pet_id);

        -- Update the adoption_status to 1 in the pets table
        UPDATE pets SET adoption_status = 1 WHERE pet_id = p_pet_id;

        SELECT 'Success' AS result;

    ELSE
        SELECT 'Error' AS result;

    END IF;
END //

DELIMITER ;



INSERT INTO Users (username, password, email, first_name, last_name, city, role)
VALUES
('rahul', 'R@hulP@ss', 'rahul@gmail.com', 'Rahul', 'Sharma', 'Mumbai', 'USER'),
('priya', 'Pr1ya@123', 'priya@gmail.com', 'Priya', 'Verma', 'Delhi', 'USER'),
('arjun', 'Arjun@567', 'arjun@gmail.com', 'Arjun', 'Singh', 'Jaipur', 'USER'),
('admin', 'Admin@123', 'admin@gmail.com', 'Admin', 'Admin', 'AdminCity', 'ADMIN'),
('sneha', 'Sneha@098', 'sneha@gmail.com', 'Sneha', 'Gupta', 'Kolkata', 'USER'),
('aniket', 'Aniket@321', 'aniket@gmail.com', 'Aniket', 'Patil', 'Pune', 'USER'),
('swati', 'Sw@tiPass', 'swati@gmail.com', 'Swati', 'Chopra', 'Chandigarh', 'USER'),
('vikram', 'Vikr@m@456', 'vikram@gmail.com', 'Vikram', 'Reddy', 'Hyderabad', 'USER'),
('tanvi', 'Tanvi@789', 'tanvi@gmail.com', 'Tanvi', 'Rajput', 'Lucknow', 'USER'),
('amit', 'Amit@abc', 'amit@gmail.com', 'Amit', 'Kumar', 'Patna', 'USER');

INSERT INTO Pets (pet_name, breed, age, is_lost_found, image_data)
VALUES
('Tommy', 'Labrador Retriever', 3, 1, NULL),
('Whiskers', 'Persian Cat', 2, 1, NULL),
('Rocky', 'German Shepherd', 1, 1, NULL),
('Mithu', 'Cockatiel', 5, 1, NULL),
('Goldie', 'Betta Fish', 1, 1, NULL),
('Cleo', 'Siamese Cat', 2, 1, NULL),
('Buddy', 'Beagle', 4, 1, NULL),
('Thumper', 'Holland Lop Rabbit', 1, 1, NULL),
('Shelly', 'Red-Eared Slider Turtle', 2, 1, NULL),
('Chikki', 'Syrian Hamster', 1, 1, NULL);

INSERT INTO Events (event_name, event_date, event_location, event_description)
VALUES
('Pet Carnival', '2023-12-01', 'Mumbai', 'Annual pet carnival with fun activities'),
('Adoption Drive', '2023-12-15', 'Delhi', 'Adopt a furry friend for your family'),
('Pet Health Camp', '2023-11-25', 'Jaipur', 'Free health check-ups for pets'),
('Dog Show', '2023-11-30', 'Chandigarh', 'Showcasing the best breeds in the region'),
('Fish Expo', '2023-12-10', 'Kolkata', 'Explore the world of aquariums and fishkeeping'),
('Cat Adoption Fair', '2023-12-05', 'Pune', 'Find a loving home for our feline friends'),
('Paws in the Park', '2023-11-20', 'Hyderabad', 'A day of outdoor fun for pets and owners'),
('Bird Watching Workshop', '2023-11-28', 'Lucknow', 'Learn about different bird species'),
('Rabbit Awareness Session', '2023-12-08', 'Patna', 'Educational session on rabbit care'),
('Hamster Playdate', '2023-12-22', 'Bangalore', 'Bring your hamster for a playdate');

CREATE TABLE AdoptionApplicationLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT,
    submission_timestamp TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES adoptionapplication(application_id)
);

-- Change the delimiter to something else (e.g., $$)
DELIMITER $$

-- Create the trigger
CREATE TRIGGER after_adoption_application_insert
AFTER INSERT ON adoptionapplication
FOR EACH ROW
BEGIN
    -- Insert a record into the AdoptionApplicationLog table for logging
    INSERT INTO AdoptionApplicationLog (application_id, submission_timestamp)
    VALUES (NEW.application_id, NOW());
END $$

-- Change the delimiter back to semicolon
DELIMITER ;

INSERT INTO adoptionapplication (pet_id, user_id)
VALUES
(27,27);

update pets set 
adoption_status=0;
select * from users;
select * from pets;
select * from adoptionapplication;	
select * from events;
select * from volunteers;
select * from AdoptionApplicationLog;

SELECT breed, COUNT(*) AS pet_count
FROM Pets
GROUP BY breed;

 
UPDATE Pets SET age = age + 1 WHERE breed = 'Labrador Retriever';

SELECT pet_name FROM Pets WHERE pet_id IN (SELECT pet_id FROM AdoptionApplication);





