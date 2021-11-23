from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20211116_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/', verbose_name='Изображение'),
        ),
    ]
