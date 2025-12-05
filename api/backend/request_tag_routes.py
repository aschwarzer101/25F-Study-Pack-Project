from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


requests_tags = Blueprint("requests_tags", __name__)

# POST - Create a request for a session [Student-1]
@requests_tags.route("/session_request", methods=["POST"])
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

# GET all the pending session requests [TA-6]
# Can filter by status 
@requests_tags.route("/session_requests", methods=["GET"])
def get_session_requests():
    """Get all session requests. Filter by status (Pending, Approved, Completed)"""
    try: 
        current_app.logger.info("Starting get session requests request")
        cursor = db.get_db().cursor()

        #status parameter to filter by 
        status = request.args.get("status")
        # display, include ones even without tags (LEFT JOIN)
        current_app.logger.debug(f'Parameter for status: {status}')
        query= """
        SELECT 
            sr.requestID,
            sr.dateCreated, 
            sr.status,
            sr.adminID,
            CONCAT(s.firstName, ' ', s.lastName) AS requestingStudents,
        FROM SessionRequest sr
        JOIN Requesting_Students rs ON sr.requestID = rs.requestID
        JOIN Student s ON rs.nuID = s.nuID
        LEFT JOIN Request_Tags rt ON sr.requestID = rt.requestID
        LEFT JOIN Tag t ON rt.tagID = t.tagID
        WHERE 1=1
        """
        params = []

        # add status filter if provided 
        if status: 
            query += "AND sr.status = %s"
            params.append(status)
        
        # append group by 
        query += "GROUP BY sr.requestID ORDER BY sr.dateCreated DESC"

        current_app.logger.debug(f'Executing query: {query}')
        cursor.execute(query, params)
        session_requests = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Success, retreived {len(session_requests)} session requests')
        return jsonify(session_requests), 200
    except Error as e:
        current_app.logger.error(f'db error in get_session_requests: {str(e)}')
        return jsonify({"error": str(e)}), 500

# GET the students who submitted a request [TA-6] [Tutor-6]



# PUT: Approve/assign specific a session request [TA-6]


# DELETE: Reject a session request [TA-6]