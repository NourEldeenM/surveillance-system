# Fawry Surveillance System

A **FastAPI**-based full-stack interface for real-time multi-object tracking and face recognition in retail surveillance video streams. Comes with:

- 🎥 **Integration Page**: run tracking + face recognition in one go
- 🧑‍💻 **Face Recognition**: upload a staff image, identify the person
- 🚶‍♂️ **Object Tracking**: upload a video, get an annotated tracking output
- 💾 **Persistence**: PostgreSQL
- ⚙️ **Modular Services & Routers** for easy extension

---

## 🚀 Quick Start

1. **Clone** & enter the repo
   ```bash
   git clone https://github.com/your-org/surveillance-system.git
   cd surveillance-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .\.venv\Scripts\activate       # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   Copy `.env.example` → `.env` and fill in:
   ```ini
   DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
   SECRET_KEY=your_jwt_secret
   HASH_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   TRACKING_MODEL_PATH=/path/to/your/trackingModel.pt
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```
   Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🗂️ Project Structure

```bash
surveillance-system/
├── app/
│   ├── main.py              # FastAPI app + routes & static mounts
│   ├── core/                # Config, database, security
│   ├── models/              # SQLAlchemy models (User, Branch, Region…)
│   ├── schemas/             # Pydantic schemas for requests/responses
│   ├── services/            # Business logic: tracking, face, integration
│   ├── routers/             # API routers: auth, users, face, tracking, integration
│   ├── templates/           # Jinja2 HTML pages (index, face, tracking, results)
│   └── static/              # Front-end assets
│       ├── css/style.css
│       ├── js/
│       │   ├── main.js      # integration page logic
│       │   ├── face.js      # face-recognition page logic
│       │   ├── tracking.js  # object-tracking page logic
│       │   └── results.js   # shared results-page logic
│       ├── images/          # logos, icons
│       └── outputs/         # auto-served annotated videos
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 Features & Endpoints

### 1. Integration (Tracking + Face)
- **UI**: `GET  /`
- **Process**: `POST /models/integration/video`
- **Results**: redirects to `/results`, shows annotated video & combined detections

---

### 2. Face Recognition
- **UI**: `GET  /face`
- **API**: `POST /models/face/recognize`
  - **Input**: form-file `file` (image)
  - **Output**: `{ "person": "<matched_name>" }`

---

### 3. Object Tracking
- **UI**: `GET  /tracking`
- **API**: `POST /models/tracking/video`
  - **Input**: form-file `file` (video)
  - **Output**:
    ```json
    {
      "annotated_video": "/static/outputs/xyz_annotated.mp4",
      "predictions": "tracker_results/data/xyz.txt"
    }
    ```

---

## 🔧 Front-End Pages

1. **Home / Integration**
   - Drag-and-drop or click to select a video
   - Yellow highlight on selection
   - Preview results & download annotated video

2. **Face Recognition**
   - Upload an image
   - Displays name of matched staff member

3. **Object Tracking**
   - Upload a raw video
   - Embeds the annotated tracking video

All pages share a **professional, responsive design** with the Fawry brand colors (yellow & blue) and logo.

