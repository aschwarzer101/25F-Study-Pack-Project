from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


session_info = Blueprint("session_info", __name__)

# # Get all study locations with optional filtering by status/building
# # (example checking status of rooms in Snell)

# @study_locations.route("/study_locations", methods=["GET"])
# def get_all_study_locations():
#     """
#     Get all study locations 
#     Can filter by status (active/inactive) and building
#     """

#     try: 
#         current_app.logger.info('Starting get_all_study_locations request')
#         cursor = db.get_db().cursor()

#         # params
#         status = request.args.get("status")
#         building = request.args.get("building")
#         #query
#         query = "SELECT * FROM StudyLocation WHERE 1=1"
#         params = []

#             # adding filters if there 
#         if status is not None:
#             query += " AND status = %s"
#             params.append(status)
#         if building:
#             query += " AND building = %s"
#             params.append(building)

#         cursor.execute(query, params)
#         locations = cursor.fetchall()
#         cursor.close()

#         current_app.logger.info(f'retrieved {len(locations)} locations')
#         return jsonify(locations), 200
#     except Error as e: 
#         current_app.logger.error(f'error in getting locations alayna : {str(e)}')
#         return jsonify({"error" : str(e)}), 500
    
# GET - Return locations of active study sessions [Student-4] [Tutor-1]
@session_info.route("/study_location", methods=["GET"])
def get_study_locations():
   """Get all study locations with active sessions"""
   try:
       # Optional filter parameters
       building = request.args.get("building")
       active_only = request.args.get("active_only", "true").lower() == "true"
      
       cursor = db.get_db().cursor()
      
       query = """
           SELECT DISTINCT sl.locID, sl.building, sl.room,
                  sl.capacity, sl.status
           FROM StudyLocation sl
       """
      
       params = []
       where_clauses = []
      
       if active_only:
           query += """
               JOIN StudySession ss ON sl.locID = ss.locID
           """
           where_clauses.append("ss.date >= CURDATE()")
      
       if building:
           where_clauses.append("sl.building = %s")
           params.append(building)
      
       if where_clauses:
           query += " WHERE " + " AND ".join(where_clauses)
      
       query += " ORDER BY sl.building, sl.room"
      
       cursor.execute(query, params)
       locations = cursor.fetchall()
       cursor.close()
      
       return jsonify(locations), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500


# # GET - Get specific location details
# @session_info.route("/study_location/<int:loc_id>", methods=["GET"])
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

# POST - Add a new study location [TA-4]
@session_info.route("/study_location", methods=["POST"])
def create_study_location():
    """Create a new study location"""
    try:
        current_app.logger.info('Creating new study location')
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["capacity", "room", "building"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        # status defaults to 1 (active) if not provided
        status = data.get("status", 1)
        
        query = """
            INSERT INTO StudyLocation (status, capacity, room, building)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            status,
            data["capacity"],
            data["room"],
            data["building"]
        ))
        
        db.get_db().commit()
        
        # Get the ID of the newly created location
        new_location_id = cursor.lastrowid
        
        cursor.close()
        
        current_app.logger.info(f'Created study location with ID {new_location_id}')
        return jsonify({
            "message": "Study location created successfully",
            "locID": new_location_id
        }), 201
        
    except Error as e:
        current_app.logger.error(f'Database error: {str(e)}')
        return jsonify({"error": str(e)}), 500

# GET - Return all active study sessions [Student-4] [Tutor-1]
@session_info.route("/study_session", methods=["GET"])
def get_study_sessions():
   """Get all active study sessions, optionally filtered by course or topic"""
   try:
       current_app.logger.info('Getting study sessions')
      
       course_crn = request.args.get("course")
       topic_name = request.args.get("topic")
      
       cursor = db.get_db().cursor()
      
       query = """
           SELECT DISTINCT ss.sessionID, ss.date, ss.startTime, ss.endTime,
                  sl.building, sl.room, sl.capacity
           FROM StudySession ss
           JOIN StudyLocation sl ON ss.locID = sl.locID
       """
      
       params = []
       where_clauses = ["ss.date >= CURDATE()"]
      
       current_app.logger.info(f'Retrieved {len(sessions)} study sessions')
       return jsonify(sessions), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500
   
# POST - Start a study session [Student-1]
@session_info.route("/study_session", methods=["POST"])
def create_study_session():
   """Create a new study session"""
   try:
       data = request.get_json()
      
       # Validate required fields
       required_fields = ["sessionID", "locID", "startTime", "endTime", "date", "studentID"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
      
       cursor = db.get_db().cursor()
      
       query = """
           INSERT INTO StudySession (sessionID, locID, startTime, endTime, date, studentID)
           VALUES (%s, %s, %s, %s, %s, %s)
       """
       cursor.execute(query, (
           data["sessionID"],
           data["locID"],
           data["startTime"],
           data["endTime"],
           data["date"],
           data["studentID"]
       ))
      
       db.get_db().commit()
       cursor.close()
       return jsonify({
           "message": "Study session created successfully",
           "sessionID": data["sessionID"]
       }), 201
   except Error as e:
       return jsonify({"error": str(e)}), 500

# GET - Return details for a specific study session [Professor 6]
@session_info.route("/study_session/<int:session_id>", methods=["GET"])
def get_study_session_details(session_id):
    """ Get detailed information about a specific study session including topics covered and time spent on each topic"""
    try:
        current_app.logger.info(f'Getting details for session {session_id}')
        cursor = db.get_db().cursor()
        
        # Get basic session information
        cursor.execute("""
            SELECT ss.sessionID, ss.date, ss.startTime, ss.endTime,
                   sl.building, sl.room, sl.capacity,
                   TIMESTAMPDIFF(MINUTE, ss.startTime, ss.endTime) AS durationMinutes
            FROM StudySession ss
            JOIN StudyLocation sl ON ss.locID = sl.locID
            WHERE ss.sessionID = %s
        """, (session_id,))
        
        session = cursor.fetchone()
        
        if not session:
            cursor.close()
            return jsonify({"error": "Study session not found"}), 404
        
        # Get topics covered in this session
        cursor.execute("""
            SELECT t.topicID, t.name AS topicName, c.courseName
            FROM Session_Covers_Topic sct
            JOIN Topic t ON sct.crn = t.crn AND sct.topicID = t.topicID
            JOIN Course c ON t.crn = c.crn
            WHERE sct.sessionID = %s
        """, (session_id,))
        
        topics = cursor.fetchall()
        session["topics_covered"] = topics
        
        cursor.close()
        
        current_app.logger.info(f'Retrieved session details for session {session_id}')
        return jsonify(session), 200
        
    except Error as e:
        current_app.logger.error(f'Database error: {str(e)}')
        return jsonify({"error": str(e)}), 500

# PUT - Update details for a study session [Student-1]
@session_info.route("/study_session/<int:session_id>", methods=["PUT"])
def update_study_session(session_id):
   """Update an existing study session"""
   try:
       data = request.get_json()
      
       cursor = db.get_db().cursor()
       cursor.execute("SELECT * FROM StudySession WHERE sessionID = %s", (session_id,))
       if not cursor.fetchone():
           return jsonify({"error": "Study session not found"}), 404
      
       update_fields = []
       params = []
       allowed_fields = ["locID", "startTime", "endTime", "date"]
      
       for field in allowed_fields:
           if field in data:
               update_fields.append(f"{field} = %s")
               params.append(data[field])
      
       if not update_fields:
           return jsonify({"error": "No valid fields to update"}), 400
      
       params.append(session_id)
       query = f"UPDATE StudySession SET {', '.join(update_fields)} WHERE sessionID = %s"
      
       cursor.execute(query, params)
       db.get_db().commit()
       cursor.close()
      
       return jsonify({"message": "Study session updated successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# DELETE - Cancel a study session [Student-1]
@session_info.route("/study_session/<int:session_id>", methods=["DELETE"])
def delete_study_session(session_id):
   """Cancel/delete a study session"""
   try:
       cursor = db.get_db().cursor()
      
       # Check if session exists
       cursor.execute("SELECT * FROM StudySession WHERE sessionID = %s", (session_id,))
       if not cursor.fetchone():
           return jsonify({"error": "Study session not found"}), 404
      
       cursor.execute("DELETE FROM StudySession WHERE sessionID = %s", (session_id,))
       db.get_db().commit()
       cursor.close()
      
       return jsonify({"message": "Study session cancelled successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# for professor pages
# GET - Get study time analytics by topic for a professor [Professor-1.6]
@session_info.route("/professor/<int:prof_id>/study_time/topics", methods=["GET"])
def get_professor_study_time_by_topic(prof_id):
    """Get study time analytics grouped by topic for courses taught by professor"""
    try:
        current_app.logger.info(f'Getting study time by topic for professor {prof_id}')
        cursor = db.get_db().cursor()
        
        query = """
            SELECT t.name AS topicName, 
                   SUM(TIMESTAMPDIFF(MINUTE, ss.startTime, ss.endTime)) AS totalMinutesStudied,
                   ROUND(AVG(TIMESTAMPDIFF(MINUTE, ss.startTime, ss.endTime)), 2) AS avgMinutesPerSession,
                   COUNT(DISTINCT ss.sessionID) AS sessionCount
            FROM Professor p
            JOIN Professor_Course pc ON p.profId = pc.profID
            JOIN Course c ON pc.CRN = c.CRN
            JOIN Topic t ON c.CRN = t.CRN
            JOIN Session_Covers_Topic sct ON t.CRN = sct.CRN AND t.topicID = sct.topicID
            JOIN StudySession ss ON sct.sessionID = ss.sessionID
            WHERE p.profId = %s
            GROUP BY t.topicID, t.name
            ORDER BY totalMinutesStudied DESC
        """
        
        cursor.execute(query, (prof_id,))
        results = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Retrieved study time data for {len(results)} topics')
        return jsonify(results), 200
        
    except Error as e:
        current_app.logger.error(f'Database error: {str(e)}')
        return jsonify({"error": str(e)}), 500

# GET - Get sessions for a specific topic
@session_info.route("/topic/<string:topic_name>/sessions", methods=["GET"])
def get_sessions_by_topic(topic_name):
    """Get all study sessions that covered a specific topic"""
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT ss.sessionID, ss.date, ss.startTime, ss.endTime,
                   sl.building, sl.room,
                   TIMESTAMPDIFF(MINUTE, ss.startTime, ss.endTime) AS durationMinutes
            FROM StudySession ss
            JOIN Session_Covers_Topic sct ON ss.sessionID = sct.sessionID
            JOIN Topic t ON sct.CRN = t.CRN AND sct.topicID = t.topicID
            JOIN StudyLocation sl ON ss.locID = sl.locID
            WHERE t.name = %s
            ORDER BY ss.date DESC, ss.startTime DESC
        """
        
        cursor.execute(query, (topic_name,))
        sessions = cursor.fetchall()
        cursor.close()
        
        return jsonify(sessions), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500