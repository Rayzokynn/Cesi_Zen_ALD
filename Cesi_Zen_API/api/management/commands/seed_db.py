from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from api.models import Utilisateur, Categorie, ArticleInfo, SessionRespiration, ArticleLu, ConfigRespi

class Command(BaseCommand):
    help = "Initialise et peuple la base de données locale avec des données de démonstration de développement"

    def handle(self, *args, **options):
        # Sécurité : Éviter d'écraser des données de production existantes
        if Utilisateur.objects.exists() or ArticleInfo.objects.exists():
            self.stdout.write(self.style.WARNING("La base de données contient déjà des données (Utilisateurs ou Articles)."))
            self.stdout.write(self.style.WARNING("Pour éviter toute perte accidentelle, l'initialisation a été annulée."))
            return

        self.stdout.write("Initialisation des données de développement...")

        # 1. Nettoyer les données existantes
        self.stdout.write("Nettoyage des anciennes données...")
        ArticleLu.objects.all().delete()
        ConfigRespi.objects.all().delete()
        SessionRespiration.objects.all().delete()
        ArticleInfo.objects.all().delete()
        Categorie.objects.all().delete()
        Utilisateur.objects.all().delete()

        # 2. Créer les utilisateurs
        self.stdout.write("Création de 2 utilisateurs...")
        u1 = Utilisateur.objects.create(
            pseudo="alexis",
            email="alexis@cesizen.fr",
            password=make_password("Password123!"),
            date_inscription=timezone.now()
        )
        u2 = Utilisateur.objects.create(
            pseudo="mentalhealth",
            email="contact@cesizen.fr",
            password=make_password("Password123!"),
            date_inscription=timezone.now()
        )
        self.stdout.write(self.style.SUCCESS(f"Utilisateurs créés : {u1.pseudo}, {u2.pseudo}"))

        # 3. Créer une catégorie
        cat = Categorie.objects.create(nom="Santé Mentale")
        self.stdout.write(self.style.SUCCESS(f"Catégorie créée : {cat.nom}"))

        # 4. Créer 5 articles
        self.stdout.write("Création de 5 articles...")
        articles_data = [
            ("Comprendre l'anxiété au quotidien", "L'anxiété est une réaction naturelle du corps face au stress. Apprendre à l'identifier et à l'accueillir est le premier pas pour mieux la gérer au jour le jour.", "https://images.unsplash.com/photo-1474447976065-67d23accb173"),
            ("La respiration carrée pour se recentrer", "La respiration carrée est une technique d'apaisement immédiat. Elle consiste à inspirer, retenir son souffle, expirer et retenir à vide pendant des durées égales.", "https://images.unsplash.com/photo-1506126613408-eca07ce68773"),
            ("L'importance du sommeil sur le moral", "Un sommeil réparateur est le pilier d'une bonne santé mentale. Établir une routine de coucher calme permet de réguler l'humeur et d'améliorer la concentration.", "https://images.unsplash.com/photo-1511295742364-92767fc4a085"),
            ("5 minutes de méditation pour débutants", "Prendre seulement 5 minutes par jour pour se concentrer sur sa respiration et observer ses pensées sans jugement aide à réduire le niveau global de stress.", "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b"),
            ("Apprendre à fixer des limites saines", "Savoir dire non sans culpabiliser est un acte d'amour propre essentiel. Cela préserve votre énergie mentale et renforce la qualité de vos relations.", "https://images.unsplash.com/photo-1516302720888-aa927e3248bb")
        ]

        for titre, contenu, img in articles_data:
            art = ArticleInfo.objects.create(
                titre=titre,
                contenu=contenu,
                imageUrl=img,
                categorie=cat,
                date_publi=timezone.now()
            )
            self.stdout.write(f"  Article créé : {art.titre}")

        # 5. Créer 3 exercices de respiration pour l'utilisateur alexis
        self.stdout.write("Création de 3 sessions de respiration pour alexis...")
        s1 = SessionRespiration.objects.create(
            user=u1,
            technique_name="Relaxant",
            cycles_completed=4
        )
        s2 = SessionRespiration.objects.create(
            user=u1,
            technique_name="Équilibrant",
            cycles_completed=6
        )
        s3 = SessionRespiration.objects.create(
            user=u1,
            technique_name="Apaisant",
            cycles_completed=3
        )
        self.stdout.write(self.style.SUCCESS(f"Sessions créées pour {u1.pseudo} : {s1.technique_name}, {s2.technique_name}, {s3.technique_name}"))

        self.stdout.write(self.style.SUCCESS("Base de données initialisée avec succès !"))
