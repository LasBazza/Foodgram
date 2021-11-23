from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20211118_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название тега'),
        ),
    ]
