class Cliente:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self._email = None
        self.email = email  # usa o setter

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, novo_email):
        if "@" not in novo_email:
            print("Você precisa colocar um '@' no email.")
            return
        self._email = novo_email


class CanalEnvio:
    def enviar(self, mensagem: str):
        raise NotImplementedError("O método enviar() deve ser implementado nas subclasses.")


class Email(CanalEnvio):
    def enviar(self, mensagem: str):
        print(f"📧 Enviando para servidor de email: {mensagem}")


class Sms(CanalEnvio):
    def enviar(self, mensagem: str):
        print(f"📱 Enviando para operadora telefônica: {mensagem}")


class SistemaAlerta:
    def __init__(self, usuario: Cliente, canal: CanalEnvio):
        self.usuario = usuario
        self.canal = canal

    def disparar(self, texto: str):
        mensagem = f"Para {self.usuario.nome}: {texto}"
        self.canal.enviar(mensagem)


if __name__ == "__main__":
    usuario = Cliente("Ana", "ana@example.com")
    print("Email atual:", usuario.email)

    print("\nTentando definir email inválido...")
    usuario.email = "email_invalido"
    print("Email depois do inválido:", usuario.email)

    print("\nTentando definir email válido...")
    usuario.email = "ana.nova@example.com"
    print("Email depois do válido:", usuario.email)

    print("\n--- Teste com canal Email ---")
    canal_email = Email()
    sistema_email = SistemaAlerta(usuario, canal_email)
    sistema_email.disparar("Seu pagamento foi aprovado!")

    print("\n--- Teste com canal SMS ---")
    canal_sms = Sms()
    sistema_sms = SistemaAlerta(usuario, canal_sms)
    sistema_sms.disparar("Servidor caiu! Verificar imediatamente.")
