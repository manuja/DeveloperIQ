from flask import Flask
import requests
from flask import Blueprint
import pymysql

product_api = Blueprint('product_api', __name__)

# app = Flask(__name__)

@product_api.route('/products', methods=['POST'])
def create_product():
    # Handle product creation logic
    return "Product created successfully"

@product_api.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    # Handle product retrieval logic
    
    #r = requests.get('https://api.github.com/repos/manuja/LASMS/commits')
    #r = requests.get('https://api.github.com/repos/manuja/LASMS/commits')
    r = requests.get('https://api.github.com/repos/manuja/LASMS/commits?author=manuja')
    
    
    # code for cloud connection



#     # Connect to the database
#     connection = pymysql.connect(
#         host=host,
#         port=port,
#         user=user,
#         password=password,
#         database=database
#     )

#     # Create a cursor object
#     cursor = connection.cursor()


#     create_table_query = '''
# INSERT INTO matrics (matrics, matval)
# VALUES (%s,%s);
# '''

#     cursor.execute(create_table_query,("thatta",len(r.json())))
#     connection.commit()

#        # Execute a SQL query
#     cursor.execute('SELECT * FROM matrics')

#     # Fetch the results
#     results = cursor.fetchall()

#     # Print the results
#     for result in results:
#         return f"Product ID: {result}"

#     # Close the cursor and connection
#     cursor.close()
#     connection.close()

    return f"Product ID: {len(r.json())}"

@product_api.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    # Handle product update logic
    return f"Product ID: {product_id} updated successfully"

@product_api.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Handle product deletion logic
    return f"Product ID: {product_id} deleted successfully"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
