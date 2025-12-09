from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


course_resources = Blueprint("course_resources", __name__)

# GET - Return all courses [Student-5]
@course_resources.route("/course", methods=["GET"])
def get_courses():
    """Get all courses, optionally filtered by department"""
    try:
        department = request.args.get("department")
        
        cursor = db.get_db().cursor()
        
        if department:
            query = """
                SELECT CRN, courseNum, name, department
                FROM Course
                WHERE department = %s
                ORDER BY courseNum
            """
            cursor.execute(query, (department,))
        else:
            query = """
                SELECT CRN, courseNum, name, department
                FROM Course
                ORDER BY department, courseNum
            """
            cursor.execute(query)
        
        courses = cursor.fetchall()
        cursor.close()
        
        return jsonify(courses), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# POST - create a new course [Professor-5]
@course_resources.route("/course", methods=["POST"])
def create_course():
   """Create a new course"""
   try:
       data = request.get_json()
      
       # Validate required fields
       required_fields = ["CRN", "courseNum", "name", "department"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
      
       cursor = db.get_db().cursor()
      
       query = """
           INSERT INTO Course (CRN, courseNum, name, department)
           VALUES (%s, %s, %s, %s)
       """
      
       cursor.execute(query, (
           data["CRN"],
           data["courseNum"],
           data["name"],
           data["department"]
       ))
      
       db.get_db().commit()
       cursor.close()
      
       return jsonify({
           "message": "Course created successfully",
           "CRN": data["CRN"]
       }), 201
   except Error as e:
       return jsonify({"error": str(e)}), 500


# GET - Return course details [Student-5]
@course_resources.route("/course/<int:crn>", methods=["GET"])
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

# GET - Get enrollments for a course [TA-1]
@course_resources.route("/course/<int:crn>/enrollments", methods=["GET"])
def get_course_enrollments(crn):
   """Get all students enrolled in a specific course"""
   try:
       cursor = db.get_db().cursor()

       cursor.execute("SELECT * FROM Course WHERE CRN = %s", (crn,))
       if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Course not found"}), 404
       query = """
            SELECT e.nuID, s.firstName, s.lastName, s.email, e.year, e.semester, e.sectionNum
            FROM EnrollmentIn e
            JOIN Student s ON e.nuID = s.nuID
            WHERE e.CRN = %s
            Order BY s.lastName, s.firstName
       """
       cursor.execute(query, (crn,))
       enrollments = cursor.fetchall()
       cursor.close()
      
       return jsonify(enrollments), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# POST - Enroll a student in a course [TA-1]
@course_resources.route("/course/<int:crn>/enrollments", methods=["POST"])
def enroll_student_in_course(crn):
    """Enroll a student in a specific course"""
    try:
         data = request.get_json()
        
         # Validate required fields
         required_fields = ["nuID", "year", "semester", "sectionNum"]
         for field in required_fields:
              if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
         cursor = db.get_db().cursor()
        
         # Check if course exists
         cursor.execute("SELECT CRN FROM Course WHERE CRN = %s", (crn,))
         if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Course not found"}), 404
            # Check if student exists
         cursor.execute("SELECT nuID FROM Student WHERE nuID = %s", (data["nuID"],))
         if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Student not found"}), 404

         query = """
              INSERT INTO EnrollmentIn (nuID, CRN, year, semester, sectionNum)
              VALUES (%s, %s, %s, %s, %s)
         """
        
         cursor.execute(query, (
              data["nuID"],
              crn,
              data["year"],
              data["semester"],
              data["sectionNum"]
         ))
        
         db.get_db().commit()
         cursor.close()
        
         return jsonify({
              "message": "Student enrolled successfully",
              "nuID": data["nuID"],
              "CRN": crn
         }), 201
    except Error as e:
         return jsonify({"error": str(e)}), 500

# DELETE - Remove a student enrollment from a course [TA-1]
@course_resources.route("/course/<int:crn>/enrollments", methods=["DELETE"])
def remove_student_enrollment(crn):
    """Remove a student's enrollment from a course"""
    try:
        # Get nuID from query parameters or request body
        nuID = request.args.get("nuID")
        if not nuID:
            data = request.get_json()
            nuID = data.get("nuID") if data else None

        if not nuID:
            return jsonify({"error": "Missing required parameter: nuID"}), 400
        
        cursor = db.get_db().cursor()

        # Check if enrollment exists
        cursor.execute("""
            SELECT * FROM EnrollmentIn
            WHERE nuID = %s AND CRN = %s
        """, (nuID, crn))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Enrollment not found"}), 404

        cursor.execute("""
            DELETE FROM EnrollmentIn
            WHERE nuID = %s AND CRN = %s
        """, (nuID, crn))

        db.get_db().commit()
        cursor.close()

        return jsonify({
            "message": "Enrollment removed successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# GET - Return materials for a course [Student-2] [Tutor-3]
@course_resources.route("/resources", methods=["GET"])
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

# # GET - Get specific resource details
# @course_resources.route("/resources/<int:resource_id>", methods=["GET"])
# def get_resource_details(resource_id):
#    """Get details of a specific resource"""
#    try:
#        cursor = db.get_db().cursor()
      
#        cursor.execute("SELECT * FROM Resource WHERE resourceID = %s", (resource_id,))
#        resource = cursor.fetchone()
      
#        if not resource:
#            return jsonify({"error": "Resource not found"}), 404
      
#        cursor.close()
#        return jsonify(resource), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500

# POST - Upload material for a course [Student-2], [Professor-2], [Tutor-5]
@course_resources.route("/resources", methods=["POST"])
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
@course_resources.route("/resources/<int:resource_id>", methods=["PUT"])
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
@course_resources.route("/resources/<int:resource_id>", methods=["DELETE"])
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
@course_resources.route("/topic", methods=["GET"])
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

# PUT - Update topic details [TA-2]
@course_resources.route("/topic/<int:topic_id>", methods=["PUT"])
def update_topic(topic_id):
   """Update an existing topic"""
   try:
       data = request.get_json()

       # Need CRN as part of composite key 
       crn = request.args.get("crn")
       if not crn:
            return jsonify({"error": "Missing required parameter: crn"}), 400

       cursor = db.get_db().cursor()

       # Check if topic exists
       cursor.execute("SELECT * FROM Topic WHERE topicID = %s AND crn = %s", (topic_id, crn))
       if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Topic not found"}), 404

       # Build update query dynamically
       update_fields = []
       params = []
       allowed_fields = ["name"]

       for field in allowed_fields:
           if field in data:
               update_fields.append(f"{field} = %s")
               params.append(data[field])

       if not update_fields:
           cursor.close()
           return jsonify({"error": "No valid fields to update"}), 400

       params.append(topic_id)
       query = f"UPDATE Topic SET {', '.join(update_fields)} WHERE topicID = %s AND crn = %s"

       cursor.execute(query, params)
       db.get_db().commit()
       cursor.close()

       return jsonify({"message": "Topic updated successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500


# For professor pages
# GET - Get courses taught by a professor [Professor-1]
@course_resources.route("/professor/<int:prof_id>/courses", methods=["GET"])
def get_professor_courses(prof_id):
    """Get all courses taught by a specific professor"""
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT c.CRN, c.courseNum, c.name, c.department
            FROM Course c
            JOIN Professor_Course pc ON c.CRN = pc.CRN
            WHERE pc.profID = %s
            ORDER BY c.department, c.courseNum
        """
        
        cursor.execute(query, (prof_id,))
        courses = cursor.fetchall()
        cursor.close()
        
        return jsonify(courses), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET - Get topics and students working on them [Professor-1.1]
@course_resources.route("/course/<int:crn>/topics/students", methods=["GET"])
def get_topics_with_students(crn):
    """Get topics and which students are working on them for a course"""
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT t.topicID, t.name AS topicName, 
                   s.nuID, s.firstName, s.lastName
            FROM Topic t
            JOIN Course c ON t.CRN = c.CRN
            JOIN ProjectGroup pg ON pg.CRN = c.CRN
            JOIN ProjectGroup_Student pgs ON pgs.teamID = pg.teamID
            JOIN Student s ON s.nuID = pgs.nuID
            WHERE c.CRN = %s
            ORDER BY t.name, s.lastName
        """
        
        cursor.execute(query, (crn,))
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET - Get topics and students working on them [Professor-1.1]
@course_resources.route("/course/<int:crn>/topics/students", methods=["GET"])
def get_topics_with_students(crn):
    """Get topics and which students are working on them for a course"""
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT t.topicID, t.name AS topicName, 
                   s.nuID, s.firstName, s.lastName
            FROM Topic t
            JOIN Course c ON t.CRN = c.CRN
            LEFT JOIN ProjectGroup pg ON pg.CRN = c.CRN
            LEFT JOIN ProjectGroup_Student pgs ON pgs.teamID = pg.teamID
            LEFT JOIN Student s ON s.nuID = pgs.nuID
            WHERE c.CRN = %s
            ORDER BY t.name, s.lastName
        """
        
        cursor.execute(query, (crn,))
        results = cursor.fetchall()
        cursor.close()
        
        return jsonify(results), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET - Get courses taught by a professor [Professor-1]
@course_resources.route("/professor/<int:prof_id>/courses", methods=["GET"])
def get_professor_courses(prof_id):
    """Get all courses taught by a specific professor"""
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT c.CRN, c.courseNum, c.name, c.department
            FROM Course c
            JOIN Professor_Course pc ON c.CRN = pc.CRN
            WHERE pc.profID = %s
            ORDER BY c.department, c.courseNum
        """
        
        cursor.execute(query, (prof_id,))
        courses = cursor.fetchall()
        cursor.close()
        
        return jsonify(courses), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500