from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for study location routes
#study_locations = Blueprint("study_locations", __name__)


# Get all study locations with optional filtering by status/building
# (example checking status of rooms in Snell)

@study_locations.route("/study_locations", methods=["GET"])
def get_all_study_locations():
    """
    Get all study locations 
    Can filter by status (active/inactive) and building
    """

    try: 
        current_app.logger.info('Starting get_all_study_locations request')
        cursor = db.get_db().cursor()

        # params
        status = request.args.get("status")
        building = request.args.get("building")
        #query
        query = "SELECT * FROM StudyLocation WHERE 1=1"
        params = []

            # adding filters if there 
        if status is not None:
            query += " AND status = %s"
            params.append(status)
        if building:
            query += " AND building = %s"
            params.append(building)

        cursor.execute(query, params)
        locations = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'retrieved {len(locations)} locations')
        return jsonify(locations), 200
    except Error as e: 
        current_app.logger.error(f'error in getting locations alayna : {str(e)}')
        return jsonify({"error" : str(e)}), 500