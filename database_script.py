import psycopg2
import os


class DB_Connection():
    """
    Creating connections using envrionment variables and using the deault database named db.
    """

    def __init__(self, host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASS"), database=os.environ.get("DB")):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = "5432"


class PostgreServer():
    def __init__(self, server):
        self.server = server

    def open_connection(self):
        self.conn = psycopg2.connect(
            database=self.server.database,
            user=self.server.user,
            password=self.server.password,
            host=self.server.host,
            port=self.server.port)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_database(self):
        sql = f"DROP DATABASE IF EXISTS {self.server.database};"
        self.cursor.execute(sql)
        sql = f"""
        CREATE DATABASE {self.server.database};
        """
        self.cursor.execute(sql)
        message = "Database created successfully........"
        return message

    def database_name(self):
        return self.server.database

    def drop_tables(self):
        customers = "DROP TABLE IF EXISTS Customers CASCADE;"
        employees = "DROP TABLE IF EXISTS Employees CASCADE;"
        payments = "DROP TABLE IF EXISTS Payments CASCADE;"
        products = "DROP TABLE IF EXISTS Products CASCADE;"
        orders = "DROP TABLE IF EXISTS Orders CASCADE;"

        self.cursor.execute(customers)
        self.cursor.execute(employees)
        self.cursor.execute(payments)
        self.cursor.execute(products)
        self.cursor.execute(orders)

        return "Tables successfully dropped"

    def create_tables(self):
        customers_table = f"""
        CREATE TABLE Customers(
            Id SERIAL PRIMARY KEY,
            FirstName varchar(50) NOT NULL,
            LastName varchar(50) NOT NULL,
            Gender varchar(50) NOT NULL,
            Address varchar(200) NOT NULL,
            Phone varchar(50) NOT NULL,
            Email varchar(100) NOT NULL,
            City varchar(20) NOT NULL,
            Country varchar(50)
        );
        """
        employees_table = f"""
                CREATE TABLE Employees(
                    Id SERIAL PRIMARY KEY,
                    FirstName varchar(50) NOT NULL,
                    LastName varchar(50) NOT NULL,
                    Email varchar(100) NOT NULL,
                    JobTitle varchar(20) NOT NULL
                );
                """

        payments_table = """
                CREATE TABLE Payments(
                    Id SERIAL PRIMARY KEY,
                    CustomerId Integer NOT NULL,
                    PaymentsDate date,
                    Amount Decimal(7,2) NOT NULL,
                    FOREIGN KEY (CustomerId) REFERENCES Customers (Id)
                    );
                    """

        products_table = """
                CREATE TABLE Products(
                    Id SERIAL PRIMARY KEY,
                    ProductName varchar(100) NOT NULL,
                    Description varchar(300) NOT NULL,
                    BuyPrice Decimal(7,2) NOT NULL
                )
                """

        orders_table = """
                CREATE TABLE Orders(
                    Id SERIAL PRIMARY KEY,
                    ProductId INTEGER NOT NULL,
                    PaymentId INTEGER NOT NULL,
                    FulfilledByEmployeeId INTEGER NOT NULL,
                    DateRequired date,
                    DateShipped date,
                    Status varchar(20) NOT NULL,
                    FOREIGN KEY (ProductId) REFERENCES Products (Id),
                    FOREIGN KEY (PaymentId) REFERENCES Payments (Id),
                    FOREIGN KEY (FulfilledByEmployeeId) REFERENCES EmployeEs (Id)
                );
                """
        self.cursor.execute(customers_table)
        self.cursor.execute(employees_table)
        self.cursor.execute(payments_table)
        self.cursor.execute(products_table)
        self.cursor.execute(orders_table)
        self.conn.commit()

        return "All tables successfully created"

    def insert_data(self):
        customers_table = """
        INSERT INTO Customers
        (FirstName, LastName, Gender, Address, Phone, Email, City, Country)
        VALUES
        ('John','Hebert','Male', '284 Chaucer St', '084789657', 'john@gmail.com', 'Johannesburg', 'South Africa'),
        ('Thando','Sithole','Female','240 Sect 1','0794445584','thando@gmail.com','Cape Town','South Africa'),
        ('Leon','Glen','Male','81 Everton Rd,Gillits','0820832830','Leon@gmail.com','Durban','South Africa'),
        ('Charl','Muller','M￼ale','290A Dorset Ecke','+44856872553','Charl.muller@yahoo.com','Berlin','Germany'),
        ('Julia','Stein','Female','22 Wernerring','+448672445058','Js234@yahoo.com','Frankfurt','Germany');
        """

        employees_table = """
        INSERT INTO Employees(FirstName, LastName, Email, JobTitle)
        VALUES
        ('Kani','Matthew','mat@gmail.com','Manager'),
        ('Lesly','Cronje','LesC@gmail.com','Clerk'),
        ('Gideon','Maduku','m@gmail.com','Accountant');
        """

        payments_table = """
        INSERT INTO Payments(CustomerId, PaymentsDate, Amount)
        VALUES
        ('1', '01-09-2018','150.75'),
        ('5', '03-09-2018', '150.75'),
        ('4','03-09-2018', '700.60');
        """
        products_table = """
        INSERT INTO Products(ProductName, Description, BuyPrice) 
        VALUES
        ('Harley Davidson Chopper', 'This replica features working kickstand, front suspension, gear-shift lever', '150.75'),
        ('Classic Car', 'Turnable front wheels, steering function', '550.75'),
        ('Sports car', 'Turnable front wheels, steering function', '700.60');
        """

        orders_table = """
        INSERT INTO Orders(ProductId, PaymentId, FulfilledByEmployeeId, DateRequired, DateShipped, Status)
        VALUES
        ('1', '1', '2', '05-09-2018', NULL, 'Not shipped'),
        ('1', '2', '2', '04-09-2018', '03-09-2018', 'Shipped'),
        ('3', '3', '3', '06-09-2018', NULL, 'Not shipped');
        """

        self.cursor.execute(customers_table)
        self.cursor.execute(employees_table)
        self.cursor.execute(payments_table)
        self.cursor.execute(products_table)
        self.cursor.execute(orders_table)

        self.conn.commit()
        return "Data Successfully Inserted"

    def querying_dastabase(self):
        # SELECT ALL records from table Customers.
        select_all_customers = "SELECT * FROM Customers;"
        self.cursor.execute(select_all_customers)

        # SELECT records only from the name column in the Customers table.
        select_names = "SELECT FirstName FROM Customers;"
        self.cursor.execute(select_names)

        # Show the name of the Customer whose CustomerID is 1.
        Id = "SELECT FirstName FROM Customers WHERE Id = 1;"
        self.cursor.execute(Id)
        # UPDATE the record for CustomerID = 1 on the Customer table so that the name is “Lerato Mabitso”.
        update_name = "UPDATE Customers SET FirstName = 'Lerato', LastName = 'Mabitso' WHERE Id = 1;"
        self.cursor.execute(update_name)

        # DELETE the record from the Customers table for customer 2 (CustomerID = 2).
        delete_customer = "DELETE FROM Customers WHERE Id=2;"
        self.cursor.execute(delete_customer)

        # Select all unique statuses from the Orders table and get a count of the number of orders for each unique status.
        unique_statuses = "select Distinct status, COUNT(status) from Orders GROUP BY status;"
        self.cursor.execute(unique_statuses)

        # Return the MAXIMUM payment made on the PAYMENTS table.
        max_payment = "SELECT MAX(Amount) FROM Payments;"
        self.cursor.execute(max_payment)

        # Select all customers from the “Customers” table, sorted by the “Country” column.
        sort_by_country = "SELECT * FROM Customers ORDER BY Country ASC;"
        self.cursor.execute(sort_by_country)

        # Select all products with a price BETWEEN R100 and R600.
        price_between = "SELECT * FROM Products WHERE BuyPrice BETWEEN 100 AND 600;"
        self.cursor.execute(price_between)

        # Select all fields from “Customers” where country is “Germany” AND city is “Berlin”.
        country_city = "SELECT * FROM Customers WHERE (country='Germany' AND city='Berlin');"
        self.cursor.execute(country_city)

        # Select all fields from “Customers” where city is “Cape Town” OR “Durban”.
        city_or = "SELECT * FROM Customers WHERE (city='Cape Town' OR city='Durban');"
        self.cursor.execute(city_or)

        # Select all records from Products where the Price is GREATER than R500.
        greater_price = "SELECT * FROM Products WHERE Buyprice > 500;"
        self.cursor.execute(greater_price)

        # Return the sum of the Amounts on the Payments table.
        sum_amount = "SELECT SUM(Amount) FROM Payments;"
        self.cursor.execute(sum_amount)

        # Count the number of shipped orders in the Orders table.
        shipped_orders = "SELECT COUNT(Status) FROM Orders WHERE Status='Shipped';"
        self.cursor.execute(shipped_orders)

        # Return the average price of all Products, in Rands and in Dollars (assume the exchange rate is R12 to the Dollar).
        average_price = "SELECT AVG(BuyPrice*12) AS RAND, AVG(BuyPrice/12) AS DOLLARS FROM Products;"
        self.cursor.execute(average_price)

        # Using INNER JOIN create a query that selects all Payments with Customer information.
        inner_join = "SELECT Customers.Id, Customers.FirstName, Customers.Lastname, Customers.Gender,Customers.Address, Customers.Phone, Customers.Email, Customers.City, Customers.Country, Payments.PaymentsDate, Payments.Amount FROM Customers INNER JOIN Payments ON Customers.Id=Payments.Id;"
        self.cursor.execute(inner_join)

        # Select all products that have turnable front wheels.
        turnable_wheels = "SELECT * FROM Products WHERE Description LIKE 'Turnable front wheels%';"
        self.cursor.execute(turnable_wheels)

    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    server = DB_Connection(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB")
    )

    # Open Connection
    postgreserver = PostgreServer(server)
    postgreserver.open_connection()

    # Create Datatbase
    # create_db = postgreserver.create_database()
    # print(create_db)

    # Drop Tables if they Exist
    drop_tables = postgreserver.drop_tables()
    print(drop_tables)

    # Create Tables
    create_tables = postgreserver.create_tables()
    print(create_tables)

    # Insert Data
    insert_data = postgreserver.insert_data()
    print(insert_data)

    # Querying the database
    postgreserver.querying_dastabase()

    # Close Connection
    postgreserver.close_connection()
