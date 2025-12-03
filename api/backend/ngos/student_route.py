from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

students = Blueprint("students", __name__)

# GET - view study sessions
@students.route("/study_sessions", methods=["GET"])
def get_sessions():
    try:
        current_app.logger.info('Getting all study sessions')
        cursor = db.get_db().cursor()
        query = "SELECT ss.sessionID, ss.date, ss.startTime, ss.endTime, sl.building, sl.room, sl.capacity, sl.status
                FROM StudySessions ss
                JOIN Study Location sl ON ss.locID = sl.locID
                WHERE ss.date >= CURDATE()
                ORDER BY ss.date, ss.startTime"
        cursor.execute(query)
        sessions = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Retrieved {len(sessions)} study sessions')
        return jsonify(sessions), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_sessions: {str(e)}')
        return jsonify({"error": str(e)}), 500

# GET - view student information
@students.route("/student", methods=["GET"])
def get_student():
    try:
        current_app.logger.info('Getting student information')
        cursor = db.get_db().cursor()
        query = "SELECT pgs.firstName, pgs.lastName, s.email
                FROM ProjectGroup_Student pgs
                JOIN Student s ON pgs.nuID = s.nuID
                WHERE pgs.teamID = 1 AND pgs.CRN = 12345;"
        cursor.execute(query)
        student = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Retrieved student information')
        return jsonify(student), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_students: {str(e)}')
        return jsonify({"error": str(e)}), 500