from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

from app.services.catalog_service import CatalogService


presentation_bp = Blueprint("presentation", __name__, url_prefix="/apresentacao")


@presentation_bp.get("/consultoria")
@login_required
def consulting():
    if not CatalogService().user_can_access(current_user.id, "consultoria-ps"):
        abort(403)
    return render_template("presentation/consulting.html")
