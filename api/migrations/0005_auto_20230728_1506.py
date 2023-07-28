# Generated by Django 3.2.2 on 2023-07-28 09:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_elevator_next_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevator',
            name='status',
            field=models.CharField(choices=[('available', 'available'), ('busy', 'busy'), ('not_working', 'not_working')], default='available', max_length=20),
        ),
        migrations.CreateModel(
            name='ElevatorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_number', models.PositiveIntegerField(verbose_name='Floor Number')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('elevator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='api.elevator')),
            ],
        ),
    ]