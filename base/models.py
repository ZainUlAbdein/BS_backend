# from django.db import models
# from django.dispatch import receiver

# # class SearchResult(models.Model):
# #     query = models.CharField(max_length=255)
# #     result = models.JSONField()
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return self.query




# # # class PDFDocument(models.Model):
# # #     title = models.CharField(max_length=100)
# # #     author = models.CharField(max_length=100)
# # #     category = models.CharField(max_length=100)
# # #     cover_image = models.ImageField(upload_to='covers/')
# # #     pdf_file = models.FileField(upload_to='pdfs/')

# # #     def __str__(self):
# # #         return self.title
    



# # # class Book(models.Model):
# # #     title = models.CharField(max_length=100)
# # #     author = models.CharField(max_length=100)
# # #     category = models.CharField(max_length=100)
# # #     cover_image = models.ImageField(upload_to='covers/')
# # #     pdf_file = models.FileField(upload_to='pdfs/')

# # #     def __str__(self):
# # #         return self.title

# # from django.db import models
# # from django.contrib.auth.models import User

# # class Book(models.Model):
# #     title = models.CharField(max_length=100)
# #     author = models.CharField(max_length=100)
# #     category = models.CharField(max_length=100)
# #     cover_image = models.ImageField(upload_to='covers/')
# #     pdf_file = models.FileField(upload_to='pdfs/')
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line to associate the book with a user

# #     def __str__(self):
# #         return self.title

# # from django.db import models
# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from rest_framework.authtoken.models import Token
# # from django.conf import settings

# # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# # def create_auth_token(sender, instance=None, created=False, **kwargs):
# #     if created:
# #         Token.objects.create(user=instance)



