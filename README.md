# Crowdfunding Web Application

A Django-based web application that enables users to create, manage, and support small-scale crowdfunding campaigns—particularly focused on community projects such as building mosques or other charitable initiatives.

## 🌟 Features

- 🕌 Create and browse fundraising projects
- 💸 Securely donate to active campaigns
- 📦 User registration and authentication
- 🧾 Project detail pages with donation history
- 📈 Progress tracking for each campaign
- 🧠 AI-powered chatbot integration using OpenAI API
- 🗃️ Admin dashboard for managing projects and users

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework, Django ORM
- **Frontend:** HTML, CSS, Bootstrap 
- **Database:** SQLite / PostgreSQL
- **Authentication:** Django's built-in auth system
- **Chatbot:** OpenAI API (GPT-4o-mini)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (optional but recommended)

### Installation

```bash
git clone https://github.com/your-username/crowdfunding-app.git
cd crowdfunding-app
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
![Screenshot from 2025-04-18 19-42-30](https://github.com/user-attachments/assets/ae5515c7-c264-466e-a806-2eb64ebbea3e)
