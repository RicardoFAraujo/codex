from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='completed_workshops',
            field=models.ManyToManyField(blank=True, related_name='completed_by_users', to='workshops.workshop'),
        ),
    ]
