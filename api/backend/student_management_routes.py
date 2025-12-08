from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


student_management = Blueprint("student_management", __name__)

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
   

