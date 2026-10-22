# InsightPulse AI - Customer Feedback Analytics Platform

A complete, functional AI-powered customer feedback analytics platform built for an AWS college project. Features sentiment analysis, complaint categorization, priority detection, and interactive dashboards.

## Technology Stack

### Backend
- **Python + FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation using Python type annotations
- **SQLAlchemy + SQLite** - Database ORM and local storage
- **Hugging Face Transformers** - Pretrained sentiment analysis model
- **Pandas** - Data processing
- **Boto3** - AWS SDK (for future cloud deployment)

### Frontend
- **React + TypeScript + Vite** - Modern React build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Interactive charting library
- **Lucide React** - Beautiful icon library
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Cloud Services (Optional - for deployment)
- **Amazon S3** - File storage
- **Amazon DynamoDB** - NoSQL database
- **AWS Lambda** - Serverless processing
- **Amazon CloudWatch** - Logging and monitoring

## Features

- **Overview Dashboard** - KPI cards, sentiment distribution, trends over time, category breakdown
- **Feedback Explorer** - Search, filter, paginate, and export customer reviews
- **AI Insights** - Executive summaries, theme extraction, improvement suggestions
- **Import Feedback** - Drag-and-drop CSV upload with validation and preview
- **Settings** - Dataset management, system status, AWS integration status
- **Genuine AI** - Hugging Face sentiment model with rule-based fallback
- **Local-First** - Works without AWS credentials using SQLite

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

## Installation & Setup (Windows PowerShell)

### 1. Clone or Navigate to Project

```powershell
cd "d:\sem-4\sem-5\aws project"
```

### 2. Backend Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install
```

### 4. Environment Configuration

```powershell
# Copy example environment file (from project root)
Copy-Item .env.example .env

# Edit .env to configure settings (optional for local development)
# Default settings work for local development
```

## Running the Application

### Start Backend (PowerShell)

```powershell
# From project root
cd "d:\sem-4\sem-5\aws project"

# Activate virtual environment
.\venv\Scripts\Activate

# Start FastAPI server
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start Frontend (New PowerShell Terminal)

```powershell
# From project root
cd "d:\sem-4\sem-5\aws project\frontend"

# Start Vite dev server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Quick Start Guide

1. **Start both servers** (backend on port 8000, frontend on port 5173)
2. **Open browser** to `http://localhost:5173`
3. **Go to Import Feedback** page
4. **Upload the sample CSV** (`sample_feedback.csv`) or download a sample from the import page
5. **Click "Start AI Analysis"** after upload
6. **View results** in Overview Dashboard, Feedback Explorer, and AI Insights pages

## CSV Format

Required column:
- `review_text` - The customer feedback text

Optional columns:
- `date` - Date of the feedback (YYYY-MM-DD format)
- `product` - Product name
- `rating` - Rating from 1-5

Example:
```csv
review_text,date,product,rating
"Great product!",2024-01-15,Product A,5
"Terrible service",2024-01-16,Product B,1
```

## Project Structure

```
aws project/
├── backend/
│   ├── app/
│   │   ├── ai/              # AI processing (sentiment, categorization, priority)
│   │   ├── api/
│   │   │   └── routes/      # API endpoints
│   │   ├── schemas/         # Pydantic models
│   │   ├── services/        # Business logic
│   │   ├── storage/         # Storage adapters (local, AWS)
│   │   ├── config.py        # Configuration
│   │   └── main.py          # FastAPI application
│   ├── tests/               # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── layouts/         # Layout components
│   │   ├── lib/             # Utilities and API client
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx          # Main app with routing
│   │   └── main.tsx         # Entry point
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── sample_feedback.csv      # Sample data for testing
├── .env.example             # Environment variables template
├── .gitignore
└── README.md
```

## Running Tests

### Backend Tests

```powershell
# Activate virtual environment
.\venv\Scripts\Activate

# Install pytest (if not already installed)
pip install pytest

# Run tests from project root
cd backend
pytest tests/
```

## AI Features

### Sentiment Analysis
- Uses Hugging Face Transformers model (`cardiffnlp/twitter-roberta-base-sentiment-latest`)
- Classifies feedback as positive, neutral, or negative
- Provides confidence scores
- Falls back to rule-based analysis if model unavailable

### Complaint Categorization
- Categories: Delivery, Customer Support, Payment, Product Quality, Pricing, App/Usability, Other
- Keyword-based classification (can be extended with LLM)

### Priority Detection
- High priority: Negative sentiment with high confidence + urgent keywords
- Medium priority: Negative sentiment or complaint keywords
- Low priority: Neutral or positive feedback

## AWS Integration (Optional)

To enable AWS cloud storage:

1. Configure environment variables in `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket-name
AWS_DYNAMODB_TABLE=your-table-name
AWS_LAMBDA_FUNCTION=your-function-name
STORAGE_MODE=aws
```

2. Provision AWS resources (S3 bucket, DynamoDB table, Lambda function)
3. Ensure IAM permissions are configured correctly

**Note:** AWS integration is prepared but not required for local development.

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/datasets` - List all datasets
- `POST /api/datasets` - Create dataset
- `GET /api/datasets/{id}` - Get dataset details
- `DELETE /api/datasets/{id}` - Delete dataset
- `POST /api/feedback/upload` - Upload CSV file
- `POST /api/feedback/{id}/analyze` - Analyze feedback
- `GET /api/feedback` - List feedback with filters
- `GET /api/feedback/export` - Export feedback as CSV
- `GET /api/analytics/overview` - Get overview analytics
- `GET /api/analytics/trends` - Get trend data
- `GET /api/analytics/categories` - Get category breakdown
- `GET /api/insights` - Get AI insights

## Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

### Frontend won't start
- Ensure Node.js is installed: `node --version`
- Install dependencies: `npm install`
- Verify port 5173 is not in use

### AI model fails to load
- The application will automatically fall back to rule-based sentiment analysis
- Check internet connection (model download requires internet)
- Check logs for specific error messages

### CORS errors
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/app/main.py`
- Verify frontend proxy settings in `frontend/vite.config.ts`

## Development Notes

- The application uses SQLite for local development (no database setup required)
- Database file (`insightpulse.db`) is created automatically in the backend directory
- All data persists across application restarts
- TypeScript errors in IDE are expected until `npm install` is run
- The AI model is downloaded on first use (~500MB)

## Future Enhancements

- [ ] LLM-based insights generation (OpenAI/Anthropic API integration)
- [ ] Real-time WebSocket updates
- [ ] Multi-dataset comparison
- [ ] Advanced filtering and saved queries
- [ ] Email alerts for high-priority feedback
- [ ] Full AWS deployment with CloudFormation/Terraform
- [ ] User authentication and authorization
- [ ] Team collaboration features

## License

This project was built for educational purposes for an AWS college subject.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `http://localhost:8000/docs`
3. Check backend logs for error messages
