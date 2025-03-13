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

async function addToDo() {
    const input = document.getElementById("todo-input");
    if (!input.value) return;
    await fetch("/todos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: input.value })
    });
    input.value = "";
    fetchToDos();
}

async function viewToDo(id) {
    const response = await fetch(`/todos/${id}`);
    if (!response.ok) return alert("To-Do not found!");
    
    const todo = await response.json();
    document.getElementById("modal-task").innerText = todo.task;
    document.getElementById("todo-modal").style.display = "block";
}

function closeModal() {
    document.getElementById("todo-modal").style.display = "none";
}

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

async function deleteToDo(id) {
    await fetch(`/todos/${id}`, { method: "DELETE" });
    fetchToDos();
}

fetchToDos();
