from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


student_management = Blueprint("student_management", __name__)

# GET - Return all students [TA-1]
@student_management.route("/students", methods=["GET"])
def get_all_students():
   """Get all students"""
   try:
       current_app.logger.info('Getting all students')
       cursor = db.get_db().cursor()
       
       query = """
           SELECT nuID, firstName, lastName, email, gradYear,
                  classYear, majorOne, majorTwo, minor
           FROM Student
           ORDER BY lastName, firstName
       """
       cursor.execute(query)
       
       students = cursor.fetchall()
       cursor.close()
       
       current_app.logger.info(f'Retrieved {len(students)} students')
       return jsonify(students), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# POST - Add a new student [TA-1]
@student_management.route("/students", methods=["POST"])
def create_student():
   """Create a new student"""
   try:
       current_app.logger.info('Creating new student')
       data = request.get_json()
       
       required_fields = ["nuID", "firstName", "lastName", "email", "gradYear", "majorOne"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
       
       cursor = db.get_db().cursor()
       
       query = """
           INSERT INTO Student (nuID, firstName, lastName, email, gradYear, majorOne, majorTwo, minor)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
       """
       cursor.execute(query, (
           data["nuID"],
           data["firstName"],
           data["lastName"],
           data["email"],
           data["gradYear"],
           data["majorOne"],
           data.get("majorTwo"),
           data.get("minor")
       ))
       
       db.get_db().commit()
       cursor.close()
       
       current_app.logger.info(f'Created student with nuID: {data["nuID"]}')
       return jsonify({
           "message": "Student created successfully",
           "nuID": data["nuID"]
       }), 201
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# GET - Return a student's information [Student-6] [Tutor-4]
@student_management.route("/student/<int:nuid>", methods=["GET"])
def get_student_info(nuid):
   """Get information about a specific student"""
   try:
       current_app.logger.info(f'Getting student info for nuID: {nuid}')
       cursor = db.get_db().cursor()
      
       query = """
           SELECT nuID, firstName, lastName, email, gradYear,
                  classYear, majorOne, majorTwo, minor
           FROM Student
           WHERE nuID = %s
       """
       cursor.execute(query, (nuid,))
       student = cursor.fetchone()
      
       if not student:
           return jsonify({"error": "Student not found"}), 404
      
       cursor.close()
       current_app.logger.info(f'Successfully retrieved student: {nuid}')
       return jsonify(student), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# PUT - Update student information [Student-6] [TA-3]
@student_management.route("/student/<int:nuid>", methods=["PUT"])
def update_student_info(nuid):
   """Update a student's information"""
   try:
       data = request.get_json()
       cursor = db.get_db().cursor()
      
       cursor.execute("SELECT * FROM Student WHERE nuID = %s", (nuid,))
       if not cursor.fetchone():
           return jsonify({"error": "Student not found"}), 404
      
       update_fields = []
       params = []
       allowed_fields = ["firstName", "lastName", "email", "majorOne", "majorTwo", "minor"]
      
       for field in allowed_fields:
           if field in data:
               update_fields.append(f"{field} = %s")
               params.append(data[field])
      
       if not update_fields:
           return jsonify({"error": "No valid fields to update"}), 400
      
       params.append(nuid)
       query = f"UPDATE Student SET {', '.join(update_fields)} WHERE nuID = %s"
      
       cursor.execute(query, params)
       db.get_db().commit()
       cursor.close()
       return jsonify({"message": "Student information updated successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# DELETE - Remove a student [TA-1]
@student_management.route("/students/<int:nuid>", methods=["DELETE"])
def delete_student(nuid):
   """Delete a student from the system"""
   try:
       current_app.logger.info(f'Deleting student with nuID: {nuid}')
       cursor = db.get_db().cursor()
       
       cursor.execute("SELECT * FROM Student WHERE nuID = %s", (nuid,))
       if not cursor.fetchone():
           return jsonify({"error": "Student not found"}), 404
       
       cursor.execute("DELETE FROM Student WHERE nuID = %s", (nuid,))
       db.get_db().commit()
       cursor.close()
       
       current_app.logger.info(f'Successfully deleted student: {nuid}')
       return jsonify({"message": "Student deleted successfully"}), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# POST - Convert student to peer tutor [TA-1]
@student_management.route("/peer_tutors/<int:nuid>", methods=["POST"])
def create_peer_tutor(nuid):
   """Convert a student to a peer tutor"""
   try:
       current_app.logger.info(f'Creating peer tutor from student: {nuid}')
       cursor = db.get_db().cursor()
       
       cursor.execute("SELECT firstName, lastName FROM Student WHERE nuID = %s", (nuid,))
       student = cursor.fetchone()
       
       if not student:
           return jsonify({"error": "Student not found"}), 404
       
       cursor.execute("SELECT * FROM PeerTutor WHERE nuID = %s", (nuid,))
       if cursor.fetchone():
           return jsonify({"error": "Student is already a peer tutor"}), 400
       
       query = """
           INSERT INTO PeerTutor (nuID, firstName, lastName)
           VALUES (%s, %s, %s)
       """
       cursor.execute(query, (nuid, student["firstName"], student["lastName"]))
       
       db.get_db().commit()
       cursor.close()
       
       current_app.logger.info(f'Successfully created peer tutor: {nuid}')
       return jsonify({
           "message": "Peer tutor created successfully",
           "nuID": nuid
       }), 201
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500
   
# adding just for TA Admin functionality
# GET /peer_tutors - get list of peer tutors [TA-3]
@student_management.route("/peer_tutors", methods=["GET"])
def get_peer_tutors():
    """Get all peer tutors"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM PeerTutor ORDER BY lastName, firstName")
        tutors = cursor.fetchall()
        cursor.close()
        return jsonify(tutors), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500