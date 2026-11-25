import django.db.models.deletion
from django.db import migrations, models


def preencher_org_categoria_tag(apps, schema_editor):
    Org = apps.get_model('core', 'Organizacao')
    Categoria = apps.get_model('posts', 'Categoria')
    Tag = apps.get_model('posts', 'Tag')
    org, _ = Org.objects.get_or_create(nome='Organização padrão')
    Categoria.objects.filter(organizacao__isnull=True).update(organizacao=org)
    Tag.objects.filter(organizacao__isnull=True).update(organizacao=org)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('posts', '0004_alter_post_organizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='organizacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.organizacao'),
        ),
        migrations.AddField(
            model_name='tag',
            name='organizacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.organizacao'),
        ),
        migrations.RunPython(preencher_org_categoria_tag, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='categoria',
            name='organizacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.organizacao'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='organizacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.organizacao'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['organizacao', 'criado_em'], name='posts_post_org_criado_idx'),
        ),
    ]
