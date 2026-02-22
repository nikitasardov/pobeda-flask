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

document.addEventListener('DOMContentLoaded', loadUsers);
