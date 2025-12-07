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
            GROUP_CONCAT(s.firstName) AS studentFirstNames,
            GROUP_CONCAT(t.tagName) AS tags
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
            query += " AND sr.status = %s"
            params.append(status)
        
        # append group by 
        query += " GROUP BY sr.requestID ORDER BY sr.dateCreated DESC"

        current_app.logger.debug(f'Executing query: {query}')
        cursor.execute(query, params)
        session_requests = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Success, retreived {len(session_requests)} session requests')
        return jsonify(session_requests), 200
    except Error as e:
        current_app.logger.error(f'db error in get_session_requests: {str(e)}')
        return jsonify({"error": str(e)}), 500


# GET /session_requests/{requestID} - Get students who submitted a request [TA-6] [Tutor-6]
@requests_tags.route("/session_requests/<int:request_id>", methods=["GET"])
def get_session_request_details(request_id):
    """
    Get detailed information about a specific session request. Returns all students who 
    submitted this request and the associated tags
    """
    try:
        cursor = db.get_db().cursor()

        #GET request with students and tags
        query = """
        SELECT 
            sr.requestID,
            sr.dateCreated,
            sr.status,
            GROUP_CONCAT(s.nuID) AS studentIDs,
            GROUP_CONCAT(s.email) AS studentEmails, 
            GROUP_CONCAT(s.firstName) AS studentFirstNames,
            GROUP_CONCAT(s.lastName) AS studentLastNames,
            GROUP_CONCAT(t.tagName) AS tags
        FROM SessionRequest sr
        JOIN Requesting_Students rs ON sr.requestID = rs.requestID
        JOIN Student s ON rs.nuID = s.nuID
        LEFT JOIN Request_Tags rt ON sr.requestID = rt.requestID
        LEFT JOIN Tag t on rt.tagID = t.tagID
        WHERE sr.requestID = %s
        GROUP BY sr.requestID
        """

        cursor.execute(query, (request_id,))
        results = cursor.fetchall()

        if not results:
            return jsonify({"error": "Session request not found"}), 404
        cursor.close()
        return jsonify(results), 200
    except Error as e: 
        return jsonify({"error" : str(e)}), 500

# PUT: /session_requests/{requestID} - Approve/assign specific a session request [TA-6]
@requests_tags.route("/session_requests/<int:request_id>", methods=["PUT"])
def approve_session_request(request_id):
    """ 
    Approve or assign a session reuqest [TA-6]
    Updates the status to Approved or Completed
    """
    try:
        data = request.get_json()
        #if proper status isn't there
        if "status" not in data:
            return jsonify({"error": "Missing required field: status"}), 400
        
        cursor = db.get_db().cursor()

        #check request
        cursor.execute("SELECT * FROM SessionRequest WHERE requestID = %s", (request_id,))
        if not cursor.fetchone():
            return jsonify({"error":"Session request not found"}), 404
        
        query = "UPDATE SessionRequest SET status = %s WHERE requestID = %s"
        cursor.execute(query, (data["status"], request_id))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Session request approved successfully"}), 200

    except Error as e:
        return jsonify({"error" : str(e)}), 500
            

# DELETE: /session_requests/{requestID} - Reject session request [TA-6] - Reject a session request [TA-6]
@requests_tags.route("/session_requests/<int:request_id>", methods=["DELETE"])
def reject_sessions_request(request_id):
    """
    Reject a session request [TA-6]
    Deletes the request and all associated data
    """
    try:
        cursor = db.get_db().cursor()

        #Check if request exists
        cursor.execute("SELECT * FROM SessionRequest WHERE requestID = %s", (request_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Session request not found"}), 404
        
        #Delete Request_tags entries first due to FK contrants
        cursor.execute("DELETE FROM Request_Tags WHERE requestID = %s", (request_id,))

        #then delete from requesting_students entries ""

        cursor.execute("DELETE FROM Requesting_Students WHERE requestID = %s", (request_id,))
        #delete session requesst itself
        cursor.execute("DELETE FROM SessionRequest WHERE requestID = %s", (request_id,))

        db.get_db().commit()
        cursor.close()

        return jsonify({"Message": "request rejected and deleted successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
