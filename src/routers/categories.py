from flask import Blueprint, request, jsonify
from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.dtos.category import CategoryResponseDTO, CategoryCreateUpdateDTO
from src.models import Category
from src.core.db import db

categories_bp = Blueprint("categories", __name__, url_prefix='/categories')


# R
# 1) Получить нужный набор данных (Sqlalchemy)
# 2) Преобразовать набор данных в простенькие объекты (Pydantic)
# 3) Вернуть ответ (jsonify Response)
@categories_bp.route('/', methods=["GET"])
def list_of_categories():
    data = Category.query.all()

    response = [
        CategoryResponseDTO.model_validate(cat).model_dump()
        for cat in data
    ]

    return jsonify(
        response
    ), 200


# C
# 1) Получить сырые данные из запроса
# 2) Проверить сырые данные на валидность (Pydantic)
# 3) Попытаться создать новый объект модели (SQLAlchemy)
# 4) Добавить созданный объект в сессию (db.session.add(<obj>))
# 5) Сохранить изменения в базу данных (db.session.commit())
# 6) Вернуть ответ (jsonify Response)


# U
# 1) Получить сырые данные из запроса
# 2) Проверить сырые данные на валидность (Pydantic)
# 3) Попытаться получить нужный объект для обновления (SQLAlchemy)
# 4) Попытаться обновить полученный объект новыми валидными данными (Model.field = New_attr)
# 5) Сохранить изменения в базу данных (db.session.commit())
# 6) Вернуть ответ (jsonify Response)
