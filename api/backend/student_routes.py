from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


students = Blueprint("students", __name__)


# GET - Return a student's information [Student-6]
@students.route("/student/<int:nuid>", methods=["GET"])
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


# PUT - Update student information [Student-6]
@students.route("/student/<int:nuid>", methods=["PUT"])
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


#SHOULD GO INTO COURSES
# GET - Return course details [Student-5]
# @students.route("/course/<int:crn>", methods=["GET"])
# def get_course_details(crn):
#    """Get detailed information about a specific course"""
#    try:
#        cursor = db.get_db().cursor()
#        cursor.execute("""
#            SELECT CRN, courseNum, name, department
#            FROM Course
#            WHERE CRN = %s
#        """, (crn,))
#        course = cursor.fetchone()
      
#        if not course:
#            return jsonify({"error": "Course not found"}), 404
      
#        cursor.close()
#        return jsonify(course), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500


# SHOULD BE IN TEACHING ASSISTANT
# # GET - Return a teaching assistant's information [Student-3]
# @students.route("/teaching_assistant/<int:ta_nuid>", methods=["GET"])
# def get_ta_info(ta_nuid):
#    """Get information about a specific teaching assistant"""
#    try:
#        cursor = db.get_db().cursor()
      
#        query = """
#            SELECT nuID, firstName, lastName, email, crn
#            FROM TeachingAssistant
#            WHERE nuID = %s
#        """
      
#        cursor.execute(query, (ta_nuid,))
#        ta = cursor.fetchone()
      
#        if not ta:
#            return jsonify({"error": "Teaching assistant not found"}), 404
      
#        cursor.close()
#        return jsonify(ta), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



#SHOULD BE IN STUDY SESSIONS
# # GET - Return all active study sessions [Student-4]
# @students.route("/study_session", methods=["GET"])
# def get_study_sessions():
#    """Get all active study sessions, optionally filtered by course or topic"""
#    try:
#        current_app.logger.info('Getting study sessions')
      
#        course_crn = request.args.get("course")
#        topic_name = request.args.get("topic")
      
#        cursor = db.get_db().cursor()
      
#        query = """
#            SELECT DISTINCT ss.sessionID, ss.date, ss.startTime, ss.endTime,
#                   sl.building, sl.room, sl.capacity
#            FROM StudySession ss
#            JOIN StudyLocation sl ON ss.locID = sl.locID
#        """
      
#        params = []
#        where_clauses = ["ss.date >= CURDATE()"]
      
#        current_app.logger.info(f'Retrieved {len(sessions)} study sessions')
#        return jsonify(sessions), 200
#    except Error as e:
#        current_app.logger.error(f'Database error: {str(e)}')
#        return jsonify({"error": str(e)}), 500



# SHOULD BE MOVED TO STUDY SESSION(?)
# POST - Start a study session [Student-1]
# @students.route("/study_session", methods=["POST"])
# def create_study_session():
#    """Create a new study session"""
#    try:
#        data = request.get_json()
      
#        # Validate required fields
#        required_fields = ["sessionID", "locID", "startTime", "endTime", "date", "studentID"]
#        for field in required_fields:
#            if field not in data:
#                return jsonify({"error": f"Missing required field: {field}"}), 400
      
#        cursor = db.get_db().cursor()
      
#        query = """
#            INSERT INTO StudySession (sessionID, locID, startTime, endTime, date, studentID)
#            VALUES (%s, %s, %s, %s, %s, %s)
#        """
#        cursor.execute(query, (
#            data["sessionID"],
#            data["locID"],
#            data["startTime"],
#            data["endTime"],
#            data["date"],
#            data["studentID"]
#        ))
      
#        db.get_db().commit()
#        cursor.close()
#        return jsonify({
#            "message": "Study session created successfully",
#            "sessionID": data["sessionID"]
#        }), 201
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# SHOULD BE MOVED TO STUDY SESSION
# PUT - Update details for a study session [Student-1]
# @students.route("/study_session/<int:session_id>", methods=["PUT"])
# def update_study_session(session_id):
#    """Update an existing study session"""
#    try:
#        data = request.get_json()
      
#        cursor = db.get_db().cursor()
#                cursor.execute("SELECT * FROM StudySession WHERE sessionID = %s", (session_id,))
#        if not cursor.fetchone():
#            return jsonify({"error": "Study session not found"}), 404
      
#        update_fields = []
#        params = []
#        allowed_fields = ["locID", "startTime", "endTime", "date"]
      
#        for field in allowed_fields:
#            if field in data:
#                update_fields.append(f"{field} = %s")
#                params.append(data[field])
      
#        if not update_fields:
#            return jsonify({"error": "No valid fields to update"}), 400
      
#        params.append(session_id)
#        query = f"UPDATE StudySession SET {', '.join(update_fields)} WHERE sessionID = %s"
      
#        cursor.execute(query, params)
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({"message": "Study session updated successfully"}), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



#
# DELETE - Cancel a study session [Student-1]
# @students.route("/study_session/<int:session_id>", methods=["DELETE"])
# def delete_study_session(session_id):
#    """Cancel/delete a study session"""
#    try:
#        cursor = db.get_db().cursor()
      
#        # Check if session exists
#        cursor.execute("SELECT * FROM StudySession WHERE sessionID = %s", (session_id,))
#        if not cursor.fetchone():
#            return jsonify({"error": "Study session not found"}), 404
      
#        cursor.execute("DELETE FROM StudySession WHERE sessionID = %s", (session_id,))
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({"message": "Study session cancelled successfully"}), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# SHOULD BE ASSOCIATED WITH RESOURCE
# # GET - Return materials for a course [Student-2]
# @students.route("/resource", methods=["GET"])
# def get_resources():
#    """Get all resources, optionally filtered by course CRN"""
#    try:
#        crn = request.args.get("crn")
#        resource_type = request.args.get("type")
      
#        cursor = db.get_db().cursor()
      
#        query = "SELECT * FROM Resource WHERE 1=1"
#        params = []
      
#        if crn:
#            query += " AND CRN = %s"
#            params.append(crn)
      
#        if resource_type:
#            query += " AND type = %s"
#            params.append(resource_type)
      
#        query += " ORDER BY dateUploaded DESC"
      
#        cursor.execute(query, params)
#        resources = cursor.fetchall()
#        cursor.close()
      
#        return jsonify(resources), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# SHOULD BE ASSOCIATED WITH RESOURCE
# # GET - Get specific resource details
# @students.route("/resource/<int:resource_id>", methods=["GET"])
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




# # POST - Upload material for a course [Student-2], [Professor-2], [Tutor-5]
# @students.route("/resource", methods=["POST"])
# def upload_resource():
#    """Upload a new course resource"""
#    try:
#        data = request.get_json()
      
#        # Validate required fields
#        required_fields = ["resourceID", "name", "type", "dateUploaded", "description", "CRN"]
#        for field in required_fields:
#            if field not in data:
#                return jsonify({"error": f"Missing required field: {field}"}), 400
      
#        cursor = db.get_db().cursor()
      
#        query = """
#            INSERT INTO Resource (resourceID, name, type, dateUploaded, description, CRN)
#            VALUES (%s, %s, %s, %s, %s, %s)
#        """
      
#        cursor.execute(query, (
#            data["resourceID"],
#            data["name"],
#            data["type"],
#            data["dateUploaded"],
#            data["description"],
#            data["CRN"]
#        ))
      
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({
#            "message": "Resource uploaded successfully",
#            "resourceID": data["resourceID"]
#        }), 201
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



#SHOULD BE UNDER RESOURCE
# # PUT - Update details for a course material [Student-2], [Professor-4]
# @students.route("/resource/<int:resource_id>", methods=["PUT"])
# def update_resource(resource_id):
#    """Update an existing resource"""
#    try:
#        data = request.get_json()
      
#        cursor = db.get_db().cursor()
      
#        # Check if resource exists
#        cursor.execute("SELECT * FROM Resource WHERE resourceID = %s", (resource_id,))
#        if not cursor.fetchone():
#            return jsonify({"error": "Resource not found"}), 404
      
#        # Build update query dynamically
#        update_fields = []
#        params = []
#        allowed_fields = ["name", "type", "description"]
      
#        for field in allowed_fields:
#            if field in data:
#                update_fields.append(f"{field} = %s")
#                params.append(data[field])
      
#        if not update_fields:
#            return jsonify({"error": "No valid fields to update"}), 400
      
#        params.append(resource_id)
#        query = f"UPDATE Resource SET {', '.join(update_fields)} WHERE resourceID = %s"
      
#        cursor.execute(query, params)
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({"message": "Resource updated successfully"}), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# SHOULD BE UNDER RESOURCE
# # DELETE - Remove a previously uploaded material [Student-2]
# @students.route("/resource/<int:resource_id>", methods=["DELETE"])
# def delete_resource(resource_id):
#    """Delete a resource"""
#    try:
#        cursor = db.get_db().cursor()
      
#        # Check if resource exists
#        cursor.execute("SELECT * FROM Resource WHERE resourceID = %s", (resource_id,))
#        if not cursor.fetchone():
#            return jsonify({"error": "Resource not found"}), 404
      
#        cursor.execute("DELETE FROM Resource WHERE resourceID = %s", (resource_id,))
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({"message": "Resource deleted successfully"}), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# SHOULD BE UNDER TOPIC (if we keep the file)
# # GET - See topics that are available [Student-5]
# @students.route("/topic", methods=["GET"])
# def get_topics():
#    """Get all topics, optionally filtered by course CRN"""
#    try:
#        crn = request.args.get("crn")
      
#        cursor = db.get_db().cursor()
      
#        if crn:
#            query = """
#                SELECT crn, topicID, name
#                FROM Topic
#                WHERE crn = %s
#            """
#            cursor.execute(query, (crn,))
#        else:
#            query = "SELECT crn, topicID, name FROM Topic"
#            cursor.execute(query)
      
#        topics = cursor.fetchall()
#        cursor.close()
      
#        return jsonify(topics), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500




# GET - Return members in a group and their details [Student-6]
@students.route("/project_group/<int:team_id>/members", methods=["GET"])
def get_project_group_members(team_id):
   """Get all members of a project group with their contact information"""
   try:
       crn = request.args.get("crn")
      
       if not crn:
           return jsonify({"error": "Missing required parameter: crn"}), 400
      
       cursor = db.get_db().cursor()
      
       # Check if project group exists
       cursor.execute("""
           SELECT * FROM ProjectGroup
           WHERE teamID = %s AND CRN = %s
       """, (team_id, crn))
      
       if not cursor.fetchone():
           return jsonify({"error": "Project group not found"}), 404
      
       # Get group members with contact info
       query = """
           SELECT pgs.firstName, pgs.lastName, s.email, s.nuID
           FROM ProjectGroup_Student pgs
           JOIN Student s ON pgs.nuID = s.nuID
           WHERE pgs.teamID = %s AND pgs.CRN = %s
       """
      
       cursor.execute(query, (team_id, crn))
       members = cursor.fetchall()
       cursor.close()
      
       return jsonify(members), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500




# GET - Get all project groups for a course
@students.route("/project_group", methods=["GET"])
def get_project_groups():
   """Get all project groups, optionally filtered by course CRN"""
   try:
       crn = request.args.get("crn")
      
       cursor = db.get_db().cursor()
      
       if crn:
           query = """
               SELECT teamID, CRN, teamName
               FROM ProjectGroup
               WHERE CRN = %s
           """
           cursor.execute(query, (crn,))
       else:
           query = "SELECT teamID, CRN, teamName FROM ProjectGroup"
           cursor.execute(query)
      
       groups = cursor.fetchall()
       cursor.close()
      
       return jsonify(groups), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500




# POST - Create a project group [Student-6]
@students.route("/project_group", methods=["POST"])
def create_project_group():
   """Create a new project group"""
   try:
       data = request.get_json()
      
       # Validate required fields
       required_fields = ["teamID", "CRN", "teamName"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
      
       cursor = db.get_db().cursor()
      
       query = """
           INSERT INTO ProjectGroup (teamID, CRN, teamName)
           VALUES (%s, %s, %s)
       """
      
       cursor.execute(query, (
           data["teamID"],
           data["CRN"],
           data["teamName"]
       ))
      
       db.get_db().commit()
       cursor.close()
      
       return jsonify({
           "message": "Project group created successfully",
           "teamID": data["teamID"]
       }), 201
   except Error as e:
       return jsonify({"error": str(e)}), 500




# PUT - Edit a project group [Student-6]
@students.route("/project_group/<int:team_id>", methods=["PUT"])
def update_project_group(team_id):
   """Update a project group's information"""
   try:
       data = request.get_json()
       crn = request.args.get("crn")
      
       if not crn:
           return jsonify({"error": "Missing required parameter: crn"}), 400
      
       cursor = db.get_db().cursor()
      
       # Check if project group exists
       cursor.execute("""
           SELECT * FROM ProjectGroup
           WHERE teamID = %s AND CRN = %s
       """, (team_id, crn))
      
       if not cursor.fetchone():
           return jsonify({"error": "Project group not found"}), 404
      
       # Only teamName can be updated
       if "teamName" not in data:
           return jsonify({"error": "No valid fields to update"}), 400
      
       query = """
           UPDATE ProjectGroup
           SET teamName = %s
           WHERE teamID = %s AND CRN = %s
       """
      
       cursor.execute(query, (data["teamName"], team_id, crn))
       db.get_db().commit()
       cursor.close()
      
       return jsonify({"message": "Project group updated successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500




# DELETE - Delete a project group [Student-6]
@students.route("/project_group/<int:team_id>", methods=["DELETE"])
def delete_project_group(team_id):
   """Delete a project group"""
   try:
       crn = request.args.get("crn")
      
       if not crn:
           return jsonify({"error": "Missing required parameter: crn"}), 400
      
       cursor = db.get_db().cursor()
      
       # Check if project group exists
       cursor.execute("""
           SELECT * FROM ProjectGroup
           WHERE teamID = %s AND CRN = %s
       """, (team_id, crn))
      
       if not cursor.fetchone():
           return jsonify({"error": "Project group not found"}), 404
      
       cursor.execute("""
           DELETE FROM ProjectGroup
           WHERE teamID = %s AND CRN = %s
       """, (team_id, crn))
      
       db.get_db().commit()
       cursor.close()
      
       return jsonify({"message": "Project group deleted successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500




# --------------------------------------------------
# /session_request RESOURCE
# --------------------------------------------------

# SHOULD PUT IN SESSION POSSIBLY
# # POST - Create a request for a session [Student-1]
# @students.route("/session_request", methods=["POST"])
# def create_session_request():
#    """Create a new session request"""
#    try:
#        data = request.get_json()
      
#        # Validate required fields
#        required_fields = ["status", "dateCreated", "adminID", "studentIDs"]
#        for field in required_fields:
#            if field not in data:
#                return jsonify({"error": f"Missing required field: {field}"}), 400
      
#        cursor = db.get_db().cursor()
      
#        # Insert the session request
#        query = """
#            INSERT INTO SessionRequest (status, dateCreated, adminID)
#            VALUES (%s, %s, %s)
#        """
      
#        cursor.execute(query, (
#            data["status"],
#            data["dateCreated"],
#            data["adminID"]
#        ))
      
#        request_id = cursor.lastrowid
      
#        # Add requesting students
#        for student_id in data["studentIDs"]:
#            cursor.execute("""
#                INSERT INTO Requesting_Students (requestID, nuID)
#                VALUES (%s, %s)
#            """, (request_id, student_id))
      
#        # Add tags if provided
#        if "tagIDs" in data:
#            for tag_id in data["tagIDs"]:
#                cursor.execute("""
#                    INSERT INTO Request_Tags (tagID, requestID)
#                    VALUES (%s, %s)
#                """, (tag_id, request_id))
      
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({
#            "message": "Session request created successfully",
#            "requestID": request_id
#        }), 201
#    except Error as e:
#        return jsonify({"error": str(e)}), 500




# # GET - Return locations of active study sessions [Student-4]
# @students.route("/study_location", methods=["GET"])
# def get_study_locations():
#    """Get all study locations with active sessions"""
#    try:
#        # Optional filter parameters
#        building = request.args.get("building")
#        active_only = request.args.get("active_only", "true").lower() == "true"
      
#        cursor = db.get_db().cursor()
      
#        query = """
#            SELECT DISTINCT sl.locID, sl.building, sl.room,
#                   sl.capacity, sl.status
#            FROM StudyLocation sl
#        """
      
#        params = []
#        where_clauses = []
      
#        if active_only:
#            query += """
#                JOIN StudySession ss ON sl.locID = ss.locID
#            """
#            where_clauses.append("ss.date >= CURDATE()")
      
#        if building:
#            where_clauses.append("sl.building = %s")
#            params.append(building)
      
#        if where_clauses:
#            query += " WHERE " + " AND ".join(where_clauses)
      
#        query += " ORDER BY sl.building, sl.room"
      
#        cursor.execute(query, params)
#        locations = cursor.fetchall()
#        cursor.close()
      
#        return jsonify(locations), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# SHOULD BE IN STUDY LOCATION
# # GET - Get specific location details
# @students.route("/study_location/<int:loc_id>", methods=["GET"])
# def get_study_location_details(loc_id):
#    """Get details of a specific study location"""
#    try:
#        cursor = db.get_db().cursor()
      
#        cursor.execute("""
#            SELECT locID, building, room, capacity, status
#            FROM StudyLocation
#            WHERE locID = %s
#        """, (loc_id,))
      
#        location = cursor.fetchone()
      
#        if not location:
#            return jsonify({"error": "Study location not found"}), 404
      
#        # Get upcoming sessions at this location
#        cursor.execute("""
#            SELECT sessionID, date, startTime, endTime
#            FROM StudySession
#            WHERE locID = %s AND date >= CURDATE()
#            ORDER BY date, startTime
#        """, (loc_id,))
      
#        sessions = cursor.fetchall()
#        location["upcoming_sessions"] = sessions
      
#        cursor.close()
#        return jsonify(location), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500

