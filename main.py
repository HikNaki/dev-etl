import os
import requests
import mysql.connector


# Function to send a request to the API and return the post data
def get_post_data():
    api_url = "https://jsonplaceholder.typicode.com/posts?userId=1"
    response = requests.get(api_url)
    data = response.json()
    return data


# Function to insert post data into the MySQL table
def insert_into_mysql(posts):
    try:
        # Replace the connection parameters with your MySQL database details
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USERNAME"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_NAME"),
        )

        cursor = connection.cursor()

        # Create the posts table if not exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                post_id INT,
                title VARCHAR(255),
                body TEXT
            )
        """
        )

        # Insert post data into the table
        for post in posts:
            cursor.execute(
                """
                INSERT INTO posts (user_id, post_id, title, body)
                VALUES (%s, %s, %s, %s)
            """,
                (post["userId"], post["id"], post["title"], post["body"]),
            )

        connection.commit()
        print("Data inserted successfully into MySQL")

        cursor.close()
        connection.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Step 1: Get post data from the API
    posts_data = get_post_data()

    # Step 2: Extract relevant information and insert into MySQL
    if posts_data:
        insert_into_mysql(posts_data)
    else:
        print("No post data retrieved from the API.")
