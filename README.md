# Análise de Fundos Imobiliários

Este projeto realiza a análise de fundos imobiliários utilizando técnicas de web scraping, processamento de dados e avaliação com modelos de linguagem (LLMs) como o Qwen. Ele coleta dados de fontes públicas, processa as informações e gera relatórios e avaliações automatizadas.

## Pré-requisitos

Antes de executar o projeto, você precisará instalar as seguintes ferramentas e dependências:

### 1. **Instalar o Python**

- Baixe e instale o Python a partir do site oficial: [python.org](https://www.python.org/).
- Não esqueça de marcar a opção **"Add Python to PATH"** durante a instalação.

### 2. **Instalar o Ollama**

- O Ollama é a ferramenta que vamos utilizar para gerenciar e executar a LLM.
- Siga as instruções de instalação no repositório oficial: [Ollama GitHub](https://github.com/jmorganca/ollama).

### 3. **Baixar os Modelos Qwen**

- Após instalar o Ollama, vamos baixar os modelos Qwen necessários:
  ```bash
  ollama run qwen2.5:3b
  ollama run qwen2.5:7b
  ```
- Esses modelos serão usados para avaliação de notícias e geração de relatórios.

---

## Como Executar o Projeto

1. **Ativar o Ambiente Virtual**

   - Certifique-se de que o ambiente virtual está ativado:
     ```bash
     source venv/bin/activate  # Linux/Mac
     venv\Scripts\activate     # Windows
     ```

2. **Executar o Script Principal**

   - Navegue até a pasta `/src` e execute o script `main.py`:
     ```bash
     cd src
     python main.py
     ```

3. **Entrada de Dados**

   - O script solicitará o nome do fundo imobiliário. Digite o código do fundo (ex: `MXRF11`) ou vários códigos separados por vírgula (ex: `MXRF11, HGLG11`).

4. **Resultados**
   - Os resultados das análises serão salvos na pasta `/output/results`.

---

## Configurações Adicionais

### 1. **Adicionar Novos Fundos**

- Para adicionar novos fundos à análise, edite o arquivo `/data/fundos_setores.json` com o código do fundo e seu setor correspondente.
- É feita essa separação para futuramente incluir geração de carteira diversificada, fazendo analise e comparando fundo de setores diferentes.

### 2. **Personalizar Modelos de Linguagem**

- Se desejar usar outros modelos além do Qwen, consulte a documentação do Ollama para baixar e configurar modelos adicionais.
- Modelos como o "Deepseek-R1" precisam de alterações por conta do "think".

---

## Dependências do Projeto

As principais bibliotecas utilizadas no projeto estão listadas no arquivo `docs/requirements.txt`. Aqui estão algumas das principais:

- **Selenium**: Para web scraping de notícias, porém ainda não implementado.
- **BeautifulSoup4**: Para análise de HTML.
- **Requests**: Para fazer requisições HTTP.
- **Pandas**: Para manipulação de dados.
- **Ollama**: Para integração com modelos de linguagem.

---

## Contribuição

Se você deseja contribuir para o projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Adicionando nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## Contato

Se tiver dúvidas ou sugestões, entre em contato:

- **Nome**: David Ramos
- **Email**: social@davidramos.com.br
- **GitHub**: davidramosbr
