-- Patrons Table
CREATE TABLE Patrons (
patron_id integer auto_increment,
patron_name varchar(50) NOT NULL,
patron_address varchar(50),
PRIMARY KEY(patron_id)
);


-- Loans Table
CREATE TABLE Loans (
patron_id integer NOT NULL,
book_id integer NOT NULL,
librarian_id integer NOT NULL,
loan_date date,
loan_is_active varchar(50)
);


-- Librarians Table
CREATE TABLE Librarians (
librarian_id integer auto_increment,
librarian_name varchar(50),
PRIMARY KEY(librarian_id)
);


-- Books Table
CREATE TABLE Books (
book_id integer auto_increment NOT NULL,
book_title varchar(50) NOT NULL,
book_author varchar(50),
book_publisher varchar(50),
book_genre varchar(50),
PRIMARY KEY(book_id)
);


-- Update Foreign Key Constraints
ALTER TABLE Loans
ADD CONSTRAINT FOREIGN KEY (patron_id)
REFERENCES Patrons (patron_id)
ON DELETE CASCADE,
ADD CONSTRAINT FOREIGN KEY (librarian_id)
REFERENCES Librarian (librarian_id)
ON DELETE CASCADE,
ADD CONSTRAINT FOREIGN KEY (book_id)
REFERENCES Books (book_id)
ON DELETE CASCADE;

-- Insert Sample Data for Loans, Books, Patrons, Librarians
INSERT INTO Books (book_title, book_author, book_genre, book_publisher) 
VALUES 
('Cannery Row', 'John Steinbeck', 'Historical Fiction', 'Viking Press'),
('To Kill A Mockingbird','Harper Lee', 'Southern Gothic Fiction','J. B. Lippincott & Co.'),
('Don Quixote', 'Miguel de Cervantes', 'Novel', 'Francisco de Robles');

Insert into Patrons(patron_name, patron_address)
Values
('John Johnson', '123 Center st.'),
('Steve Smith Sr.', '800 S Mint st.'),
('George Lincoln', '1776 Freedom Way');

Insert Into Librarians(librarian_name)
Values
('Nick'),
('Hiroto'),
('Azuki');

INSERT INTO Loans (book_id, patron_id, librarian_id, loan_is_active, loan_date)
VALUES 
(1, 1, (SELECT librarian_id From Librarians Where librarian_name = 'Nick'), 'Yes', '2021-11-11'),
(2, 2, (SELECT librarian_id From Librarians Where librarian_name = 'Hiroto'), 'No', '2020-1-13'),
(3, 3, (SELECT librarian_id From Librarians Where librarian_name = 'Azuki'), 'Yes', '2021-7-11');
