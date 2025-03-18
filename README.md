# 📌 **To-Do List API with FastAPI**  

This project is a **CRUD-based To-Do List API** built with **FastAPI**, featuring:  
✅ Aesthetic & UX improvements with a **military matte green theme**.  
✅ A **Dark Mode Toggle** with **localStorage persistence**.  
✅ A fully responsive **frontend using HTML, CSS, and JavaScript**.  
✅ A **backend powered by FastAPI** with database integration for persistent storage.  


## 🔹 **Features**  
### ✅ **FastAPI Backend**  
- Fully functional **CRUD API** for managing to-do items.  
- Uses **Pydantic models** for validation and structured responses.  
- Returns proper **HTTP status codes** for errors (e.g., `400`, `404`).  

### ✅ **Modern UI with Improved UX**  
- **Military Matte Green (#454B1B) theme** for a sleek, unique look.  
- **Enhanced button designs** with hover effects.  
- **Smooth modal animations** for better user experience.  

### ✅ **Persistent Dark Mode**  
- **Dark mode toggle button** for a better user experience.  
- Saves user preference in **localStorage** so the setting remains after refresh.  

### ✅ **RESTful API with Frontend Integration**  
- JavaScript **fetch API** interacts with the FastAPI backend dynamically.  
- UI updates **instantly** when tasks are added, edited, or deleted.  

---

## 🚀 Getting Started (Dockerized Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/To-Do-List_Python.git
cd To-Do-List_Python
```

### 2️⃣ Install Dependencies
Ensure Docker is installed on your machine. If not, download and install it from [Docker's official website](https://www.docker.com/products/docker-desktop/)

### 3️⃣ Build and Run the Containers
Use docker-compose to build and start the backend container.
```bash
docker-compose up -d --build
```
This command will:
✅ Build the FastAPI backend container  
✅ Start the container in detached mode (-d)

### 4️⃣ Verify Running Containers
To check if the container is running correctly, use:
```bash
docker ps
```
You should see the running container:
```bash
CONTAINER ID   IMAGE                        COMMAND                  PORTS                    NAMES
xxxxx          to-do-list_python-backend    "uvicorn main:app --…"   0.0.0.0:8000->8000/tcp   to-do-list_python-backend-1
```

### 5️⃣ Access the Application
Once the container is running, open the application in your browser:
🔗 API Endpoint: [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive API documentation)  
🔗 To-Do List API: [http://localhost:8000/todos](http://localhost:8000/todos) (Check stored to-dos)

### 🛑 Stopping the Application
To stop the running container, use:
```bash
docker-compose down
```
This will gracefully shut down the service.

---

## 🔹 **Tech Stack**  
| Technology  | Usage |
|-------------|--------------------------------------------------|
| **FastAPI** | Backend API framework |
| **SQLite**  | Database for persistent storage |
| **Pydantic** | Data validation and serialization |
| **Jinja2** | Template rendering for frontend |
| **HTML5** | Markup language for UI |
| **CSS3** | Styling and Dark Mode implementation |
| **JavaScript (Vanilla)** | Frontend interactivity and API calls |