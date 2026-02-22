const API_URL = '/users';

function loadUsers() {
    fetch(API_URL)
        .then(response => response.json())
        .then(users => renderTable(users))
        .catch(error => console.error('Ошибка загрузки пользователей:', error));
}

function renderTable(users) {
    const tbody = document.querySelector('#users-table tbody');
    tbody.innerHTML = '';

    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.addEventListener('click', () => showUserDetail(user.id));
        tr.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
        `;
        tbody.appendChild(tr);
    });
}

function showUserDetail(userId) {
    fetch(`${API_URL}/${userId}`)
        .then(response => {
            if (!response.ok) throw new Error('Пользователь не найден');
            return response.json();
        })
        .then(user => {
            document.getElementById('modal-user-id').textContent = user.id;
            document.getElementById('modal-user-name').textContent = user.name;
            document.getElementById('modal-user-email').textContent = user.email;

            const modal = new bootstrap.Modal(document.getElementById('userModal'));
            modal.show();
        })
        .catch(error => console.error('Ошибка загрузки пользователя:', error));
}

function handleAddUser(event) {
    event.preventDefault();

    const name = document.getElementById('input-name').value.trim();
    const email = document.getElementById('input-email').value.trim();

    fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
    })
        .then(response => {
            if (!response.ok) return response.json().then(data => { throw new Error(data.error); });
            return response.json();
        })
        .then(user => {
            showAlert(`Пользователь «${user.name}» добавлен`, 'success');
            document.getElementById('add-user-form').reset();
            loadUsers();
        })
        .catch(error => {
            showAlert(error.message || 'Ошибка при добавлении', 'danger');
        });
}

function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    container.prepend(alert);

    setTimeout(() => alert.remove(), 5000);
}

document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    document.getElementById('add-user-form').addEventListener('submit', handleAddUser);
});
