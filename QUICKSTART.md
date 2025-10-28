# Quick Start Guide

## Immediate Next Steps

### 1. Update Node.js (REQUIRED)

Your current Node.js version (v20.0.0) is too old. You need:
- **Minimum**: Node.js 20.19.0
- **Recommended**: Node.js 22.12.0 or later

**Install latest Node.js:**
- Download from https://nodejs.org/
- Or use nvm: `nvm install 22 && nvm use 22`

### 2. Install Dependencies

**Option A: Docker (Easiest)**
```bash
# Just run this - no manual dependency installation needed!
docker-compose up --build
```

**Option B: Local Development**

Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend (after updating Node.js):
```bash
cd frontend
npm install
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Using the Application

1. **Allow camera access** when prompted by browser
2. **Click "Detect Cards"** to analyze current frame
3. **Watch the count update** in real-time via SSE
4. **Click "Reset Count"** to start over

## Important Notes

### Current Model Status

The app uses a **generic YOLOv8n model** as a placeholder. It will detect objects but NOT playing cards specifically.

**To detect actual cards, you need to:**
1. Train a custom model on playing card dataset (see README.md)
2. Place trained model (`your_model.pt`) in `backend/` folder
3. Update `backend/.env`: `MODEL_PATH=your_model.pt`

### Development Tips

**Auto-generate route tree:**
```bash
cd frontend
npm run dev  # Generates routeTree.gen.ts automatically
```

**View API documentation:**
- Visit http://localhost:8000/docs for interactive Swagger UI
- Or http://localhost:8000/redoc for ReDoc

**Check backend logs:**
```bash
docker logs card-detection-backend -f
```

**Check frontend logs:**
```bash
docker logs card-detection-frontend -f
```

## File Structure Reference

```
card-detection/
├── frontend/app/           # Your React code here
│   ├── routes/            # Add new pages here
│   ├── components/ui/     # shadcn components
│   └── api/detection/     # API functions
├── backend/
│   ├── routers/           # Add new endpoints here
│   └── services/          # Business logic
└── docker-compose.yml     # Start everything
```

## Common Commands

```bash
# Start everything with Docker
docker-compose up

# Rebuild after changes
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Backend only (local)
cd backend && uvicorn main:app --reload

# Frontend only (local)
cd frontend && npm run dev

# Install new npm package
cd frontend && npm install <package-name>

# Install new Python package
cd backend && pip install <package-name>
# Then: pip freeze > requirements.txt
```

## Next Steps for Development

1. **Train Card Detection Model** (see README.md)
2. **Add more routes** in `frontend/app/routes/`
3. **Create custom components** in `frontend/app/components/`
4. **Add backend endpoints** in `backend/routers/`
5. **Deploy to cloud** (AWS, GCP, Azure)

## Troubleshooting

**Node version error:**
- Update to Node.js 22+ (see step 1 above)

**Camera not working:**
- Use HTTPS or localhost
- Check browser permissions
- Try Chrome or Firefox

**Can't install dependencies:**
- Delete `node_modules/` and run `npm install` again
- Delete `venv/` and create fresh virtual environment

**Docker issues:**
- Run `docker-compose down -v` to remove volumes
- Run `docker system prune` to clean up

## Need Help?

- Check README.md for detailed documentation
- Review `.claude/patterns.md` for code patterns
- Inspect existing code in `frontend/app/routes/index.tsx`
- Check FastAPI docs at `/docs` endpoint

---

**You're ready to go!** 🚀

Start with: `docker-compose up --build`
