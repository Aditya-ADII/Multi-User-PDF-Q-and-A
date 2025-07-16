# Multi-User PDF Q&A

A Streamlit-based web app for uploading and querying multiple PDF research papers concurrently, using FAISS for vector search, Redis for storage, Gemini 1.5 Flash API for answers, and Kubernetes/Docker for deployment.

## Features
- Upload PDFs and ask questions about their content.
- Supports multiple users with isolated sessions via unique `user_id`.
- FAISS enables fast similarity search for context retrieval.
- Redis stores text chunks, embeddings, and chat history.
- Gemini 1.5 Flash API generates concise answers.
- Deployed on Kubernetes with Docker for scalability.

## Prerequisites
- **Docker Desktop**: Installed and running on Windows.
- **Kubernetes**: Enabled in Docker Desktop.
- **PowerShell**: For running commands.
- **Gemini API Key**: Obtain from [Google AI Studio](https://aistudio.google.com/).
- Free disk space: ~25GB for Docker images and builds.

## Setup Instructions
1. Set up the Gemini API key in `k8s/deployment.yaml` and `app/gemini_api.py`:
   ```yaml
   - name: GEMINI_API_KEY
     value: "<your-real-key>"
   ```
2. Ensure Docker Desktop and Kubernetes are running.

## Project Structure
```
multi_user_pdf_qa/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── utils/
│   │   ├── embeddings.py
│   │   ├── pdf_processor.py
│   │   ├── redis_client.py
│   │   ├── gemini_api.py
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── redis/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
├── screenshots/
│   ├── streamlit_paper1.png
│   ├── streamlit_paper2.png
│   ├── streamlit_paper3.png
│   ├── streamlit_paper4.png
│   ├── streamlit_paper5.png
│   ├── docker_build.png
│   ├── kubectl_commands.png
│   ├── docker_containers.png
│   ├── docker_images.png
│   ├── docker_volumes.png
│   ├── docker_builds.png
│   ├── kubectl_docker_status.png
├── readme.markdown
```

## How It Works
1. **PDF Upload**: Users upload PDFs via Streamlit, saved temporarily.
2. **Text Extraction**: `PyPDF2` extracts text, split into chunks.
3. **Embedding**: `sentence-transformers` (`all-MiniLM-L6-v2`) generates embeddings.
4. **Storage**: Chunks, embeddings, and FAISS index stored in Redis.
5. **Querying**: User questions are embedded, matched via FAISS, and context sent to Gemini 1.5 Flash.
6. **Response**: Gemini generates concise answers, stored in Redis chat history.
7. **Multi-User**: Kubernetes/Docker ensures isolated sessions per user.

## Running the Project
1. Build the Docker image:
   ```powershell
   cd app
   docker build -t multi-user-pdf-qa:latest .
   ```
   See `screenshots/docker_build.png`.

2. Deploy to Kubernetes:
   ```powershell
   cd ../k8s
   kubectl apply -f redis/deployment.yaml
   kubectl apply -f redis/service.yaml
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
   See `screenshots/kubectl_commands.png`.

3. Forward the Streamlit service port:
   ```powershell
   kubectl port-forward svc/streamlit-service 8501:8501
   ```
   See `screenshots/kubectl_commands.png`.

4. Access the app at `http://localhost:8501`.
   - Upload a PDF (e.g., *Generative Agents Interactive Simulacra of Human Behavior.pdf*).
   - Ask: “What is this paper about in one line?”
   - See `screenshots/streamlit_paper1.png` to `streamlit_paper5.png` for 5 papers.

5. Verify system status:
   ```powershell
   kubectl get pods
   kubectl get svc
   docker ps
   ```
   See `screenshots/kubectl_docker_status.png`.

6. Check Docker Desktop:
   - Containers: `screenshots/docker_containers.png`
   - Images: `screenshots/docker_images.png`
   - Volumes: `screenshots/docker_volumes.png`
   - Builds: `screenshots/docker_builds.png`

## Dependencies
- `streamlit==1.45.1`: Web app interface.
- `redis==3.2.0`: Stores chunks, embeddings, and history.
- `faiss-cpu==1.7.4`: Vector similarity search.
- `PyPDF2==3.0.1`: PDF text extraction.
- `sentence-transformers==2.2.2`: Text embeddings.
- `google-generativeai==0.8.5`: Gemini 1.5 Flash API.
- `torch==2.0.1`: ML framework.
- `transformers==4.28.1`: Hugging Face models.
- `huggingface_hub==0.16.4`: Model access.
- `numpy==1.23.1`: Numerical computations.

## Demo Results

Tested with 5 research papers. Screenshots are available in the `screenshots/` folder:

### Streamlit UI
- ![Paper 1](screenshots/streamlit_paper1.png)
- ![Paper 2](screenshots/streamlit_paper2.png)
- ![Paper 3](screenshots/streamlit_paper3.png)
- ![Paper 4](screenshots/streamlit_paper4.png)
- ![Paper 5](screenshots/streamlit_paper5.png)

### Docker & Kubernetes
- ![Docker Build](screenshots/docker_build.png)
- ![Kubectl Commands](screenshots/kubectl_commands.png)
- ![Running Containers](screenshots/docker_containers.png)
- ![Docker Images](screenshots/docker_images.png)
- ![Docker Volumes](screenshots/docker_volumes.png)
- ![Docker Build History](screenshots/docker_builds.png)
- ![Kubectl + Docker Status](screenshots/kubectl_docker_status.png)
