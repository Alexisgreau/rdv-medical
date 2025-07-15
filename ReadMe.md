# RDV Medical

## Table des matières

1. [Présentation du projet](#présentation-du-projet)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Démarrage de l'application](#démarrage-de-lapplication)
6. [Structure du projet](#structure-du-projet)
7. [Endpoints API](#endpoints-api)
8. [Diagramme de la base de données](#diagramme-de-la-base-de-données)
9. [Contribuer](#contribuer)

---

## Présentation du projet

**RDV Medical** est une application Django permettant aux patients de réserver, modifier et annuler leurs rendez‑vous médicaux, et aux médecins de gérer leurs créneaux et rédiger des notes médicales.

Fonctionnalités principales :

* Authentification (patient, médecin, admin)
* Inscription et édition de profil
* CRUD rendez‑vous via une API REST (DRF)
* Widgets dynamiques pour choix de créneaux (slots)
* Dashboard patient (prise, modif, annulation de RDV)
* Dashboard médecin (liste, détail, confirmation, notes)
* Tests unitaires et d’intégration

---

## Prérequis

* Python 3.11+
* pip / virtualenv
* Git

Optionnel pour le front : un navigateur moderne supportant `fetch()` et `<input type="datetime-local">`.

---

## Installation

1. **Cloner le dépôt** :

   ```bash
   git clone https://github.com/ton‑utilisateur/rdv‑medical.git
   cd rdv‑medical
   ```

2. **Créer et activer un environnement virtuel** :

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Fichier d'environnement** : duplique `env.sample` en `.env` et renseigne :

   ```ini
   SECRET_KEY=ta_clé_secrète_django
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   TIME_ZONE=Europe/Paris
   ```

2. **Variables Django** sont chargées via `django-environ` (voire `python-dotenv`).

3. **Base de données** : par défaut `sqlite3`. Pour PostgreSQL, modifie `DATABASE_URL` et installe `psycopg2`.

---

## Démarrage de l'application

1. **Appliquer les migrations** :

   ```bash
   python manage.py migrate
   ```

2. **Créer un super‑utilisateur** :

   ```bash
   python manage.py createsuperuser
   ```

3. **Lancer le serveur de développement** :

   ```bash
   python manage.py runserver
   ```

4. **Accéder à l'interface** :

   * Dashboard patient : `http://127.0.0.1:8000/dashboard/patient/`
   * Dashboard médecin : `http://127.0.0.1:8000/dashboard/medecin/`
   * Admin Django : `http://127.0.0.1:8000/admin/`

---

## Structure du projet

```
rdv_medical/
├── app/                # application principale
│   ├── migrations/
│   ├── templates/      # templates HTML (registration, dashboard,...)
│   ├── models.py       # User, Appointment, MedicalNote
│   ├── views.py        # vues classiques & DRF ViewSets
│   ├── serializers.py  # DRF serializers
│   ├── permissions.py  # permissions DRF
│   ├── urls.py         # routes signup, dashboards, API
│   └── tests/          # tests unitaires et d'intégration
├── rdv_medical/        # configuration Django
│   ├── settings.py
│   └── urls.py
├── manage.py           # script de gestion
├── requirements.txt    # dépendances Python
└── README.md           # documentation (ce fichier)
```

---

## Endpoints API

* **Liste/CRUD RDV** :

  * `GET  /api/appointments/`        → liste des RDV (patient ou médecin)
  * `POST /api/appointments/`        → création (patient uniquement)
  * `GET  /api/appointments/{id}/`   → détail RDV
  * `PATCH/ DELETE /api/appointments/{id}/` → modifier (statut ou date) / annuler
* **Confirmation** (médecin) :

  * `POST /api/appointments/{id}/confirm/`
* **Créneaux libres** :

  * `GET  /api/appointments/available-slots/?doctor=<id>&date=YYYY-MM-DD`
    → retourne listes de JSON ISO des slots libres de 09:00 à 17:00 (pas d’overlap)

---

## Diagramme de la base de données

* **User** (`AUTH_USER_MODEL`)

  * `username`, `email`, `role`, `phone`, ...
* **Appointment**

  * `patient` (FK → User)
  * `doctor` (FK → User)
  * `scheduled_time`, `status`
* **MedicalNote**

  * `appointment` (OneToOne → Appointment)
  * `content`

(Diagramme visuel à générer avec `django-extensions` ou outil externe.)

---

## Contribuer

1. Forker le projet
2. Créer une branche feature : `git checkout -b feat/ma-fonctionnalité`
3. Commit & push
4. Ouvrir une Pull Request

Merci de respecter les guidelines de code (PEP8, tests).
