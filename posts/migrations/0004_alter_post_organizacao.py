import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('posts', '0003_dados_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='organizacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.organizacao'),
        ),
    ]
