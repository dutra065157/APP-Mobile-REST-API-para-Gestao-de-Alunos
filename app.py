
import flet as ft
import requests  # Importa a biblioteca requests para fazer requisições HTTP.


# Define a URL base da API que será utilizada.
API_BASE_URL = "http://127.0.0.1:8000/api"


# Função principal que define a estrutura da página Flet.
def main(page: ft.Page):

    page.title = "CADASTRO ALUNOS"  # Define o título da página.

    # criar aluno

    # Cria um campo de texto para o nome do aluno.
    nome_field = ft.TextField(label="Nome")
    # Cria um campo de texto para o email do aluno.
    email_field = ft.TextField(label="Email")
    # Cria um campo de texto para a faixa do aluno.
    faixa_field = ft.TextField(label="Faixa")
    data_nascimento_field = ft.TextField(  # Cria um campo de texto para a data de nascimento do aluno.
        label="Data de Nascimento (YYYY-MM-DD)")
    # Cria um elemento de texto para exibir o resultado da criação do aluno.
    create_result = ft.Text()

    # Mensagem de erro
    error_text = ft.Text(color=ft.colors.RED, visible=False)

    # Função chamada quando o botão "Criar Aluno" é clicado.
    def criar_aluno_click(e):

        if not (nome_field.value and email_field.value and faixa_field.value and data_nascimento_field.value):
            error_text.value = "Por favor, preencha todos os campos!"
            error_text.visible = True
            page.update()
            return

        # Se todos os campos estiverem preenchidos
        error_text.visible = False
        page.update()

        payload = {  # Cria um dicionário com os dados do aluno a serem enviados na requisição.
            "nome": nome_field.value,
            "email": email_field.value,
            "faixa": faixa_field.value,
            "data_nascimento": data_nascimento_field.value,
        }
        # limpa campos
        nome_field.value = ""
        email_field.value = ""
        faixa_field.value = ""
        data_nascimento_field.value = ""

        # Faz uma requisição POST para a API para criar o aluno.
        response = requests.post(API_BASE_URL + "/", json=payload)
        # Verifica se a requisição foi bem-sucedida.
        if response.status_code == 200:
            # Converte a resposta JSON em um dicionário Python.
            aluno = response.json()
            # Exibe a mensagem de sucesso com os dados do aluno criado.
            create_result.value = f"Aluno criado: {aluno}"
        else:
            # Exibe a mensagem de erro retornada pela API.
            create_result.value = f"Erro: {response.text}"

        page.update()  # Atualiza a página para exibir os resultados.

    create_button = ft.ElevatedButton(  # Cria um botão "Criar Aluno".
        text="Criar Aluno", on_click=criar_aluno_click)

    # Organiza os campos e o botão em uma coluna.

    criar_aluno_tab = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_nascimento_field,
            create_button,
            create_result,
        ],
        # Adiciona rolagem à coluna caso o conteúdo seja maior que a tela.
        scroll=True,
    )

    # listar alunos

    students_table = ft.DataTable(  # Cria uma tabela para exibir a lista de alunos.
        columns=[

            ft.DataColumn(ft.Text("Nome")),  # Define as colunas da tabela.
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Faixa")),
            ft.DataColumn(ft.Text("Data Nascimento")),
        ],

        rows=[],  # Inicializa a lista de linhas da tabela vazia.

    )

    # Cria um elemento de texto para exibir o resultado da listagem.
    list_result = ft.Text()

    # Função chamada quando o botão "Listar Alunos" é clicado.
    def listar_alunos_click(e):

        try:
            # Faz uma requisição GET para a API para listar os alunos.
            response = requests.get(API_BASE_URL + "/alunos/")
            # Verifica se a requisição foi bem-sucedida.
            if response.status_code == 200:
                # Converte a resposta JSON em uma lista de dicionários Python.
                alunos = response.json()
                # Limpa as linhas anteriores
                # Limpa as linhas existentes na tabela antes de adicionar as novas.
                students_table.rows.clear()
                for aluno in alunos:  # Itera sobre a lista de alunos retornada pela API.
                    row = ft.DataRow(  # Cria uma nova linha para a tabela.
                        cells=[

                            # Adiciona as células com os dados do aluno.
                            ft.DataCell(ft.Text(aluno.get("nome", ""))),
                            ft.DataCell(ft.Text(aluno.get("email", ""))),
                            ft.DataCell(ft.Text(aluno.get("faixa", ""))),
                            ft.DataCell(
                                ft.Text(aluno.get("data_nascimento", ""))),
                        ]

                    )
                    # Adiciona a linha à tabela.
                    students_table.rows.append(row)
                # Exibe a mensagem com a quantidade de alunos encontrados.
                list_result.value = f"{len(alunos)} alunos encontrados."
            else:
                # Exibe a mensagem de erro retornada pela API.
                list_result.value = f"Erro: {response.text}"
        except Exception as ex:  # Captura possíveis exceções durante a requisição.
            # Exibe a mensagem de exceção.
            list_result.value = f"Exceção: {ex}"

        page.update()  # Atualiza a página para exibir os resultados.

    list_button = ft.ElevatedButton(  # Cria um botão "Listar Alunos".
        text="Listar Alunos", on_click=listar_alunos_click)

    listar_alunos_tab = ft.Column([
        list_button, students_table, list_result

    ],
        expand=True, scroll=True


    )

    # adicionar aula
    # Campo para email do aluno para adicionar aula.
    email_aula_field = ft.TextField(label="Email do Aluno")
    # Campo para quantidade de aulas, valor padrão 1.
    qtd_field = ft.TextField(label="Quantidade de Aulas", value="1")
    # Texto para exibir o resultadoe da adição de aulas.
    aula_result = ft.Text()

    # Função chamada ao clicar no botão "Marcar Aula Realizada".
    def marcar_aula_click(e):

        payload = {  # Dados da aula a serem enviados na requisição.
            # Quantidade de aulas (convertida para inteiro).
            "qtd": int(qtd_field.value),
            "email_aluno": email_aula_field.value,  # Email do aluno.
        }
        qtd_field.value = ""
        email_aula_field.value = ""
        response = requests.post(  # Requisição POST para a API para marcar a aula.
            API_BASE_URL + "/aula_realizada/", json=payload)
        # Verifica se a requisição foi bem-sucedida.
        if response.status_code == 200:
            # Exibe a mensagem de sucesso com a resposta da API.
            aula_result.value = f"Sucesso:{response.json()}"
        else:
            # Exibe a mensagem de erro.
            aula_result.value = f"Erro: {response.text}"

        page.update()  # Atualiza a página.

    aula_button = ft.ElevatedButton(  # Botão "Marcar Aula Realizada".
        text="Marcar Aula Realizada", on_click=marcar_aula_click)

    # Organiza os campos e o botão em uma coluna.
    aula_tab = ft.Column([email_aula_field, qtd_field,
                          # Adiciona rolagem.
                          aula_button, aula_result], scroll=True)

    # progresso aluno

    # Campo para email do aluno para consultar o progresso.
    email_progress_field = ft.TextField(label="Email do Aluno")

    progress_result = ft.Text()  # Texto para exibir o resultado do progresso.

    # Função chamada ao clicar em "Consultar Progresso".

    def consultar_progresso_click(e):

        email = email_progress_field.value  # Obtém o email do aluno.
        email_progress_field.value = ""

        response = requests.get(  # Requisição GET para a API para obter o progresso.
            API_BASE_URL + '/progresso_aluno/', params={'email_aluno': email})
        # Verifica se a requisição foi bem-sucedida.
        if response.status_code == 200:
            # Converte a resposta JSON em um dicionário.
            progress = response.json()
            progress_result.value = (  # Formata a string com as informações de progresso.
                f"Nome: {progress.get('nome')}\n"
                f"Email: {progress.get('email')}\n"
                f"Faixa: {progress.get('faixa')}\n"
                f"Total de aulas: {progress.get('total_aulas')}\n"
                f"Aulas necessarias para proxima faixa: {progress.get('aulas_necessarias_para_proxima_faixa')}\n"
            )

        else:
            # Exibe a mensagem de erro.
            progress_result.value = f"Erro: {response.text}"

        page.update()  # Atualiza a página.

    progress_button = ft.ElevatedButton(  # Botão "Consultar Progresso".
        text="Consultar Progresso", on_click=consultar_progresso_click)

    # Organiza os campos e o botão em uma coluna.

    progresso_tab = ft.Column(
        # Adiciona rolagem.
        [email_progress_field, progress_button, progress_result], scroll=True)

    # Atualizar Aluno

    # Campo para o ID do aluno para atualização.
    id_aluno_field = ft.TextField(label="ID do Aluno")
    # Campo para o novo nome.
    nome_update_field = ft.TextField(label="Novo Nome")
    # Campo para o novo email.
    email_update_field = ft.TextField(label="Novo Email")
    # Campo para a nova faixa.
    faixa_update_field = ft.TextField(label="Nova Faixa")
    data_nascimento_update_field = ft.TextField(  # Campo para a nova data de nascimento.
        label="Nova Data de Nascimento (YYYY-MM-DD)")
    update_result = ft.Text()  # Texto para exibir o resultado da atualização.

    # Função chamada ao clicar em "Atualizar Aluno".
    def atualizar_aluno_click(e):

        aluno_id = id_aluno_field.value  # Obtém o ID do aluno.
        if not aluno_id:  # Verifica se o ID do aluno foi fornecido.
            update_result.value = "ID do aluno é necessário."
        else:
            payload = {  # Dados a serem enviados na requisição PUT.
                "nome": nome_update_field.value,
                "email": email_update_field.value,
                "faixa": faixa_update_field.value,
                "data nascimento": data_nascimento_update_field.value,
            }
            id_aluno_field.value = ""
            nome_update_field.value = ""
            email_update_field.value = ""
            faixa_update_field.value = ""
            data_nascimento_update_field.value = ""
            print(payload)  # Imprime os dados (para depuração).

            response = requests.put(  # Requisição PUT para a API para atualizar o aluno.
                API_BASE_URL + f"/alunos/{aluno_id}", json=payload)
            # Imprime o código de status da resposta (para depuração).
            print(response.status_code)
            # Verifica se a requisição foi bem-sucedida.
            if response.status_code == 200:
                # Converte a resposta JSON em um dicionário.
                aluno = response.json()
                # Exibe a mensagem de sucesso.
                update_result.value = f"Aluno atualizado: {aluno}"
            else:
                # Exibe a mensagem de erro.
                update_result.value = f"Erro: {response.text}"

            page.update()  # Atualiza a página.

    update_button = ft.ElevatedButton(  # Botão "Atualizar Aluno".
        text="Atualizar Aluno", on_click=atualizar_aluno_click)

    atualizar_tab = ft.Column(  # Organiza os campos e o botão em uma coluna.
        [
            id_aluno_field,
            nome_update_field,
            email_update_field,
            faixa_update_field,
            data_nascimento_update_field,
            update_button,
            update_result,
        ],
        scroll=True,  # Adiciona rolagem.
    )

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Criar Aluno",
                content=ft.Container(
                     content=criar_aluno_tab,
                     alignment=ft.alignment.center,
                     padding=20
                )
            ),
            ft.Tab(
                text="Listar Alunos",
                content=ft.Container(
                     content=listar_alunos_tab,
                     alignment=ft.alignment.center,
                     padding=20
                )
            ),
            ft.Tab(
                text="Aula realizada",
                content=ft.Container(
                     content=aula_tab,
                     alignment=ft.alignment.center,
                     padding=20
                )
            ),
            ft.Tab(
                text="Progresso do aluno",
                content=ft.Container(
                     content=progresso_tab,
                     alignment=ft.alignment.center,
                     padding=20
                )
            ),
            ft.Tab(
                text="Atualizar aluno",
                content=ft.Container(
                     content=atualizar_tab,
                     alignment=ft.alignment.center,
                     padding=20
                )
            ),
        ],
        expand=True
    )

    page.add(
        ft.Container(
            content=tabs,
            alignment=ft.alignment.center,
            expand=True,
            padding=20
        ), error_text
    )


if __name__ == "__main__":
    ft.app(target=main)
# Inicializa a aplicação Flet.
