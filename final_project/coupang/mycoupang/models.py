# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ReviewsTable(models.Model):
    review_id = models.BigIntegerField(primary_key=True)
    reviewer_name = models.TextField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    review_contents = models.TextField(blank=True, null=True)
    ratings = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    category1 = models.TextField(blank=True, null=True)
    category2 = models.TextField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    class Meta:
        managed = False
        app_label = 'default'
        db_table = 'reviews_table'

class NewReview(models.Model):
    new_review_id = models.BigIntegerField(primary_key=True)
    reviewer_name = models.TextField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    review_contents = models.TextField(blank=True, null=True)
    ratings = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    category1 = models.TextField(blank=True, null=True)
    category2 = models.TextField(blank=True, null=True)
    product_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'default'
        db_table = 'new_review'