- Project Structure:

├── backend/ # FastAPI Backend
│ ├── app/
│ │ ├── **init**.py
│ │ ├── main.py # FastAPI app, API endpoints
│ │ ├── models.py # Pydantic models for validation
│ │ ├── services/ # Business logic (retrieval, generation)
│ │ │ ├── **init**.py
│ │ │ ├── retrieval.py # Data retrieval logic (query processing)
│ │ │ └── generation.py # GPT-3 generation logic
│ │ ├── utils/ # Helper functions (e.g., environment variables, logging)
│ │ │ ├── **init**.py
│ │ │ ├── openai.py # OpenAI API interaction
│ │ │ └── database.py # Database interactions (e.g., SQLite)
│ ├── requirements.txt # Dependencies for FastAPI backend
│ ├── Dockerfile # Docker configuration for the backend
│ └── .env # Environment variables (API keys, etc.)
├── frontend/ # Next.js Frontend
│ ├── pages/
│ │ ├── api/ # API routes for Next.js
│ │ │ ├── query.js # API route to communicate with FastAPI
│ │ ├── index.js # Main page for input and results
│ ├── components/ # React components (UI elements)
│ │ ├── QueryForm.js # Form for submitting queries
│ │ ├── ResponseDisplay.js # Display generated responses
│ ├── public/ # Static assets (images, styles, etc.)
│ ├── styles/ # CSS or styled-components
│ ├── package.json # Frontend dependencies
│ ├── Dockerfile # Docker configuration for the frontend
│ └── .env # Frontend environment variables (API URLs)
├── docker-compose.yml # Docker Compose for backend and frontend
└── README.md # Project documentation
