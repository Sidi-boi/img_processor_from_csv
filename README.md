# Image Processing API

## Overview
This Django-based API processes image data from a CSV file, compresses images asynchronously, and stores them in the database. The API provides endpoints to upload CSV files, check processing status, and view compressed images from the Django Admin Panel.

## Features
- **Asynchronous image processing** using `ThreadPoolExecutor`.
- **CSV Upload API** to accept product images for processing.
- **Status API** to check processing status.
- **Webhook support** to notify external services when processing completes.
- **Compressed image storage** using `ImageField`, accessible from the Django Admin Panel.
- **Logging** for debugging and tracking.

## Technologies Used
- **Django** (Python-based web framework)
- **Django REST Framework (DRF)** (for API endpoints)
- **Pillow** (for image compression)
- **ThreadPoolExecutor** (for asynchronous image processing)
- **SQLite/PostgreSQL/MySQL** (for data storage)

## Installation & Setup

### Prerequisites
- Python 3.x
- Django installed (`pip install django`)
- Django REST Framework (`pip install djangorestframework`)
- Pillow (`pip install pillow`)

### Clone the Repository
```sh
git clone [https://github.com/your-username/img-processing-api.git](https://github.com/Sidi-boi/img_processor_from_csv.git)
cd img-processing-api
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Apply Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser
```sh
python manage.py createsuperuser
```
Follow the prompts to set up the admin user.

### Run the Server
```sh
python manage.py runserver
```
Access the API at: `http://127.0.0.1:8000/`
Access Django Admin at: `http://127.0.0.1:8000/admin/`

## API Endpoints

### **1. Upload CSV File**
**Endpoint:** `POST /upload/`

**Request:**
- `file` (CSV file containing image URLs)
- `webhook_url` (optional, to receive processing completion updates)

**Response:**
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### **2. Check Status**
**Endpoint:** `GET /status/<request_id>/`

**Response:**
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "In Process"
}
```
Possible statuses:
- `In Process`
- `Completed`
- `Failed`

## Database Schema
### **ImageProcessingRequest** (Tracks processing requests)
| Field | Type |
|--------|------|
| request_id | UUID |
| status | CharField (Pending, In Process, Completed, Failed) |
| webhook_url | URLField (optional) |

### **ProductImage** (Stores image details)
| Field | Type |
|--------|------|
| request | ForeignKey (ImageProcessingRequest) |
| serial_number | Integer |
| product_name | CharField |
| input_urls | TextField (comma-separated URLs) |
| output_image | ImageField (Compressed image stored in `/media/`) |

## How It Works
1. **User uploads CSV** via `/upload/`.
2. API **validates CSV** and **stores data** in the database.
3. **Asynchronous processing starts**: Downloads images, compresses them, and saves them.
4. User can **check status** using `/status/<request_id>/`.
5. **Compressed images are stored** and accessible in Django Admin.
6. (Optional) **Webhook is triggered** upon completion.

## Viewing Compressed Images in Admin
1. Run the server: `python manage.py runserver`
2. Go to Django Admin: `http://127.0.0.1:8000/admin/`
3. Navigate to **Product Images**.
4. View **compressed images as thumbnails**.

## Logging & Debugging
- Logs are printed to the console.
- Errors and processing steps are logged using `logging`.

## Reset Database (Optional)
If you need to clear all data, use:
```sh
python manage.py flush --noinput
```
Or for SQLite:
```sh
rm db.sqlite3 && python manage.py migrate
```

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

## Contact
For questions or issues, contact [your-email@example.com].

