from flask import Blueprint, render_template
bp = Blueprint('offline', __name__)

@bp.route('/offline')
def offline():
    return render_template('offline.html'), 200
