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

# GET /ta_admin/{nuID} [Student-3] - Get TA admin info
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
