from django.db import models

class Reviews(models.Model):
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
        
class ProductsTable(models.Model):
    product_id = models.BigIntegerField(blank=True, primary_key=True)
    product_rating = models.TextField(blank=True, null=True)
    review_count = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    category1 = models.TextField(blank=True, null=True)
    category2 = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        app_label = 'default'
        db_table = 'products_review_visualization'

class New_Review(models.Model):
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

class LoginRecommend(models.Model):
    review_id = models.BigIntegerField(blank=True, primary_key=True)
    userid = models.TextField(blank=True, null=True)
    ratings = models.TextField(blank=True, null=True)
    category1 = models.TextField(blank=True, null=True)
    category2 = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    product_url = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        app_label = 'default'
        db_table = 'login_recommend'
class NoLoginRecommend(models.Model):
    product_id = models.BigIntegerField(blank=True, primary_key=True)
    product_rating = models.TextField(blank=True, null=True)
    review_count = models.TextField(blank=True, null=True)
    category1 = models.TextField(blank=True, null=True)
    category2 = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    product_url = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        app_label = 'default'
        db_table = 'no_login_recommend'
        
