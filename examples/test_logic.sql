CREATE TABLE person (
	id int pk,
	age int,
	name char(100)
);

CREATE PROCEDURE add_person(@id int in, @name char(100) in, @age int in)
BEGIN
	INSERT TABLE person VALUES (@id, @age, @name);
END;

CREATE PROCEDURE get_people_older_than_age(@age int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE age > @age;
END;

CREATE PROCEDURE get_people_younger_than_age(@age int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE age < @age;
END;

CREATE PROCEDURE get_people_older_or_same_age(@age int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE age >= @age;
END;

CREATE PROCEDURE get_people_younger_or_same_age(@age int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE age <= @age;
END;

CREATE PROCEDURE get_people_not_equal_age_1(@age int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE age <> @age;
END;

CREATE PROCEDURE get_people_not_equal_age_2(@age int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE NOT age = @age;
END;

CREATE PROCEDURE get_people_either_age(@age1 int in, @age2 int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE (age = @age1 OR age = @age2) AND (NOT age <= @age1);
END;

CREATE PROCEDURE get_people_less_than_id(@id int in, @name char(100) out)
BEGIN
	SELECT name SET @name FROM person WHERE id < @id;
END;