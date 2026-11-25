from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Organizacao, Perfil
from .models import Categoria, Comentario, Post


class DashboardTest(TestCase):
    def setUp(self):
        self.org_a = Organizacao.objects.create(nome="Org A")
        self.org_b = Organizacao.objects.create(nome="Org B")
        self.org_vazia = Organizacao.objects.create(nome="Org Vazia")

        self.user_a = User.objects.create_user(username="admin_a", password="123")
        self.perfil_a = Perfil.objects.create(
            usuario=self.user_a, organizacao=self.org_a, papel="admin"
        )

        self.user_op = User.objects.create_user(username="op_a", password="123")
        self.perfil_op = Perfil.objects.create(
            usuario=self.user_op, organizacao=self.org_a, papel="operador"
        )

        self.user_b = User.objects.create_user(username="admin_b", password="123")
        self.perfil_b = Perfil.objects.create(
            usuario=self.user_b, organizacao=self.org_b, papel="admin"
        )

        self.user_vazio = User.objects.create_user(username="admin_vazio", password="123")
        self.perfil_vazio = Perfil.objects.create(
            usuario=self.user_vazio, organizacao=self.org_vazia, papel="admin"
        )

        self.cat_a = Categoria.objects.create(nome="Geral", organizacao=self.org_a)

        self.posts_a = []
        for i in range(3):
            p = Post.objects.create(
                titulo=f"Post A {i}",
                conteudo="Conteúdo de teste com mais de cinquenta caracteres para validação.",
                autor=self.perfil_a,
                categoria=self.cat_a,
                organizacao=self.org_a,
                status="publicado" if i < 2 else "rascunho",
            )
            self.posts_a.append(p)

        Comentario.objects.create(post=self.posts_a[0], autor="Leitor 1", texto="Muito bom!")
        Comentario.objects.create(post=self.posts_a[1], autor="Leitor 2", texto="Excelente!")

        for i in range(5):
            p = Post.objects.create(
                titulo=f"Post B {i}",
                conteudo="Conteúdo de teste da organização B com mais de cinquenta caracteres.",
                autor=self.perfil_b,
                organizacao=self.org_b,
                status="publicado",
            )
            if i < 4:
                Comentario.objects.create(post=p, autor="Leitor B", texto="Comentário B")

    def test_total_da_organizacao(self):
        self.client.force_login(self.user_a)
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["kpis"]["total"], 3)
        self.assertEqual(r.context["kpis"]["publicados"], 2)
        self.assertEqual(r.context["kpis"]["rascunhos"], 1)
        self.assertEqual(r.context["kpis"]["comentarios"], 2)

    def test_filtro_por_periodo_e_data_invalida(self):
        tz = timezone.get_current_timezone()
        Post.objects.filter(pk=self.posts_a[0].pk).update(
            criado_em=timezone.make_aware(datetime(2026, 1, 15, 12, 0), tz)
        )
        Post.objects.filter(pk=self.posts_a[1].pk).update(
            criado_em=timezone.make_aware(datetime(2026, 3, 10, 12, 0), tz)
        )
        Post.objects.filter(pk=self.posts_a[2].pk).update(
            criado_em=timezone.make_aware(datetime(2026, 5, 20, 12, 0), tz)
        )

        self.client.force_login(self.user_a)

        r = self.client.get(reverse("dashboard"), {"inicio": "2026-03-01", "fim": "2026-03-31"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["kpis"]["total"], 1)

        r_invalido = self.client.get(reverse("dashboard"), {"inicio": "abc"})
        self.assertEqual(r_invalido.status_code, 200)
        self.assertEqual(r_invalido.context["kpis"]["total"], 3)

    def test_dashboard_vazio_sem_erro(self):
        self.client.force_login(self.user_vazio)
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["kpis"]["total"], 0)
        self.assertEqual(r.context["kpis"]["comentarios"], 0)

    def test_permissao_exportacao_e_series_por_papel(self):
        self.client.force_login(self.user_op)
        r_dash = self.client.get(reverse("dashboard"))
        self.assertEqual(r_dash.status_code, 200)
        self.assertFalse(r_dash.context["mostra_series"])

        r_csv_op = self.client.get(reverse("exportar_csv"))
        self.assertEqual(r_csv_op.status_code, 403)

        self.client.force_login(self.user_a)
        r_csv_admin = self.client.get(reverse("exportar_csv"))
        self.assertEqual(r_csv_admin.status_code, 200)
        self.assertIn("text/csv", r_csv_admin["Content-Type"])

    def test_sem_n_mais_1_com_select_related(self):
        with self.assertNumQueries(1):
            qs = Post.objects.filter(organizacao=self.org_a).select_related(
                "autor__usuario", "categoria"
            )
            for p in qs:
                _ = p.autor.usuario.username
                _ = p.categoria.nome
