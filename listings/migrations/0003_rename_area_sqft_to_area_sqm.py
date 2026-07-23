from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_property_owner_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='area_sqft',
            new_name='area_sqm',
        ),
        migrations.AlterField(
            model_name='property',
            name='area_sqm',
            field=models.PositiveIntegerField(help_text='Living area in square meters'),
        ),
    ]
