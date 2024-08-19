import requests, json, os, datetime, secrets
from dotenv import load_dotenv
from random import randrange
from datetime import *

import firebase_admin
from firebase_admin import credentials, db, firestore
sim = [
    # Português
    "Sim", "s", "sim", "sin", "Simm", "Simmm", "Siim", "Siimmm", "Claro", "Certeza", "Com certeza",
    "Pois é", "Pode crer", "Fechado", "Certo", "Beleza", "Tá bom", "Tô dentro",
    "Tá sim", "Tá certo", "Vai nessa", "Mandou bem", "De boa", "Certamente", 
    "Óbvio", "Combinado", "Vai fundo", "Bora", "Vamo que vamo", "Tamo junto",
    "Demorou", "Partiu", "Já é", "É nóis", "Fechou", "Pode apostar", "Tranquilo",
    "Tô nessa", "É isso aí", "Tô junto", "Sin", "Si", "Zim", "Já tá na mão",
    "Vambora", "Simplesmente sim", "Sim, krl", "Sinão", "Já tô na área", 
    "Certeza, mano", "Vai na fé", "Tô contigo", "Beleza pura", "Pode deixar",
    
    # Inglês
    "Yes", "Yep", "Yup", "Yeah", "Yessir", "Yass", "Yaaas", "Yesss", "Hell yeah",
    "Hell yes", "Yuppers", "Yuh", "Yah", "Yepper", "Absolutely", "Totally", 
    "For sure", "Fo sho", "You bet", "Bet", "Sure thing", "Of course", "Definitely",
    "Okie dokie", "Ok", "Roger that", "Aye", "Aight", "Yisss", "Uh-huh", "Yep yep",
    "Sure", "Damn right", "Yupp", "Yaaaaas", "Yeet", "Okey dokey", "Affirmative",
    "You got it", "Right on", "10-4", "No doubt", "You betcha", "Alright", "All good",
    "In a heartbeat", "Sign me up", "I’m in", "Count me in", "Totally down", "Gotcha",
    
    # Espanhol
    "Sí", "Sip", "Sipos", "Sep", "Claro", "Claro que sí", "Simón", "Obvio", 
    "Por supuesto", "Seguro", "Ándale", "A huevo", "A webo", "Dale", "Sí, pues", 
    "Es correcto", "Ya está", "Eso es", "Sí, señor", "Desde luego", "De una", 
    "Obvio que sí", "Claramente", "Seguro que sí", "No hay duda", "Por descontado", 
    "Desde luego que sí", "Venga", "Sí, güey", "Órale", "Claro, güey", "Va que va",
    "Sí, compa", "Vamos allá", "Ya pues", "Hecho", "Dale pues", "Órale pues", 
    "Sí, carnal", "Sin problema", "Por supuesto que sí", "Sí claro", "Confirmado", 
    "Sí, mi rey", "Ya está, loco", "Afirmativo", "Claro que sí, loco", "Sí, parcero",
    
    # Francês
    "Oui", "Ouais", "Oué", "Ouip", "Of course", "Carrément", "Bien sûr", "Tout à fait", 
    "Certainement", "Evidemment", "C’est sûr", "Clairement", "D’accord", "Exactement", 
    "Bien entendu", "Pourquoi pas", "Sans doute", "Absolument", "Affirmatif", 
    "Volontiers", "Je veux bien", "C’est ça", "Tout à fait, mon ami", "Comme tu veux", 
    "Avec plaisir", "Aucun problème", "Bien sûr que oui", "Bien entendu, mon ami", 
    "Okidoki", "Sans aucun doute", "Avec certitude", "Ouais, c’est ça", "Oui oui", 
    "Ah oui", "Tout bon", "Mais bien sûr", "Tu parles", "C’est clair", "Oui, chef",
    
    # Italiano
    "Sì", "Sì sì", "Certo", "Sicuro", "Certamente", "Sicuramente", "Ovviamente", 
    "Senza dubbio", "Senza problemi", "Chiaro", "Assolutamente", "D’accordo", 
    "Va bene", "Giusto", "Come no", "Va bene così", "Senza dubbio, amico", "Di sicuro", 
    "Certamente sì", "Ovviamente sì", "Sicuramente sì", "Sì, certo", "Sì, caro", 
    "Esattamente", "È così", "Perfetto", "Senza dubbio, fratello", "Confermo", "Ok", 
    "Ok certo", "Ok perfetto", "Ok, andiamo", "Ok sì", "Sì, dai", "Sì, certo, dai", 
    "Sì, facciamolo", "Sì, ovviamente, dai", "Ovviamente sì, caro", "Sì, caro amico", 
    "Sì sì sì", "Ok, tutto bene", "Ok, sicuro", "Sicuro al 100%", "Sì sì sì sì sì",
    
    # Alemão
    "Ja", "Jap", "Jup", "Jo", "Jawohl", "Genau", "Sicher", "Klar", "Natürlich", 
    "Selbstverständlich", "Aber sicher", "Natürlich, mein Freund", "Auf jeden Fall", 
    "Ohne Zweifel", "Absolut", "Bestimmt", "Auf jeden Fall, mein Freund", "Sicherlich", 
    "Einverstanden", "Aber ja", "Ja, natürlich", "Ganz genau", "Gewiss", "Ja klar", 
    "Natürlich, Chef", "Auf jeden Fall, Chef", "Sicherlich, Chef", "Aber sicher doch", 
    "Natürlich"
]

load_dotenv('.venv/certificate.env')

# Obtém o caminho do certificado e a URL do banco de dados
cert_path = os.getenv('FIREBASE_CERTIFICATE_PATH')
database_url = os.getenv('DATABASE_URL')
LinkIP = os.getenv('Link_URL')

link = firebase_admin.credentials.Certificate(cert_path)
id = requests.get(LinkIP).text
default_app = firebase_admin.initialize_app(link, {
    'databaseURL': database_url
})
ref = db.reference("/")
data = ref.get()
saldo = randrange(1200)

def limpar():
      print("\n" * 300)

def restart():
     resposta = input("Deseja ir para o loguin? Digite s/n ")
     if resposta.lower() in sim:
         loguin()
         
def Cadastro():
     user = input("Digite seu nome de usuario: ")
     senha = input("Digite uma senha: ")
     if not user or not senha: 
          print("Você precisa colocar um valor aqui bebe >:(")
     else:
           senhadb = db.reference(f'/{user}')
           senhadb.set({
                 'senha': senha,
                        'saldo': saldo})

def loginAutomatico():
    global user
    global ref
    global login
    for user, ref in data.items():
        if 'IP' in ref and ref['IP'] == id:
            print(f"Login automático bem-sucedido!")
            login = True
            break  # Adicionei um break para sair do loop após encontrar o usuário
    else:
        print("Login automático falhou. Redirecionado para login manual.")
        login = False
        return

loginAutomatico()

banco = db.reference(f"/{user}")

def painel():
     valores = input(
          "Olá, este é o KaueBank, o que deseja?\n"
          "1- Ver Saldo Bancário.\n"
          "2- Transferir valor para outro cliente.\n"
          "3- Ver quanto seu dinheiro esta rendendo.\n"
          "4- Roubar um Cartao de crédito.\n"
          "5- Retirar login automático\n"
          "Qualquer coisa estou a disposição!\n"
          "\n"
          "\n"
          "\n"
          "Digite um numero:"
                          )
     if valores == "1":
          print("Seu saldo é: ")
          print( ref.get('saldo'))
          retornar = input("Quer retornar ao inicio?")
          if retornar in sim:
               limpar()
               painel()
     if valores == "2":
        print("Seu saldo é: ")
        ValorCarteira = ref.get('saldo')
        print(ref.get('saldo'))
        ValorTransf = int(input( "Quanto voce quer tranferir? "))
        QuemMandar = input("Para quem você quer mandar? ")
        valor = ValorCarteira - ValorTransf
        banco.update({
            'saldo': valor
                 })
        Local = db.reference(f"/{QuemMandar}/saldo")
        LocalUpdate = db.reference(f"/{QuemMandar}")
        valor2 = Local.get()
        result = (valor2 + ValorTransf)
        LocalUpdate.update({'saldo': result })
        print("seu novo valor é ")
        print(ref['saldo'])
        voltar = input("Quer voltar ao inicio? s/n ")
        if voltar in sim :
            painel()
     if valores == "3":
         data_armazenada = ref.get('data')
         data  = datetime.strptime(data_armazenada, "%Y-%m-%d %H:%M:%S.%f")

         Horario = datetime.now()
         banco.update({
             "data": Horario.strftime("%Y-%m-%d %H:%M:%S.%f")
         })
         diferenca = Horario - data
         horas_passadas = diferenca.total_seconds() / 3600
         Valor_Saldo = ref.get('saldo')
         saldo = Valor_Saldo * (1 + 0.05) ** horas_passadas

         banco.update({
             'saldo': saldo
         })
         print("Saldo anterior:", Valor_Saldo)
         print("Saldo atualizado:", saldo)
         lucro = Valor_Saldo - saldo
         print("seu lucro foi de: ", lucro)
     if valores == "4":
         print("AI AI SEU DANADINHO(A)\n"
               "TENTANDO ROUBAR CARTAO\n"
               "SE DEUS MULTIPLICOU, NÃO QUER DIZER QUE VOCÊ TAMBEM PODE\n"
               "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
         voltar = input("quer voltar? s/n")
         if voltar in sim:
               painel()
     if valores == "5":
          tirar = input("realmente quer remover o login automatico? s/n")
          if tirar in sim:
              banco.update({ 
               'IP': ""   
              })
              print("login Deletado")
              return

     

def loguin():
    limpar()
    User_conta = input("Digite seu usuario: ")
    Senha_conta = input("Digite sua senha: ")
    limpar()
    dados = db.reference(f"/{User_conta}").get()
    IDSave = db.reference(f"/{User_conta}")
    if   dados['senha'] == Senha_conta:
         logado = True
         manter = input("Deseja continuar logado? Digite s/n ")	
         if manter in sim:
          IDSave.update({'IP': id})
          print("Após o inicio do programa você estará logado!")
          print("Bem-vindo,", User_conta, "</>")
          painel()
         else:    
          print("Bem-vindo,", User_conta, "</>")
          painel()
         
    elif User_conta not in dados:
         print(User_conta, dados)
         print("Usuario Não encontrado!")
         limpar()
         loguin()
    else:
      print("Senha incorreta!!!!")

if login == False:
     Criar = input("Precisa criar uma conta? ")
     limpar()
     if Criar in sim:
      Cadastro()
      restart()
     else:
      loguin()

if login == True:	
      print("Bem-vindo,", user, "</>")
      painel()
