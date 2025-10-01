import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração do servidor Expresso (exemplo, troque pelos dados reais)
SMTP_SERVER = "smtp.seudominio.gov.br"  # servidor SMTP do Expresso
SMTP_PORT = 587  # ou 465 dependendo da configuração
EMAIL = "beatriz.paredes@empetur.pe.gov.br"
SENHA = "99696723san"

ARQUIVO_CONTATOS = "contatos.csv"

# Conexão com o servidor
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()  # se a porta for 587; se for 465, usar smtplib.SMTP_SSL
server.login(EMAIL, SENHA)

with open(ARQUIVO_CONTATOS, newline='', encoding='utf-8') as csvfile:
    contatos = csv.DictReader(csvfile)

    for contato in contatos:
        nome = contato["nome"]
        destinatario = contato["email"]

        assunto = "Aviso Importante"
        corpo = f"""
        Olá, {nome},

        Esta é uma mensagem enviada via Expresso.

        Atenciosamente,
        Sua Equipe
        """

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo, "plain"))

        server.sendmail(EMAIL, destinatario, msg.as_string())
        print(f"E-mail enviado para {nome} - {destinatario}")

server.quit()
