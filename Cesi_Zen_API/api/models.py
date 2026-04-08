# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Admin(models.Model):
    login = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=150)
    password_admin = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'admin'


class ArticleInfo(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_publi = models.DateTimeField(blank=True, null=True)
    imageUrl = models.CharField(max_length=500, blank=True, null=True) 
    
    categorie = models.ForeignKey('Categorie', models.DO_NOTHING)
    admin = models.ForeignKey(Admin, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'article_info'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categorie'


class ConfigRespi(models.Model):
    nom = models.CharField(max_length=50)
    duree_inspi = models.IntegerField()
    duree_apnee = models.IntegerField()
    duree_expi = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'config_respi'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class JournalEmotion(models.Model):
    date_heure = models.DateTimeField(blank=True, null=True)
    emotion_niv1 = models.CharField(max_length=50)
    emotion_niv2 = models.CharField(max_length=50)
    commentaire = models.TextField(blank=True, null=True)
    utilisateur = models.ForeignKey('Utilisateur', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_emotion'


class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    pseudo = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    date_inscription = models.DateTimeField(blank=True, null=True)
    date_connexion = models.DateTimeField(blank=True, null=True)

    @property
    def is_authenticated(self):
        return True
    
    class Meta:
        managed = False
        db_table = 'utilisateur'

class SessionRespiration(models.Model):
    # Lien vers le modèle User standard de Django (utilisé par ton JWT)
    user = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='utilisateur_id')
    technique_name = models.CharField(max_length=100)
    cycles_completed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True  # Autorise Django à créer cette table
        db_table = 'session_respiration'

class ArticleLu(models.Model):
    id = models.AutoField(primary_key=True) 
    utilisateur = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='utilisateur_id')
    article = models.ForeignKey('ArticleInfo', models.DO_NOTHING, db_column='article_id')
    date_lecture = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'article_lu'
        unique_together = (('utilisateur', 'article'),)