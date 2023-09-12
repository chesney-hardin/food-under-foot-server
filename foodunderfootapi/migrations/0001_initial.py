# Generated by Django 4.2.5 on 2023-09-10 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EdiblePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harvest_start', models.CharField(max_length=2)),
                ('harvest_end', models.CharField(max_length=2)),
                ('image', models.CharField(max_length=299)),
            ],
        ),
        migrations.CreateModel(
            name='PlantPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='Usability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=99)),
                ('icon', models.CharField(max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='WildPlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=99)),
                ('latin_name', models.CharField(max_length=99)),
                ('alternate_names', models.CharField(max_length=299, null=True)),
                ('latin_family', models.CharField(max_length=99)),
                ('description', models.CharField(max_length=999)),
                ('image', models.CharField(max_length=299)),
                ('link_to_usda', models.CharField(max_length=299, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('edible_parts', models.ManyToManyField(related_name='plants_with_edible_part', through='foodunderfootapi.EdiblePart', to='foodunderfootapi.plantpart')),
            ],
        ),
        migrations.CreateModel(
            name='TipsAndRecipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=199)),
                ('description', models.CharField(max_length=999)),
                ('image', models.CharField(max_length=299)),
                ('isRecipe', models.BooleanField(default=False)),
                ('isApproved', models.BooleanField(default=False)),
                ('edible_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodunderfootapi.ediblepart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HarvestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('isPublicLocation', models.BooleanField(default=False)),
                ('quantity', models.CharField(max_length=199)),
                ('title', models.CharField(max_length=199)),
                ('description', models.CharField(max_length=999)),
                ('image', models.CharField(max_length=299)),
                ('isPublic', models.BooleanField(default=False)),
                ('plant_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodunderfootapi.plantpart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wild_plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='harvest_logs', to='foodunderfootapi.wildplant')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wild_plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='foodunderfootapi.wildplant')),
            ],
        ),
        migrations.AddField(
            model_name='ediblepart',
            name='plant_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodunderfootapi.plantpart'),
        ),
        migrations.AddField(
            model_name='ediblepart',
            name='usability',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='foodunderfootapi.usability'),
        ),
        migrations.AddField(
            model_name='ediblepart',
            name='wild_plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodunderfootapi.wildplant'),
        ),
    ]
