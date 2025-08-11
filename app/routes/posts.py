from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from ..models import db, Post, Like

bp = Blueprint('posts_actions', __name__)

@bp.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_toggle(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    created = False
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        created = True
    count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({"liked": created, "count": count})
