from repositories.usuario_repository import UsuarioRepository
from repositories.chamado_repository import ChamadoRepository
from models.usuario import Usuario

class UsuarioService:
    @staticmethod
    def listar_todos():
        return UsuarioRepository.get_all()

    @staticmethod
    def buscar_por_id(usuario_id):
        return UsuarioRepository.get_by_id(usuario_id)

    @staticmethod
    def criar_usuario(data):
        nome = data.get("nome")
        email = data.get("email")
        setor = data.get("setor")

        if not nome:
            raise ValueError("O campo 'nome' é obrigatório.")
        if not email:
            raise ValueError("O campo 'email' é obrigatório.")

        if UsuarioRepository.get_by_email(email):
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        novo_usuario = Usuario(nome=nome, email=email, setor=setor)
        return UsuarioRepository.create(novo_usuario)

    @staticmethod
    def atualizar_usuario(usuario_id, data):
        usuario = UsuarioRepository.get_by_id(usuario_id)
        if not usuario:
            raise KeyError("Usuário não encontrado.")

        email = data.get("email")
        if email and email != usuario.email:
            if UsuarioRepository.get_by_email(email):
                raise ValueError("Já existe outro usuário cadastrado com este e-mail.")
            usuario.email = email

        if "nome" in data:
            if not data["nome"]:
                raise ValueError("O campo 'nome' não pode ser vazio.")
            usuario.nome = data["nome"]

        if "setor" in data:
            usuario.setor = data["setor"]

        UsuarioRepository.update()
        return usuario

    @staticmethod
    def deletar_usuario(usuario_id):
        usuario = UsuarioRepository.get_by_id(usuario_id)
        if not usuario:
            raise KeyError("Usuário não encontrado.")

        chamados = ChamadoRepository.get_by_usuario_id(usuario_id)
        if len(chamados) > 0:
            raise ValueError("Não é possível excluir um usuário que possui chamados cadastrados.")

        UsuarioRepository.delete(usuario)

    @staticmethod
    def listar_chamados_do_usuario(usuario_id):
        usuario = UsuarioRepository.get_by_id(usuario_id)
        if not usuario:
            raise KeyError("Usuário não encontrado.")
        return ChamadoRepository.get_by_usuario_id(usuario_id)