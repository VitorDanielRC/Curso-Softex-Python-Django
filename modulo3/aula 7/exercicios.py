class analisador_de_frase:
    def __init__(self):
        self.frase = ""
    
    def analisar(self):
        self.frase = input("Digite a sua frase:\nR: ")
        

        palavra_2 = self.frase.lower().strip().replace(' ', '')
        

        numero_pa = len(self.frase.split())
        print("Quantidade de palavras:", numero_pa)
        
        cont_vogal = 0
        cont_con = 0
        vogais = "aeiou"
        

        for letra in self.frase.lower():
            if letra in vogais:
                cont_vogal += 1

        for letra in self.frase.lower():
            if letra.isalpha() and letra not in vogais:
                cont_con += 1
        
        print("Quantidade de vogais:", cont_vogal)
        print("Quantidade de consoantes:", cont_con)
        
 
        if palavra_2 == palavra_2[::-1]:
            print("É um palíndromo")
        else:
            print("Não é um palíndromo")


a = analisador_de_frase()
a.analisar()
