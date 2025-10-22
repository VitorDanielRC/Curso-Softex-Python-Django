# user_service.py
from user_model import UserModel
from hasher import hash_senha, verificar_senha


class UserService:

    def __init__(self):
        """
        crie um atributo que receberá a UserModel como composição
        """
        self.usermodel = UserModel
    def _safe_user_data(self, user) -> dict | None:
        """
        este é um método privado que recebe um usuarios do banco.
        verifique se o usuários existe e então retorne ele sem a sua senha
        caso ele não exista retorne None
        """

        if user is None:
            return None
        user_dict = dict(user)
        user_dict.pop("senha_hash", None)
        return user_dict
    

    def _is_authorized(
        self,
        current_user_id: int | None,
        current_user_profile: str,
        target_user_id: int,
        action: str,
    ) -> bool:
        """
        Método que verifica o perfil do usuários, se for Diretoria retorne true
        Se não tiver target_user_id retorn false
        Se  action == "edit_self" retorne current_user_id == target_user_id
        No geral retorn false
        """

        if current_user_profile == "Diretoria":
            return True
        if target_user_id == None:
            return False
        if action == "edit_self":
            return current_user_id == target_user_id
        return False
    def register_user(
        self,
        senha: str,
        email: str,
        nome_completo: str,
        perfil: str = "Afiliado",
    ) -> tuple[bool, str]:
        """
        Método para criar um usuários.
        o campo senha deve ter no mínimo 8 caracteres, caso contrário retorne False a mensagem de erro.
        O campo email deve ter pelo menos 10 caracteres, uma @ e terminar com .com, retorne False se não tiver e a mensagem de erro.
        O campo Nome deve ter apenas letras e não deve estar vazio, retorne False se não tiver e a mensagem de erro.
        Caso os campos atendas as requisições, faça o hash da senha e salve use o método create_user da User Model
        """
        if len(senha) < 8:
            print("Senha incorreta")
        else:
            return False
        
        if len(email) < 10 and email not in "@" and email.endswith(".com") == False:
            return False
        if not any(char.isdigit() for char in nome_completo):
            print("Nao pode estar vazio")
            return False
        senha_cripto = hash_senha(senha)
        UserModel.create_user = senha_cripto

    def login_user(self, email: str, senha: str) -> tuple[dict | None, str]:
        """
        Este método é o login do usuários, deve receber um email e senha não vazios
        Use o método do find_user_by_email para buscar o usuario
        Se houver usuarios faça a comparação da senha passada com a senha hash do DB
        Use a função verificar_senha, se tiver ok, retorn o usuarios pelo método privado _safe_user_data
        e a mensagem Login bem-sucedido!.
        Caso contrario retorne None e a mensagem de erro
        """

        if email == "" and senha == "":
            verificar_email = UserModel.find_user_by_email(email)

            
    def update_user_profile(
        self,
        current_user_id: int | None,
        current_user_profile: str,
        target_user_id: int,
        new_data: dict,
    ) -> tuple[bool, str]:
        """
        Método para atualizar usuários.
        Chame o método privado _is_authorized, se o retorno for false, retorne false e acesso negado
        Confira as chaves em new_data (senha, nome_completo, email), se pelo menos um desses campos,
        Caso não haja nenhum valor a ser atualizado, encerre a função com False e mensagem de erro.
        Caso contrátio, chame o método da UserModel update_user_by_id passando o id e o new data
        """

    def delete_user(
        self,
        current_user_profile: str,
        user_id: int,
    ) -> tuple[bool, str]:
        """
        Método para deletar usuarios.
        So é permitido deletar usuarios se o current_user_profile for Diretoria.
        Caso não seja retorn false e a mensagem de acesso negado
        Senão chame o método delete_user_by_id, passando o id do usuários
        """

    def get_user_by_id(self, user_id: int) -> dict | None:
        """
        Método para pegar um usuarios pelo id
        Retorne o usuarios apos passar pelo método _safe_user_data
        """

    def get_all_users(self) -> list[dict | None]:
        """
        Método para retornar todos os usuários.
        retorne todos os usuáriso apos passar pelo método _safe_user_data
        """