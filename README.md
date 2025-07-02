# 📄 OpenRouter PDF Reader

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-enabled-blueviolet)](https://openrouter.ai)
[![GUI](https://img.shields.io/badge/interface-Tkinter-lightgrey)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<table>
  <tr>
    <td>
      <img src=https://github.com/user-attachments/assets/45d9d29a-2475-4354-850f-9f2b75a53fc7 width="700" alt="App Preview">
    </td>
    <td>
      <p align="center">
        A minimal GUI Python app for making local requisitions to prompt OpenRouter API models (free or token charged) about submited, parsed .pdf files.<br>
      </p>
    </td>
  </tr>
</table>

---


### ATTENTION: Uploading large .pdf files, even parsed, may spend a lot of tokens. If the file is larger than the context window, it will be separated in two requests, possibly consuming more tokens than expected. For more information on token charging consult API documentation.
---
## 🔑 Get your OpenRouter API Key

1. Visit [https://openrouter.ai/keys](https://openrouter.ai/keys)  
2. Log in or sign up  
3. Copy your API key  
4. Paste it into the app input field when prompted
5. *Default model set to Deepseek free*

## ⚡ Quick Start

```bash
git clone https://github.com/naranjii/openrouter-pdf-reader.git
cd openrouter-pdf-reader
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

- Paste your OpenRouter API Key  
- Select a PDF  
- Prompt a question

---

## 📝 License

MIT — see [LICENSE](./LICENSE)

---

## 🇧🇷 Versão em Português
## ⚡ Comece Aqui

```bash
git clone https://github.com/naranjii/openrouter-pdf-reader.git
cd openrouter-pdf-reader
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
python app.py
```

- Cole sua chave OpenRouter  
- Selecione um PDF  
- Faça sua pergunta — pronto ✅

---

## 🔑 Obtenha sua chave da OpenRouter

1. Acesse [https://openrouter.ai/keys](https://openrouter.ai/keys)  
2. Faça login ou crie uma conta  
3. Copie a chave  
4. Cole no campo de entrada do app
5. *Modelo está configurado para Deepseek versão free*
---

> Projeto simples, sem dependências externas além do Tkinter + bibliotecas padrão do Python feito para estudar chamadas à api com UI.
