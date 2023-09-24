# Instruções para Executar os Projetos LLM Client e LLM Server

Este README fornece instruções detalhadas sobre como executar os projetos LLM Client e LLM Server. Certifique-se de seguir as etapas abaixo para configurar e executar ambos os projetos com sucesso.

## LLM Client

1. Primeiro, navegue para o diretório `llm-client` usando o terminal:

```bash
cd llm-client
```

2. Instale as dependências necessárias executando o comando:

```bash
npm install
```

3. Após a instalação das dependências, você pode iniciar o cliente LLM executando:

```bash
npm run dev
```

Isso iniciará o cliente LLM e você poderá usá-lo normalmente.

## LLM Server

1. Navegue para o diretório `llm-server` usando o terminal:

```bash
cd llm-server
```

2. Abra o arquivo `app.py` em um editor de texto ou IDE de sua escolha.

3. Procure pela variável `api_key` no código e substitua-a pela sua chave de API OpenAI, se necessário. Certifique-se de que a chave de API seja válida.

4. Salve as alterações no arquivo `app.py`.

5. Para executar o servidor LLM, use o seguinte comando:

```bash
python app.py
```

O servidor será iniciado e estará pronto para receber solicitações.

Agora você tem o LLM Client e o LLM Server configurados e em execução. Certifique-se de seguir todas as etapas para garantir que ambos os projetos funcionem corretamente. Se você encontrar algum problema durante o processo, verifique as etapas e assegure-se de que todas as dependências estejam instaladas corretamente e que as configurações de chave da API estejam corretas.
