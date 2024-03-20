# Generated by Django 5.0.3 on 2024-03-18 21:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0010_alter_contactlocation_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinicalstudy",
            name="brief_title",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="clinicalstudy",
            name="nct_id",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="clinicalstudy",
            name="official_title",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="clinicalstudy",
            name="org_study_id",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clinicalstudy",
            name="organization_name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="clinicalstudy",
            name="status",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
