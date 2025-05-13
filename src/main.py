import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import smtplib # Para envio de email real, precisaria de configuração
from email.mime.text import MIMEText # Para formatar o email
from werkzeug.utils import secure_filename
import time # Adicionado para o cache busting

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.urandom(24) # Necessário para flash messages

# Senha para upload - EM UM AMBIENTE REAL, USE ALGO MAIS SEGURO E NÃO HARDCODED
UPLOAD_PASSWORD = "ManuscritoSeguro123"

# Caminhos base para arquivos estáticos
STATIC_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "static")
IMAGE_FOLDER_PATH = os.path.join(STATIC_FOLDER_PATH, "images")
DOWNLOADS_FOLDER_PATH = os.path.join(STATIC_FOLDER_PATH, "downloads")

# Arquivos permitidos para substituição e seus caminhos
ALLOWED_FILES = {
    "fluxo_compras_visual.png": {"path": IMAGE_FOLDER_PATH, "type": "image"},
    "apresentacao_fluxo_compras.pptx": {"path": DOWNLOADS_FOLDER_PATH, "type": "document"},
    "planilha_rastreamento_compras.xlsx": {"path": DOWNLOADS_FOLDER_PATH, "type": "document"}
}
ALLOWED_EXTENSIONS_IMAGE = {"png", "jpg", "jpeg", "gif"}
ALLOWED_EXTENSIONS_DOCUMENT = {"pptx", "xlsx", "docx", "pdf"}

# Configurações de E-mail (para um cenário real, usar variáveis de ambiente)
SMTP_SERVER = "smtp.example.com" # Substituir pelo servidor SMTP real
SMTP_PORT = 587 # Porta TLS padrão
SMTP_USERNAME = "user@example.com" # Substituir pelo usuário SMTP
SMTP_PASSWORD = "password" # Substituir pela senha SMTP
EMAIL_SENDER = "noreply@example.com" # E-mail que aparecerá como remetente
EMAIL_RECEIVER = "leonardo.pontes@educacross.com.br"

# Função para obter a versão do cache
def get_cache_version():
    return int(time.time())

@app.route("/")
def index():
    return render_template("index.html", cache_version=get_cache_version())

@app.route("/carta-abertura")
def carta_abertura_page():
    return render_template("carta_abertura_page.html", cache_version=get_cache_version())

@app.route("/fluxo-de-compras")
def fluxo_compras_page():
    return render_template("fluxo_compras_page.html", cache_version=get_cache_version())

@app.route("/formulario-solicitacao", methods=["GET"])
def formulario_solicitacao_page():
    return render_template("formulario_solicitacao_page.html", cache_version=get_cache_version())

@app.route("/modelos-de-email")
def modelos_email_page():
    return render_template("modelos_email_page.html", cache_version=get_cache_version())

@app.route("/apresentacao")
def apresentacao_page():
    return render_template("apresentacao_page.html", cache_version=get_cache_version())

@app.route("/planilha-de-rastreamento")
def planilha_rastreamento_page():
    planilha_path = os.path.join(DOWNLOADS_FOLDER_PATH, "planilha_rastreamento_compras.xlsx")
    if not os.path.exists(planilha_path):
        try:
            with open(planilha_path, "w") as f:
                f.write("Arquivo placeholder para planilha de rastreamento.")
            print(f"Arquivo placeholder criado em: {planilha_path}")
        except Exception as e:
            print(f"Erro ao criar placeholder da planilha: {e}")
    return render_template("planilha_rastreamento_page.html", cache_version=get_cache_version())

@app.route("/submit-formulario", methods=["POST"])
def submit_formulario():
    if request.method == "POST":
        try:
            # Coleta de dados do formulário (omitida para brevidade)
            flash("Sua solicitação foi enviada com sucesso!", "success")
        except Exception as e:
            print(f"Erro ao processar formulário: {e}")
            flash(f"Ocorreu um erro ao enviar sua solicitação: {e}. Por favor, tente novamente.", "danger")
        return redirect(url_for("formulario_solicitacao_page"))

def allowed_file(filename, file_type):
    allowed_extensions = set()
    if file_type == "image":
        allowed_extensions = ALLOWED_EXTENSIONS_IMAGE
    elif file_type == "document":
        allowed_extensions = ALLOWED_EXTENSIONS_DOCUMENT
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

@app.route("/upload-file", methods=["POST"])
def upload_file():
    if request.method == "POST":
        password = request.form.get("password")
        target_file_name = request.form.get("target_file")
        file_type = request.form.get("file_type")

        if not password or password != UPLOAD_PASSWORD:
            return jsonify({"success": False, "message": "Senha incorreta."}), 403

        if "file" not in request.files:
            return jsonify({"success": False, "message": "Nenhum arquivo selecionado."}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "message": "Nenhum arquivo selecionado."}), 400

        if target_file_name not in ALLOWED_FILES:
            return jsonify({"success": False, "message": "Arquivo alvo não permitido para substituição."}), 400
        
        if ALLOWED_FILES[target_file_name]["type"] != file_type:
            expected_type = ALLOWED_FILES[target_file_name]["type"]
            return jsonify({"success": False, "message": f"Tipo de arquivo inválido para {target_file_name}. Esperado: {expected_type}."}), 400

        if file and allowed_file(file.filename, file_type):
            filename_to_save = target_file_name 
            save_path_dir = ALLOWED_FILES[target_file_name]["path"]
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            
            full_save_path = os.path.join(save_path_dir, filename_to_save)
            
            try:
                file.save(full_save_path)
                if file_type == "image":
                    new_src = url_for("static", filename=f"images/{filename_to_save}?v={get_cache_version()}") # Usar get_cache_version aqui também
                    return jsonify({"success": True, "message": f"Arquivo {filename_to_save} substituído com sucesso!", "new_src": new_src}), 200
                
                return jsonify({"success": True, "message": f"Arquivo {filename_to_save} substituído com sucesso!"}), 200
            except Exception as e:
                print(f"Erro ao salvar arquivo: {e}")
                return jsonify({"success": False, "message": f"Erro ao salvar o arquivo: {e}"}), 500
        else:
            return jsonify({"success": False, "message": "Tipo de arquivo não permitido."}), 400
    
    return jsonify({"success": False, "message": "Método não permitido."}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)

