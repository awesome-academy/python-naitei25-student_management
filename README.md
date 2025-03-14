# python-naitei25-student_management

Student management system

# Tạo file .env

- Xem file .env.example

# Tạo database (student_management)

python manage.py makemigrations school
python manage.py migrate
python manage.py createsuperuser

# Tạo seeder

- Nếu có dữ liệu rồi => xóa: python manage.py flush
- Tạo seeder: python manage.py seed
