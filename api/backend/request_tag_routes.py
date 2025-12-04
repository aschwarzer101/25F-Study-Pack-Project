from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


students = Blueprint("request tag", __name__)



# POST - Create a request for a session [Student-1]
@students.route("/session_request", methods=["POST"])
def create_session_request():
   """Create a new session request"""
   try:
       data = request.get_json()
      
       # Validate required fields
       required_fields = ["status", "dateCreated", "adminID", "studentIDs"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
      
       cursor = db.get_db().cursor()
      
       # Insert the session request
       query = """
           INSERT INTO SessionRequest (status, dateCreated, adminID)
           VALUES (%s, %s, %s)
       """
      
       cursor.execute(query, (
           data["status"],
           data["dateCreated"],
           data["adminID"]
       ))
      
       request_id = cursor.lastrowid
      
       # Add requesting students
       for student_id in data["studentIDs"]:
           cursor.execute("""
               INSERT INTO Requesting_Students (requestID, nuID)
               VALUES (%s, %s)
           """, (request_id, student_id))
      
       # Add tags if provided
       if "tagIDs" in data:
           for tag_id in data["tagIDs"]:
               cursor.execute("""
                   INSERT INTO Request_Tags (tagID, requestID)
                   VALUES (%s, %s)
               """, (tag_id, request_id))
      
       db.get_db().commit()
       cursor.close()
      
       return jsonify({
           "message": "Session request created successfully",
           "requestID": request_id
       }), 201
   except Error as e:
       return jsonify({"error": str(e)}), 500

