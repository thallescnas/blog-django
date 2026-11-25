import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('posts', '0002_autor_alter_post_autor'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='organizacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.organizacao'),
        ),
        migrations.AlterField(
            model_name='post',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.perfil'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='posts.post'),
        ),
        migrations.DeleteModel(
            name='Autor',
        ),
    ]
