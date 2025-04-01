APP Mobile + REST API para Gestão de Alunos



🥋 Judo Academy Manager

APP Mobile + REST API para Gestão de Alunos

🌟 Visão Geral
Sistema integrado para academias de judô, combinando um aplicativo mobile desenvolvido com Flet (Python) e uma API RESTful com Django. Permite o gerenciamento completo de alunos, acompanhamento de progresso e registro de aulas.

📋 Funcionalidades Principais
📱 Aplicativo Mobile (Flet)
Janela interativa com navegação intuitiva

Cadastro de Alunos: Inclusão de dados pessoais, faixa, peso e histórico médico

Listagem Completa: Visualização de todos alunos com filtros por faixa/idade

Progresso do Aluno: Registro de evolução técnica (kihon, kata, randori)

Controle de Aulas: Marcação de presenças e conteúdos trabalhados

Edição de Dados: Atualização de informações do aluno

🌐 Backend API (Django REST)
Endpoints REST para todas operações CRUD

Autenticação JWT para instrutores

Banco de dados relacional (SQLite/PostgreSQL)

Documentação automática com Swagger

🛠️ Tecnologias Utilizadas
Backend	Frontend Mobile	Bibliotecas
Python 3.11	Flet (UI Multiplataforma)	flet (0.22.0)
Django 5.0	Componentes Customizados	requests (2.31.0)
Django REST Framework	Layout Responsivo	httpx (0.27.0)
SQLite (Dev) / PostgreSQL (Prod)		django-cors-headers
