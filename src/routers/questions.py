from flask import Blueprint, request, jsonify
from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from src.dtos.questions import PollCreateRequest, PollResponse, PollUpdateRequest
from src.dtos.questions import PollOptionCreateRequest
from src.models import Poll, PollOption
from src.core.db import db

questions_bp = Blueprint("questions", __name__, url_prefix='/questions')


# CRUD (Questions)

# R
@questions_bp.route('', methods=["GET"])
def list_of_questions():
    try:
        polls = db.session.execute(
            db.select(Poll)
            .options(
                selectinload(Poll.options),
                selectinload(Poll.category)
            )
        ).scalars().all()

        polls_list = [
            PollResponse.model_validate(poll).model_dump()
            for poll in polls
        ]

        return jsonify(polls_list), 200

    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": str(exc)
        }), 500

    except Exception as exc:
        return jsonify({
            "error": "Unexpected error",
            "message": str(exc)
        }), 500


# C
@questions_bp.route('/create', methods=["POST"])
def create_new_question():
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify({
                "error": "Validation error",
                "message": "Request body is required"
            }), 400

        poll_data: PollCreateRequest = PollCreateRequest.model_validate(raw_data)

        options_data: list[PollOptionCreateRequest]  = poll_data.options
        poll_dict: dict[str, Any] = poll_data.model_dump(exclude={'options'})

        poll: Poll = Poll(**poll_dict)

        db.session.add(poll)
        db.session.flush()

        for option_data in options_data:
            option = PollOption(
                poll_id=poll.id,
                text=option_data.text
            )
            poll.options.append(option)

        db.session.commit()

        poll = db.session.execute(
            db.select(Poll)
            .options(
                selectinload(Poll.options),
                selectinload(Poll.category)
            )
            .where(Poll.id == poll.id)
        ).scalar_one()
        
        poll_response = PollResponse.model_validate(poll)

        return jsonify(poll_response.model_dump()), 201

    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "message": exc.errors()
        }), 400

    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": str(exc)
        }), 500

    except Exception as exc:
        db.session.rollback()
        return jsonify({
            "error": "Unexpected error",
            "message": str(exc)
        }), 500


# R
@questions_bp.route('/<int:question_id>', methods=["GET"])
def get_question_by_id(question_id: int):
    try:
        poll = db.session.execute(
            db.select(Poll)
            .options(
                selectinload(Poll.options),
                selectinload(Poll.category)
            )
            .where(Poll.id == question_id)
        ).scalar_one_or_none()

        if poll is None:
            return jsonify({
                "error": "Not found",
                "message": f"Poll with ID {question_id} not found"
            }), 404

        poll_response = PollResponse.model_validate(poll)

        return jsonify(poll_response.model_dump()), 200

    except SQLAlchemyError as exc:
        return jsonify({
            "error": "Database error",
            "message": str(exc)
        }), 500

    except Exception as exc:
        return jsonify({
            "error": "Unexpected error",
            "message": str(exc)
        }), 500


# U
@questions_bp.route('/<int:question_id>/update', methods=["PUT", "PATCH"])
def update_question(question_id: int):
    try:
        raw_data = request.get_json()

        if not raw_data:
            return jsonify({
                "error": "Validation error",
                "message": "Request body is required"
            }), 400

        poll = db.session.execute(
            db.select(Poll).where(Poll.id == question_id)
        ).scalar_one_or_none()

        if poll is None:
            return jsonify({
                "error": "Not found",
                "message": f"Poll with ID {question_id} not found"
            }), 404

        update_data = PollUpdateRequest.model_validate(raw_data)

        update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in update_dict.items():
            setattr(poll, field, value)

        db.session.commit()

        db.session.refresh(poll)
        poll = db.session.execute(
            db.select(Poll)
            .options(
                selectinload(Poll.options),
                selectinload(Poll.category)
            )
            .where(Poll.id == question_id)
        ).scalar_one()

        poll_response = PollResponse.model_validate(poll)

        return jsonify(poll_response.model_dump()), 200

    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "message": exc.errors()
        }), 400

    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": str(exc)
        }), 500

    except Exception as exc:
        db.session.rollback()
        return jsonify({
            "error": "Unexpected error",
            "message": str(exc)
        }), 500


# D
@questions_bp.route('/<int:question_id>/delete', methods=["DELETE"])
def delete_question(question_id: int):
    try:
        poll = db.session.execute(
            db.select(Poll).where(Poll.id == question_id)
        ).scalar_one_or_none()

        if poll is None:
            return jsonify({
                "error": "Not found",
                "message": f"Poll with ID {question_id} not found"
            }), 404

        db.session.delete(poll)
        db.session.commit()

        return jsonify({
            "message": f"Poll with ID {question_id} was deleted successfully"
        }), 200

    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": str(exc)
        }), 500

    except Exception as exc:
        db.session.rollback()
        return jsonify({
            "error": "Unexpected error",
            "message": str(exc)
        }), 500
