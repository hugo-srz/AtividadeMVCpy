from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = UsuarioService.listar_todos()
    return jsonify([u.to_dict() for u in usuarios]), 200

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json() or {}
    try:
        novo_usuario = UsuarioService.criar_usuario(data)
        return jsonify(novo_usuario.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.get_json() or {}
    try:
        usuario = UsuarioService.atualizar_usuario(id, data)
        return jsonify(usuario.to_dict()), 200
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        UsuarioService.deletar_usuario(id)
        return jsonify({"mensagem": "Usuário removido com sucesso."}), 200
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route('/usuarios/<int:id>/chamados', methods=['GET'])
def listar_chamados_usuario(id):
    try:
        chamados = UsuarioService.listar_chamados_do_usuario(id)
        return jsonify([c.to_dict() for c in chamados]), 200
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404