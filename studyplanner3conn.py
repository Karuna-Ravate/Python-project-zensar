import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector
from datetime import datetime

# Database connection configuration
Db_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "karuna1864",
    "database": "studyplanner"
}

# Function to establish a connection to the database


def get_db_connection():
    return mysql.connector.connect(**Db_CONFIG)

# Serialize datetime objects to ISO 8601 string format


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

# Recursively serialize datetime objects inside nested structures (e.g., lists, dictionaries)


def recursive_serialize(obj):
    if isinstance(obj, dict):
        return {key: recursive_serialize(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [recursive_serialize(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj

# Request handler class to handle incoming requests


class RequestHandler(BaseHTTPRequestHandler):

    # Handle GET requests
    def do_GET(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Route: Get Users
            if self.path.startswith("/users/"):
                user_id = self.path.split("/")[-1]
                cursor.execute(
                    "SELECT * FROM Users WHERE UserID = %s", (user_id,))
                result = cursor.fetchone()
                if result is None:
                    self.send_error(404, "User Not Found")
                    return
            elif self.path == "/users":
                cursor.execute("SELECT * FROM Users")
                result = cursor.fetchall()

            # Route: Get Subjects
            elif self.path.startswith("/subjects/"):
                subject_id = self.path.split("/")[-1]
                cursor.execute(
                    "SELECT * FROM Subjects WHERE SubjectID = %s", (subject_id,))
                result = cursor.fetchone()
                if result is None:
                    self.send_error(404, "Subject Not Found")
                    return
            elif self.path == "/subjects":
                cursor.execute("SELECT * FROM Subjects")
                result = cursor.fetchall()

            # Route: Get Study Plans
            elif self.path.startswith("/studyplans/"):
                plan_id = self.path.split("/")[-1]
                cursor.execute(
                    "SELECT * FROM StudyPlans WHERE PlanID = %s", (plan_id,))
                result = cursor.fetchone()
                if result is None:
                    self.send_error(404, "Study Plan Not Found")
                    return
            elif self.path == "/studyplans":
                cursor.execute("SELECT * FROM StudyPlans")
                result = cursor.fetchall()

            # Route: Get Study Sessions
            elif self.path.startswith("/studysessions/"):
                session_id = self.path.split("/")[-1]
                cursor.execute(
                    "SELECT * FROM StudySessions WHERE SessionID = %s", (session_id,))
                result = cursor.fetchone()
                if result is None:
                    self.send_error(404, "Study Session Not Found")
                    return
            elif self.path == "/studysessions":
                cursor.execute("SELECT * FROM StudySessions")
                result = cursor.fetchall()

            # Route: Get Progress
            elif self.path.startswith("/progress/"):
                progress_id = self.path.split("/")[-1]
                cursor.execute(
                    "SELECT * FROM Progress WHERE ProgressID = %s", (progress_id,))
                result = cursor.fetchone()
                if result is None:
                    self.send_error(404, "Progress Not Found")
                    return
            elif self.path == "/progress":
                cursor.execute("SELECT * FROM Progress")
                result = cursor.fetchall()

            else:
                # Invalid Route
                self.send_error(404, "Invalid Endpoint")
                return

            # Serialize datetime fields and send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Recursively serialize result to handle datetime objects
            serialized_result = json.dumps(recursive_serialize(result))

            self.wfile.write(serialized_result.encode())

        except Exception as e:
            # Handle Errors
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

    # Handle POST requests
    def do_POST(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Route: Insert User
            if self.path == "/users":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)

                cursor.execute(
                    "INSERT INTO Users (UserName, Password, Email) VALUES (%s, %s, %s)",
                    (data["UserName"], data["Password"], data["Email"])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(
                    {"message": "User created successfully!"}).encode())

            # Route: Insert Subject
            elif self.path == "/subjects":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)

                cursor.execute(
                    "INSERT INTO Subjects (UserID, SubjectName, HoursPerWeek) VALUES (%s, %s, %s)",
                    (data["UserID"], data["SubjectName"], data["HoursPerWeek"])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(
                    {"message": "Subject created successfully!"}).encode())

            # Route: Insert Study Plan
            elif self.path == "/studyplans":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)

                cursor.execute(
                    "INSERT INTO StudyPlans (UserID, StartDate, EndDate, Goal) VALUES (%s, %s, %s, %s)",
                    (data["UserID"], data["StartDate"],
                     data["EndDate"], data["Goal"])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(
                    {"message": "Study Plan created successfully!"}).encode())

            # Route: Insert Study Session
            elif self.path == "/studysessions":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)

                cursor.execute(
                    "INSERT INTO StudySessions (PlanID, SessionDate, SubjectName, DurationInHours) VALUES (%s, %s, %s, %s)",
                    (data["PlanID"], data["SessionDate"],
                     data["SubjectName"], data["DurationInHours"])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(
                    {"message": "Study Session created successfully!"}).encode())

            # Route: Insert Progress
            elif self.path == "/progress":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)

                cursor.execute(
                    "INSERT INTO Progress (UserID, PlanID, SessionID, Completed) VALUES (%s, %s, %s, %s)",
                    (data["UserID"], data["PlanID"],
                     data["SessionID"], data["Completed"])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(
                    {"message": "Progress recorded successfully!"}).encode())

            else:
                # Invalid Route
                self.send_error(404, "Invalid Endpoint")
                return

        except Exception as e:
            # Handle Errors
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

# Function to run the HTTP server


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


# Main execution
if __name__ == "__main__":
    run()
