# Portal do Fluxo de Compras - Educacross

Este é o código-fonte do site do Portal do Fluxo de Compras, desenvolvido em Flask.

## Estrutura do Projeto

-   `/src/main.py`: Arquivo principal da aplicação Flask, contém as rotas, a lógica do formulário de solicitação e a funcionalidade de upload de arquivos.
-   `/src/templates/`: Contém os arquivos HTML do site.
    -   `base.html`: Layout base para todas as páginas (inclui o modal de upload).
    -   `index.html`: Página inicial (hub de informações).
    -   `carta_abertura_page.html`: Página da Carta de Abertura.
    -   `fluxo_compras_page.html`: Página do Fluxo de Compras Detalhado (com fluxograma e ícone de edição).
    -   `formulario_solicitacao_page.html`: Página com o formulário de solicitação.
    -   `modelos_email_page.html`: Página com os modelos de e-mail.
    -   `apresentacao_page.html`: Página com o conteúdo da apresentação (com ícone de edição e link para download).
    -   `planilha_rastreamento_page.html`: Página com o modelo da planilha (com ícone de edição e link para download).
    -   `*.html` (arquivos de conteúdo): Arquivos de conteúdo incluídos nas páginas principais.
-   `/src/static/`: Contém os arquivos estáticos.
    -   `/css/style.css`: Folha de estilos principal.
    -   `/js/script.js`: Código JavaScript para interatividade (incluindo a lógica do modal de upload).
    -   `/images/`: Imagens utilizadas no site (ex: `fluxo_compras_visual.png`).
    -   `/downloads/`: Arquivos para download (ex: `apresentacao_fluxo_compras.pptx`, `planilha_rastreamento_compras.xlsx`).
-   `requirements.txt`: Lista de dependências Python do projeto.
-   `venv/`: Ambiente virtual Python (não incluído no zip de distribuição, mas gerado ao rodar).

## Funcionalidade do Formulário de Solicitação

O formulário na página "Formulário de Solicitação" coleta dados e **simula** o envio de um e-mail para `leonardo.pontes@educacross.com.br`. Os detalhes do e-mail são impressos no console do servidor.

**Para habilitar o envio real de e-mails:**

1.  Configure um servidor SMTP.
2.  Atualize as variáveis `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `EMAIL_SENDER` em `src/main.py`.
3.  Descomente e ajuste o bloco de código de envio de e-mail em `src/main.py`.

## Funcionalidade de Substituição de Arquivos (Upload)

O portal permite a substituição de arquivos específicos diretamente pela interface. Um ícone de edição (✏️) aparecerá ao lado dos seguintes itens:

-   Imagem do Fluxograma (na página "Fluxo de Compras")
-   Arquivo da Apresentação (na página "Apresentação")
-   Arquivo da Planilha de Rastreamento (na página "Planilha de Rastreamento")

**Como substituir um arquivo:**

1.  Clique no ícone de edição (✏️) ao lado do item que deseja atualizar.
2.  Um formulário (modal) aparecerá solicitando uma senha e o novo arquivo.
3.  Digite a senha de upload: `ManuscritoSeguro123`
4.  Clique em "Selecionar novo arquivo" e escolha o arquivo do seu computador.
    *   Para a imagem do fluxograma, são permitidos arquivos: `.png`, `.jpg`, `.jpeg`, `.gif`.
    *   Para a apresentação e planilha, são permitidos arquivos: `.pptx`, `.xlsx`, `.docx`, `.pdf`.
5.  Clique em "Enviar Novo Arquivo".
6.  Você receberá uma mensagem de sucesso ou erro. Se for sucesso, o arquivo no servidor será substituído.
    *   A imagem do fluxograma será atualizada visualmente na página sem a necessidade de recarregar (para evitar cache do navegador).
    *   Para os arquivos de download (apresentação, planilha), pode ser necessário recarregar a página para que o link de download aponte para a versão mais recente, ou o link será atualizado dinamicamente se possível.

**Importante:** A senha `ManuscritoSeguro123` está definida diretamente no código (`src/main.py`). Para um ambiente de produção mais seguro, considere armazená-la como uma variável de ambiente ou utilizar um sistema de autenticação mais robusto.

## Executando Localmente (para desenvolvimento/teste)

1.  Certifique-se de ter Python 3 e pip instalados.
2.  Navegue até a pasta raiz do projeto (`educacross_fluxo_compras`).
3.  Crie um ambiente virtual: `python3 -m venv venv`
4.  Ative o ambiente virtual:
    *   Linux/macOS: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate`
5.  Instale as dependências: `pip install -r requirements.txt`
6.  Execute a aplicação: `python3 src/main.py`
7.  Acesse o site em `http://127.0.0.1:8081` no seu navegador.

Lembre-se que a funcionalidade de envio de e-mail real não funcionará localmente sem a configuração SMTP mencionada acima.

