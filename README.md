# Amal - My Personal Dua Book

## Story behind this

I was thinking of making a mobile app for myself to perform daily adhkar. I will choose the adhkar based on my needs.
For example, if I want to perform a specific dhikr for a particular purpose, I will add it to the app. Similarly, if I
want to memorize a specific ayah, I will add it to the app so I can read it from time to time.

However, since I would need to rebuild the mobile app every time I add, remove, or update any item, I created a backend
using Django to manage this through an API. I use SQLite as the database because I am the sole user of the app.

## How to use it

### Setup .env

```shell
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=<key>
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
API_TOKEN=<api-token>
DJANGO_ADMIN_URL=admin
```

### Run using docker

```bash
 docker compose -f docker-compose.yml build
 docker compose -f docker-compose.yml up -d
```

## Endpoints

### Get All Ayah Groups

```http
GET /api/v1/ayah-group/
```

Returns a list of all ayah groups.

#### Response

```json
[
  {
    "id": 1,
    "title": "সাধারণ",
    "subtitle": "সব সময়ের জন্য প্রযোজ্য"
  },
  {
    "id": 2,
    "title": "সালাতের পর",
    "subtitle": "সালাত শেষে পড়ার বিভিন্ন বিষয়ের দুআ"
  }
]
```

### Get All Ayahs

```http
GET /api/v1/ayah/
```

Returns a list of all ayahs.

#### Response

```json
[
  {
    "id": 1,
    "group": 1,
    "title": "চলতে ফিরতে পড়বে",
    "position": 1,
    "arabic": "رَبِّ إِنِّي لِمَا أَنزَلْتَ إِلَيَّ مِنْ خَيْرٍ فَقِيرٌ",
    "indopak": "رَبِّ اِنِّیۡ لِمَاۤ اَنۡزَلۡتَ اِلَیَّ مِنۡ خَیۡرٍ فَقِیۡرٌ",
    "bangla": "হে আমার পালনকর্তা! আপনি আমার প্রতি যে কল্যাণ অবতীর্ণ করেছেন, আমি তারই মুখাপেক্ষী।",
    "ref": "সূরা আল-কাসাস, আয়াত ২৪",
    "audiopath": "0"
  }
]
```

It also supports backup and restore using sqlite db.

## Screenshots

<img src="https://github.com/SNNafi/amal-backend/blob/main/pictures/1.png?raw=true" width="300" height="645">
<img src="https://github.com/SNNafi/amal-backend/blob/main/pictures/2.png?raw=true" width="300" height="645">
