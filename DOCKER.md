# Docker deployment

Build the Docker image locally:

```bash
docker build -t churn-prediction:latest .
```

Run the container and map port 5000:

```bash
docker run --rm -p 5000:5000 --name churn-app churn-prediction:latest
```

Notes:
- Ensure `models/churn_model.pkl` and `data/cleaned_churn.csv` exist in the project before building; the Docker image copies the workspace into the container.
- The app listens on port `5000` (container) and is exposed to the host at the same port.

Optional: tag and push to Docker Hub:

```bash
docker tag churn-prediction:latest YOUR_DOCKERHUB_USERNAME/churn-prediction:latest
docker push YOUR_DOCKERHUB_USERNAME/churn-prediction:latest
```
