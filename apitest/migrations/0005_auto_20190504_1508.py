# Generated by Django 2.0.3 on 2019-05-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0004_auto_20190504_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodgeunitinfo',
            name='estate',
            field=models.CharField(choices=[('valid', 'valid'), ('deleted', 'deleted')], default='valid', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='estate',
            field=models.CharField(choices=[('valid', 'valid'), ('deleted', 'deleted')], default='valid', max_length=10),
        ),
        migrations.AlterField(
            model_name='others_order',
            name='estate',
            field=models.CharField(choices=[('no', 'no'), ('yes', 'yes')], default='no', max_length=10),
        ),
    ]