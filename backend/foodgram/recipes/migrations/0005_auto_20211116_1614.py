from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20211105_1853'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ингредиент рецепта', 'verbose_name_plural': 'Ингредиенты рецепта'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredients', to='recipes.Recipe'),
        ),
    ]
