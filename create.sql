CREATE TABLE Users
(netid VARCHAR(6) NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 gender CHAR(1) NOT NULL CHECK(gender IN ('F', 'M', 'O')),
 year SMALLINT NOT NULL CHECK(year IN (2020, 2021, 2022, 2023, 2024)),
 smoking CHAR(1) NOT NULL CHECK(smoking IN ('Y', 'N')),
 sleeping TIME NOT NULL,
 waking TIME NOT NULL,
 room_utility VARCHAR(6) NOT NULL CHECK(room_utility IN ('Study', 'Social')),
 on_campus VARCHAR(3) NOT NULL CHECK(on_campus IN ('Y', 'N')),
 profile_image VARCHAR(64) NOT NULL,
 password_hash VARCHAR(128));

CREATE TABLE House
(name VARCHAR(100) NOT NULL,
 building VARCHAR(100) NOT NULL,
 PRIMARY KEY (name, building));

CREATE TABLE Major
(name VARCHAR(100) NOT NULL,
 school VARCHAR(100) NOT NULL CHECK(school IN ('Pratt School of Engineering', 'Trinity College of Arts and Sciences')),
 PRIMARY KEY(name, school));

CREATE TABLE UserMajor
(netid VARCHAR(6) NOT NULL PRIMARY KEY REFERENCES Users(netid),
 major VARCHAR(100) NOT NULL,
 school VARCHAR(100) NOT NULL,
 FOREIGN KEY(major, school)
 REFERENCES Major(name, school));

CREATE TABLE UserLikes
(netid VARCHAR(6) NOT NULL,
 housename VARCHAR(100) NOT NULL,
 building VARCHAR(100) NOT NULL,
 FOREIGN KEY(housename, building)
 REFERENCES House(name, building),
 PRIMARY KEY(netid, housename, building));

CREATE TABLE Blog_Post
(id INTEGER NOT NULL PRIMARY KEY,
 user_id VARCHAR(6) NOT NULL REFERENCES Users(netid),
 "date" TIMESTAMP NOT NULL,
 title VARCHAR(140) NOT NULL,
 "text" TEXT NOT NULL);


-- Users can be linked to no more than four housing chocies
CREATE FUNCTION TF_Five_Housing_Choices() RETURNS TRIGGER AS $$
BEGIN
  IF ((select COUNT(*) from UserLikes where NEW.netid = UserLikes.netid) = 5)
  THEN RAISE EXCEPTION 'a user can only have 5 housing preferences';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Five_Housing_Choices
  BEFORE INSERT OR UPDATE ON UserLikes
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Five_Housing_Choices();

-- Users who prefer off campus living cannot have an entry in UserLikes
CREATE FUNCTION TF_OffCampusLimit() RETURNS TRIGGER AS $$
BEGIN
    IF(NEW.netid IN (SELECT Users.netid FROM UserLikes, Users WHERE UserLikes.netid = Users.netid AND Users.on_campus = 'N'))
    THEN RAISE EXCEPTION 'if user prefers off campus, cannot have preferences of on-campus housing.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_OffCampusLimit
  BEFORE INSERT OR UPDATE ON UserLikes
  FOR EACH ROW
  EXECUTE PROCEDURE TF_OFFCampusLimit();
