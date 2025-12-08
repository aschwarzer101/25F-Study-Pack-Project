from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


person_assignment = Blueprint("person_assignment", __name__)

# GET - Return a teaching assistant's information [Student-3] [TA-2]
@person_assignment.route("/teaching_assistant/<int:ta_nuid>", methods=["GET"])
def get_ta_info(ta_nuid):
   """Get information about a specific teaching assistant"""
   try:
       cursor = db.get_db().cursor()
      
       query = """
           SELECT nuID, firstName, lastName, email, crn
           FROM TeachingAssistant
           WHERE nuID = %s
       """
      
       cursor.execute(query, (ta_nuid,))
       ta = cursor.fetchone()
      
       if not ta:
           return jsonify({"error": "Teaching assistant not found"}), 404
      
       cursor.close()
       return jsonify(ta), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# GET /ta_admins/{nuID} [Student-3] - Get TA admin info
@person_assignment.route("/ta_admins/<int:nu_id>", methods=["GET"])
def get_ta_admin_info(nu_id): 
    """
    Get info about a TA admin 
    Used by students to contact their TA admin
    """
    try: 
        cursor = db.get_db().cursor()

        query = """
        SELECT nuID, firstName, lastName, email, crn
        FROM TA_Admin
        WHERE nuID = %s
        """

        cursor.execute(query, (nu_id,))
        ta_admin = cursor.fetchone()

        if not ta_admin:
            return jsonify({"error": "TA admin not found"}), 404
        
        cursor.close()
        return jsonify(ta_admin), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500


# PUT /ta_admins/{nuID} - TA admin updates own profile
@person_assignment.route("/ta_admins/<int:nu_id>", methods=["PUT"])
def update_ta_admin(nu_id):
    """
    TA admin updates their own profile information
    Can update firstName, lastName, email
    """
    try:
        data = request.get_json()

        cursor = db.get_db().cursor()

        #check ta admin exists
        cursor.execute("SELECT * FROM TA_Admin WHERE nuID = %s", (nu_id,))
        if not cursor.fetchone():
            return jsonify({"error": "TA admin not found"}), 404

        #paramatize fields
        update_fields = []
        params = []
        allowed_fields = ["firstName", "lastName", "email"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(nu_id)
        query = f"UPDATE TA_Admin SET {', '.join(update_fields)} WHERE nuID = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "TA admin profile updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# POST /teaching_assistants - add TA to the team [TA-2]
@person_assignment.route("/teaching_assistants", methods=["POST"])
def add_teaching_assistant():
    """
    Add a new teaching assistant to the team , would be: 
    Body: {
        "nuID": 001567890,
        "firstName": "Mark Jr.",
        "lastName": "Fontenot",
        "email":"fontenot.mj@northeastern.edu",
        "crn": 12345,
        "adminID": 001234567
    }
    """
    try: 
        data = request.get_json()

        #Validate fields 
        required_fields = ["nuID", "firstName", "lastName", "email", "crn", "adminID"]
        for field in required_fields: 
            if field not in data: 
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
        cursor = db.get_db().cursor()

        #insert new assistant - LANE COME AND FIX THIS LATER
        query = """
        INSERT INTO TeachingAssistant (nuID, firstName, lastName, email, crn, adminID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query, 
            (
                data["nuID"],
                data["firstName"],
                data["lastName"],
                data["email"],
                data["crn"],
                data["adminID"]
            )
        )

        db.get_db().commit()
        cursor.close()

        return jsonify({
            "message": "Teaching assistant added",
            "nuID": data["nuID"]
        }), 201
    except Error as e: 
        return jsonify({"error": str(e)}), 500