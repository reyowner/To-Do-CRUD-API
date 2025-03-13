// Fetch and Render To-Do Items
async function fetchToDos() {
    const response = await fetch("/todos");
    const todos = await response.json();
    const todoList = document.getElementById("todo-list");
    todoList.innerHTML = "";
    
    todos.forEach((todo) => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${todo.task}</span>
            <div>
                <button class="view-btn" onclick="viewToDo(${todo.id})">View</button>
                <button class="edit-btn" onclick="editToDo(${todo.id})">Edit</button>
                <button class="delete-btn" onclick="deleteToDo(${todo.id})">Delete</button>
            </div>
        `;
        todoList.appendChild(listItem);
    });
}

// Add To-Do
async function addToDo() {
    const input = document.getElementById("todo-input");
    if (!input.value.trim()) return;
    
    await fetch("/todos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: input.value.trim() })
    });
    
    input.value = "";
    fetchToDos();
}

// View To-Do
async function viewToDo(id) {
    const response = await fetch(`/todos/${id}`);
    if (!response.ok) return alert("To-Do not found!");
    
    const todo = await response.json();
    document.getElementById("modal-task").innerText = todo.task;
    document.getElementById("todo-modal").style.display = "block";
}

// Close Modal
function closeModal() {
    document.getElementById("todo-modal").style.display = "none";
}

// Edit To-Do
async function editToDo(id) {
    const newTask = prompt("Enter new task:");
    if (!newTask) return;
    
    await fetch(`/todos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: newTask })
    });
    fetchToDos();
}

// Delete To-Do
async function deleteToDo(id) {
    await fetch(`/todos/${id}`, { method: "DELETE" });
    fetchToDos();
}

// Dark Mode Toggle
const darkModeToggle = document.getElementById("dark-mode-toggle");
darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
});

// Load Dark Mode Preference
if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark-mode");
}

// Fetch To-Dos on Load
fetchToDos();
