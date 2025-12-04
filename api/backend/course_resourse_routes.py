from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


students = Blueprint("course resources", __name__)

# GET - Return course details [Student-5]
@students.route("/course/<int:crn>", methods=["GET"])
def get_course_details(crn):
   """Get detailed information about a specific course"""
   try:
       cursor = db.get_db().cursor()
       cursor.execute("""
           SELECT CRN, courseNum, name, department
           FROM Course
           WHERE CRN = %s
       """, (crn,))
       course = cursor.fetchone()
      
       if not course:
           return jsonify({"error": "Course not found"}), 404
      
       cursor.close()
       return jsonify(course), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# GET - Return materials for a course [Student-2]
@students.route("/resource", methods=["GET"])
def get_resources():
   """Get all resources, optionally filtered by course CRN"""
   try:
       crn = request.args.get("crn")
       resource_type = request.args.get("type")
      
       cursor = db.get_db().cursor()
      
       query = "SELECT * FROM Resource WHERE 1=1"
       params = []
      
       if crn:
           query += " AND CRN = %s"
           params.append(crn)
      
       if resource_type:
           query += " AND type = %s"
           params.append(resource_type)
      
       query += " ORDER BY dateUploaded DESC"
      
       cursor.execute(query, params)
       resources = cursor.fetchall()
       cursor.close()
      
       return jsonify(resources), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# GET - Get specific resource details
@students.route("/resource/<int:resource_id>", methods=["GET"])
def get_resource_details(resource_id):
   """Get details of a specific resource"""
   try:
       cursor = db.get_db().cursor()
      
       cursor.execute("SELECT * FROM Resource WHERE resourceID = %s", (resource_id,))
       resource = cursor.fetchone()
      
       if not resource:
           return jsonify({"error": "Resource not found"}), 404
      
       cursor.close()
       return jsonify(resource), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# POST - Upload material for a course [Student-2], [Professor-2], [Tutor-5]
@students.route("/resource", methods=["POST"])
def upload_resource():
   """Upload a new course resource"""
   try:
       data = request.get_json()
      
       # Validate required fields
       required_fields = ["resourceID", "name", "type", "dateUploaded", "description", "CRN"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
      
       cursor = db.get_db().cursor()
      
       query = """
           INSERT INTO Resource (resourceID, name, type, dateUploaded, description, CRN)
           VALUES (%s, %s, %s, %s, %s, %s)
       """
      
       cursor.execute(query, (
           data["resourceID"],
           data["name"],
           data["type"],
           data["dateUploaded"],
           data["description"],
           data["CRN"]
       ))
      
       db.get_db().commit()
       cursor.close()
      
       return jsonify({
           "message": "Resource uploaded successfully",
           "resourceID": data["resourceID"]
       }), 201
   except Error as e:
       return jsonify({"error": str(e)}), 500

# PUT - Update details for a course material [Student-2], [Professor-4]
@students.route("/resource/<int:resource_id>", methods=["PUT"])
def update_resource(resource_id):
   """Update an existing resource"""
   try:
       data = request.get_json()
      
       cursor = db.get_db().cursor()
      
       # Check if resource exists
       cursor.execute("SELECT * FROM Resource WHERE resourceID = %s", (resource_id,))
       if not cursor.fetchone():
           return jsonify({"error": "Resource not found"}), 404
      
       # Build update query dynamically
       update_fields = []
       params = []
       allowed_fields = ["name", "type", "description"]
      
       for field in allowed_fields:
           if field in data:
               update_fields.append(f"{field} = %s")
               params.append(data[field])
      
       if not update_fields:
           return jsonify({"error": "No valid fields to update"}), 400
      
       params.append(resource_id)
       query = f"UPDATE Resource SET {', '.join(update_fields)} WHERE resourceID = %s"
      
       cursor.execute(query, params)
       db.get_db().commit()
       cursor.close()
      
       return jsonify({"message": "Resource updated successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# DELETE - Remove a previously uploaded material [Student-2]
@students.route("/resource/<int:resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
   """Delete a resource"""
   try:
       cursor = db.get_db().cursor()
      
       # Check if resource exists
       cursor.execute("SELECT * FROM Resource WHERE resourceID = %s", (resource_id,))
       if not cursor.fetchone():
           return jsonify({"error": "Resource not found"}), 404
      
       cursor.execute("DELETE FROM Resource WHERE resourceID = %s", (resource_id,))
       db.get_db().commit()
       cursor.close()
      
       return jsonify({"message": "Resource deleted successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# GET - See topics that are available [Student-5]
@students.route("/topic", methods=["GET"])
def get_topics():
   """Get all topics, optionally filtered by course CRN"""
   try:
       crn = request.args.get("crn")
      
       cursor = db.get_db().cursor()
      
       if crn:
           query = """
               SELECT crn, topicID, name
               FROM Topic
               WHERE crn = %s
           """
           cursor.execute(query, (crn,))
       else:
           query = "SELECT crn, topicID, name FROM Topic"
           cursor.execute(query)
      
       topics = cursor.fetchall()
       cursor.close()
      
       return jsonify(topics), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

