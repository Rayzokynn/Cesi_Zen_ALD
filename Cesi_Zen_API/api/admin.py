from django.contrib import admin
from .models import ArticleInfo, Categorie, ArticleLu, Utilisateur

@admin.register(ArticleInfo)
class ArticleInfoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_publi')
    list_filter = ('categorie', 'date_publi')
    search_fields = ('titre', 'contenu')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(ArticleLu)
class ArticleLuAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'article', 'date_lecture')
    list_filter = ('date_lecture',)

admin.site.register(Utilisateur)