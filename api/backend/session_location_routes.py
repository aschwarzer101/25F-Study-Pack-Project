from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


students = Blueprint("session location", __name__)

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
    
# GET - Return locations of active study sessions [Student-4]
@students.route("/study_location", methods=["GET"])
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


# GET - Get specific location details
@students.route("/study_location/<int:loc_id>", methods=["GET"])
def get_study_location_details(loc_id):
   """Get details of a specific study location"""
   try:
       cursor = db.get_db().cursor()
      
       cursor.execute("""
           SELECT locID, building, room, capacity, status
           FROM StudyLocation
           WHERE locID = %s
       """, (loc_id,))
      
       location = cursor.fetchone()
      
       if not location:
           return jsonify({"error": "Study location not found"}), 404
      
       # Get upcoming sessions at this location
       cursor.execute("""
           SELECT sessionID, date, startTime, endTime
           FROM StudySession
           WHERE locID = %s AND date >= CURDATE()
           ORDER BY date, startTime
       """, (loc_id,))
      
       sessions = cursor.fetchall()
       location["upcoming_sessions"] = sessions
      
       cursor.close()
       return jsonify(location), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500


# GET - Return all active study sessions [Student-4]
@students.route("/study_session", methods=["GET"])
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
@students.route("/study_session", methods=["POST"])
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

# PUT - Update details for a study session [Student-1]
@students.route("/study_session/<int:session_id>", methods=["PUT"])
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
@students.route("/study_session/<int:session_id>", methods=["DELETE"])
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

