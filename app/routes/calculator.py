from flask import Blueprint, request, jsonify
from app.services.calculator import calculate_average

calculator_bp = Blueprint("calculator", __name__, url_prefix="/calculator")

@calculator_bp.route("/average", methods=["POST"])
def average():
    """
    Calcula a média aritmética de uma lista de números.
    ---
    tags:
      - Calculator
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            values:
              type: array
              items:
                type: number
              example: [1, 2, 3, 4]
    responses:
      200:
        description: Média calculada com sucesso
        schema:
          type: object
          properties:
            average:
              type: number
              example: 2.5
      400:
        description: Payload inválido
    """
    try:
        data = request.get_json()
        values = data["values"]
        result = calculate_average(values)
        return jsonify({"average": result}), 200
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid payload"}), 400
