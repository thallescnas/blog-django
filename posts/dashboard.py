from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from .models import Comentario


def calcular_metricas(base):
    kpis = base.aggregate(
        total=Count("id"),
        autores=Count("autor", distinct=True),
        publicados=Count("id", filter=Q(status="publicado")),
        rascunhos=Count("id", filter=Q(status="rascunho")),
    )
    kpis["comentarios"] = Comentario.objects.filter(post__in=base).aggregate(
        total=Count("id")
    )["total"]
    ranking = (
        base.values("autor__usuario__username")
        .annotate(total=Count("id")).order_by("-total")[:5]
    )
    por_mes_qs = (
        base.annotate(mes=TruncMonth("criado_em")).values("mes").annotate(total=Count("id")).order_by("mes")
    )
    por_mes = [
        {"mes": r["mes"].strftime("%m/%Y"), "total": r["total"]}
        for r in por_mes_qs if r["mes"]
    ]
    por_status = (
        base.values("status").annotate(total=Count("id")).order_by("-total")
    )

    return {
        "kpis": kpis,
        "ranking": ranking,
        "por_mes": por_mes,
        "por_status": por_status
    }