from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from .models import Post

def metricas_kpis(org):
    base = Post.objects.filter(organizacao=org)

    kpis = base.aggregate(
        total=Count("id"),
        autores=Count("autor", distinct=True),
        publicados=Count("id", filter=Q(status="publicado")),
        rascunhos=Count("id", filter=Q(status="rascunho"))
    )

    return kpis

def metricas_ranking(org):
    base = Post.objects.filter(organizacao=org)

    ranking = (
        base.values("autor__usuario__username").annotate(total=Count("id")).order_by("-total")[:5]
    )

    return ranking

def metricas_por_mes(org):
    base = Post.objects.filter(organizacao=org)

    por_mes = (
        base.annotate(mes=TruncMonth("criado_em")).values("mes").annotate(total=Count("id")).order_by("mes")
    )

    return por_mes

def metricas_por_status(org):
    base = Post.objects.filter(organizacao=org)

    por_status = (
        base.values("status").annotate(total=Count("id")).order_by("-total")
    )

    return por_status