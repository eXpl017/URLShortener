# URL Shortener

A minimal, fast, and extensible URL shortener built with FastAPI and MariaDB. Converts long URLs into compact, short links.
***
## Features

- Generate unique 5-character short URLs for long links
- Redirect short URLs to their original destinations
- View info for any short URL (ShortURL, OriginalURL, Creation Date)
- Simple API for integration
- Database trigger enforces strict short code length
- Robust error handling
***
## Technology Stack

- **FastAPI:** Python API framework built for async and modern web APIs
- **Uvicorn:** Lightning-fast ASGI web server powering FastAPI (run directly from Python)
- **MariaDB/MySQL:** Robust, scalable relational database
- **ASGI:** Used and learned Asynchronous Server Gateway Interface concepts to enable non-blocking, high-performance web serving
***
## Setup

1. **Clone the repo:**  
```bash
git clone https://github.com/eXpl017/URLShortener.git
cd URLShortener
```

2. **Create and activate your Python environment:**  
```bash
# venv
python3 -m venv venv
source venv/bin/activate

# virtualenv
virtualenv .venv
source .venv/bin/activate
```

3. **Install dependencies:**  
```bash
pip install -r requirements.txt
```

4. **Configure the database:**  
- Create a MariaDB database and user.
- Add your DB `username` and `password` to `db_config.py`

5. **Start the API server:**  
`python main.py`

6. **Visit the web UI:**  
- Open [http://localhost:8008](http://localhost:8008) in your browser.

## API Endpoints

### 1. Generate Short URL

- **POST** `/api/v1/create/`
- **Body:** `{ "long_url": "<long-url>" }`
- **Response:** `{ "short_url": "<5-char-code>" }`

### 2. Redirect or View Info

- **GET** `/{short_url}`
    - Redirects to original url

- **GET** `/{short_url}?info=true`
    - **Response:**  
      ```
	  # example
      { 
        "short_url": "abc12",
        "long_url": "https://originalsite.com",
        "c_date": "2025-08-17 09:16:36"
      }
      ```
***
## Frontend

> Webpages for this project have been generated with the help of AI

- Minimal page with:
  - Input box for URL
  - "Generate ShortURL" button
  - Short URL shown after creation, as a link to the input URL
  - View info button
***
## Error Handling

- 5-character limit enforced by DB trigger.  
  If unable to generate a new short URL, new short links don't get added.
***
## To Do / Customization

- [ ] Add authentication, admin UI, etc.
- [ ] Give user ability to delete ShortURLs, add custom ShortURLs etc.
- [ ] Docker support

