from flask import Flask, request, jsonify
import pymysql.cursors

# Initialize Flask application
app = Flask(__name__)

# Configure MySQL connection
db_host = '<RDS_ENDPOINT>'
db_user = 'admin'
db_password = 'password'
db_name = 'mydatabase'

# Function to create database connection
def get_db_connection():
    return pymysql.connect(host=db_host,
                           user=db_user,
                           password=db_password,
                           db=db_name,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

# Create table if not exists
def create_table():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = '''
            CREATE TABLE IF NOT EXISTS visitors (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            )
            '''
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()

# Endpoint to add a visitor
@app.route('/add_visitor', methods=['POST'])
def add_visitor():
    try:
        visitor_name = request.json['name']
    except KeyError:
        return jsonify({'error': 'Name parameter is required.'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = '''
            INSERT INTO visitors (name)
            VALUES (%s)
            '''
            cursor.execute(sql, (visitor_name,))
            connection.commit()
    finally:
        connection.close()
    
    return jsonify({'message': 'Visitor added successfully.'}), 201

# Endpoint to retrieve all visitors
@app.route('/get_visitors', methods=['GET'])
def get_visitors():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = '''
            SELECT * FROM visitors
            '''
            cursor.execute(sql)
            visitors = cursor.fetchall()
    finally:
        connection.close()

    return jsonify(visitors)

# Initialize database table
create_table()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
