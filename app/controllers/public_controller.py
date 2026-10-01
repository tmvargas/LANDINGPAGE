from flask import Blueprint, jsonify, render_template
from sqlalchemy import text

from app.db import db


public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def home():
    return render_template("public/home.html")


@public_bp.get("/health")
def health():
    return jsonify(status="ok"), 200


@public_bp.get("/ready")
def ready():
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        return jsonify(status="not_ready"), 503
    return jsonify(status="ready"), 200
