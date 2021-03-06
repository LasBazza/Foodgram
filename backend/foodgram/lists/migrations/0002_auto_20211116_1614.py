from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritelist',
            name='recipes',
            field=models.ManyToManyField(related_name='in_favorite_list', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='favoritelist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipes',
            field=models.ManyToManyField(related_name='in_shopping_list', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
