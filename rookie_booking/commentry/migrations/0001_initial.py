# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments', '0002_update_user_email_field_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MPTTComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_comments.Comment')),
                ('upvotes', models.IntegerField(default=0, verbose_name=b'Upvotes')),
                ('downvotes', models.IntegerField(default=0, verbose_name=b'Downvotes')),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='commentry.MPTTComment', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
            },
            bases=('django_comments.comment', models.Model),
        ),
        migrations.AddField(
            model_name='commentvote',
            name='post',
            field=models.ForeignKey(related_name='user_votes', to='commentry.MPTTComment'),
        ),
    ]
