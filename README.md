# OrderAPI

# 🛒 OrderAPI – Travail de session INF349

Une API de commandes e-commerce développée en **Flask**, avec un système de file d’attente pour les paiements via **Redis** et **RQ**, et une base de données **PostgreSQL**. Un **frontend HTML simple** permet de créer, mettre à jour, payer et consulter des commandes.

## 🚀 Fonctionnalités principales

- Création de commandes avec un ou plusieurs produits
- Calcul automatique des taxes (selon la province) et des frais de livraison (selon le poids)
- Sauvegarde en base de données PostgreSQL
- Paiement asynchrone via un **worker Redis (RQ)**
- Mise en cache des commandes payées
- Interface HTML minimale pour tester les fonctionnalités

---

## 🧱 Technologies utilisées

- **Python 3.10+**
- **Flask 2.2+**
- **Peewee** (ORM)
- **PostgreSQL 15**
- **Redis** + **RQ** (tâches en arrière-plan)
- **Docker / Docker Compose**
- **HTML / JS vanilla** (frontend)

---

## ⚙️ Installation et lancement

### 1. Cloner le projet

```bash
git clone <repo-url>
cd OrderAPI
```

### 🔧 1. Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé et lancé

---

### ▶️ 2. Lancer les services

```bash
docker-compose up --build