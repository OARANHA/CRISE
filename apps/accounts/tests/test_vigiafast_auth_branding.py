"""Regressões sintéticas da primeira fatia de identidade VIGIAFAST.

Não atestam que toda a aplicação esteja traduzida nem pronta para clientes reais.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_mostra_identidade_vigiafast_e_mantem_fluxo_de_autenticacao(client):
    response = client.get(reverse("account_login"))

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert '<html lang="pt-BR"' in html
    assert "<title>Entrar · VIGIAFAST</title>" in html
    assert "Bem-vindo ao VIGIAFAST" in html
    assert "Esqueceu sua senha?" in html
    assert "csrfmiddlewaretoken" in html
    assert 'method="post"' in html
    assert "BrightBean · Studio" not in html


@pytest.mark.django_db
def test_dashboard_sem_workspace_exibe_orientacao_em_portugues(client, django_user_model):
    usuario = django_user_model.objects.create_user(
        email="operador-sintetico@example.test",
        password="senha-sintetica-de-teste",
    )
    client.force_login(usuario)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert '<html lang="pt-BR"' in html
    assert "Nenhum espaço de trabalho disponível" in html
    assert "Nome do espaço de trabalho" in html
    assert "Criar espaço de trabalho" in html
    assert 'method="post"' in html
    assert "csrfmiddlewaretoken" in html
