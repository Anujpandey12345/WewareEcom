# 🛍️ Django E-Commerce Platform with AI Product Recommendations

![Project Screenshot](https://github.com/Anujpandey12345/WewareEcom/blob/master/screenshot/githubIphone.png?raw=true)


---

## 📖 Overview

This is a full-featured **E-commerce platform** built with **Django**, where:
- 🧑‍💼 **Sellers** can register and add products from the frontend.  
- 🛒 **Buyers** can register, browse products, and give feedback (like/dislike).  
- 🤖 **AI Recommendation System** suggests products based on user preferences.  

---

## 🚀 Features

### 🧑‍💼 Seller Features
- Seller registration & login  
- Add new products with images  
- Manage product listings  

### 🛒 Buyer Features
- Buyer registration & login  
- Browse product catalog  
- Like 👍 or Dislike 👎 products  
- Get recommendations based on liked items  
- Add items to cart and checkout  

### 🧠 AI Recommendation
- Real-time product recommendations  
- Personalized user-based feedback system  

---

## 🧱 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django (Python) |
| Database | SQLite (default) / PostgreSQL |
| Authentication | Django Auth System |
| Machine Learning | Custom Recommendation Model |

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/django-ai-ecommerce.git
cd django-ai-ecommerce
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

---

## 📂 Project Structure

```
WAREWEECOMr/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── ecommerce_project/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── shop/             # Product management app
      ├── recommendations/        # AI recommendation engine            
├── static/                 # CSS, JS, images
└── staticfiles/              # css collect
```

---

## 🎯 Usage

### For Sellers
1. Register as a seller
2. Login to your dashboard
3. Add products with images and descriptions
4. Manage your product inventory

### For Buyers
1. Register as a buyer
2. Browse the product catalog
3. Like/dislike products to train the recommendation system
4. View personalized recommendations
5. Add products to cart and checkout

### Admin Panel
Access the Django admin at `http://127.0.0.1:8000/admin/` to manage users, products, and orders.

---

## 🤖 AI Recommendation System

The platform uses a custom recommendation algorithm that:
- Analyzes user feedback (likes/dislikes)
- Identifies patterns in user preferences
- Suggests similar products based on user behavior
- Updates recommendations in real-time

---

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Setup (PostgreSQL)
To use PostgreSQL instead of SQLite:

```bash
pip install psycopg2-binary
```

Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@Anujpandey12345](https://github.com/Anujpandey12345)
- LinkedIn: [My Profile](https://anujcom.vercel.app/)

---

## 🙏 Acknowledgments

- Django Documentation
- Python Community
- Open Source Contributors

---

## 📧 Contact

For questions or support, please contact: anuj.a87a@gmail.com

---

⭐ **If you find this project useful, please give it a star!** ⭐