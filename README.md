# Women in Tech & Entrepreneurship - Member Engagement Platform
# 🎯 Project Overview
Women in Tech and Entrepreneurship is a groundbreaking organization, on a mission to support the most ambitious and innovative women at every stage of their journey in technology and entrepreneurship.

This project, with the support of R. Jean Louis at ENGINUITi Solutions, serves to gamify the existing onboarding and retention processes, thereby enhancing the member experience through:

* Points-based rewards system for event attendance and engagement

* Staff dashboard with real-time analytics and notifications

* Member dashboard showing personal rewards and events

* Automated signup bonuses (20 points for new members)

# 🚀 Features
* Member Dashboard
    * Rewards earned this month / to date

    * Total events attended

    * Paginated events table with proof images

    * "Add Event" functionality

* Staff Dashboard
    * Total registered users counter

    * Registrations this month

    * Total points awarded

    * Top users table with 3 view modes:

        * This Month | This Year | All Time

    * Full pagination support

    * Real-time notifications system

# Notifications System
* Individual mark as read

* Mark all as read

* Clear all notifications (staff only)

* Staff alerting for new signups

# 📋 Quick Setup
1. Clone & Environment
```
git clone <your-repo-url>
cd wte_gamification
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. Database Setup
```
python manage.py migrate
python manage.py createsuperuser
```
4. Collect Static Files
`python manage.py collectstatic --noinput`

5. Run Server
`python manage.py runserver`

6. Visit: 
`http://localhost:8000`

Empowering women in tech through gamified engagement! 🚀✨