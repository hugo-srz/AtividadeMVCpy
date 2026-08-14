from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository
from models.chamado import Chamado

class ChamadoService:
    @staticmethod
    def listar_todos():
        return ChamadoRepository.get_all()

    @staticmethod
    def listar_abertos():
        return ChamadoRepository.get_by_status("Aberto")

    @staticmethod
    def listar_alta_prioridade():
        return ChamadoRepository.get_by_prioridade("Alta")

    @staticmethod
    def criar_chamado(data):
        titulo = data.get("titulo")
        descricao = data.get("descricao")
        prioridade = data.get("prioridade")
        usuario_id = data.get("usuario_id")
        tecnico = data.get("tecnico")

        if not titulo or len(titulo) < 5:
            raise ValueError("O título é obrigatório e deve conter pelo menos 5 caracteres.")

        if not descricao or len(descricao) < 10:
            raise ValueError("A descrição é obrigatória e deve conter pelo menos 10 caracteres.")

        if prioridade not in ["Baixa", "Média", "Alta"]:
            raise ValueError("A prioridade deve ser 'Baixa', 'Média' ou 'Alta'.")

        if not usuario_id or not UsuarioRepository.get_by_id(usuario_id):
            raise ValueError("O chamado deve estar vinculado a um usuário existente.")

        if prioridade == "Alta":
            ativos_alta = ChamadoRepository.count_ativos_alta_prioridade_por_usuario(usuario_id)
            if ativos_alta >= 5:
                raise ValueError("O usuário não pode possuir mais de 5 chamados de alta prioridade não encerrados.")

        novo_chamado = Chamado(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            status="Aberto",
            usuario_id=usuario_id,
            tecnico=tecnico
        )
        return ChamadoRepository.create(novo_chamado)

    @staticmethod
    def atualizar_chamado(chamado_id, data):
        chamado = ChamadoRepository.get_by_id(chamado_id)
        if not chamado:
            raise KeyError("Chamado não encontrado.")

        if "titulo" in data:
            if len(data["titulo"]) < 5:
                raise ValueError("O título deve possuir pelo menos 5 caracteres.")
            chamado.titulo = data["titulo"]

        if "descricao" in data:
            if len(data["descricao"]) < 10:
                raise ValueError("A descrição deve possuir pelo menos 10 caracteres.")
            chamado.descricao = data["descricao"]

        if "prioridade" in data:
            if data["prioridade"] not in ["Baixa", "Média", "Alta"]:
                raise ValueError("Prioridade inválida.")
            chamado.prioridade = data["prioridade"]

        if "tecnico" in data:
            chamado.tecnico = data["tecnico"]

        ChamadoRepository.update()
        return chamado

    @staticmethod
    def deletar_chamado(chamado_id):
        chamado = ChamadoRepository.get_by_id(chamado_id)
        if not chamado:
            raise KeyError("Chamado não encontrado.")
        ChamadoRepository.delete(chamado)

    @staticmethod
    def iniciar_atendimento(chamado_id):
        chamado = ChamadoRepository.get_by_id(chamado_id)
        if not chamado:
            raise KeyError("Chamado não encontrado.")

        if chamado.status != "Aberto":
            raise ValueError(f"Transição não permitida: Não é possível mudar de '{chamado.status}' para 'Em atendimento'.")

        chamado.status = "Em atendimento"
        ChamadoRepository.update()
        return chamado

    @staticmethod
    def encerrar_chamado(chamado_id):
        chamado = ChamadoRepository.get_by_id(chamado_id)
        if not chamado:
            raise KeyError("Chamado não encontrado.")

        if chamado.status != "Em atendimento":
            raise ValueError(f"Transição não permitida: Não é possível mudar de '{chamado.status}' para 'Encerrado'.")

        chamado.status = "Encerrado"
        ChamadoRepository.update()
        return chamado

    @staticmethod
    def obter_estatisticas():
        return {
            "usuarios": UsuarioRepository.count_all(),
            "chamados": ChamadoRepository.count_all(),
            "abertos": ChamadoRepository.count_by_status("Aberto"),
            "em_atendimento": ChamadoRepository.count_by_status("Em atendimento"),
            "encerrados": ChamadoRepository.count_by_status("Encerrado")
        }
