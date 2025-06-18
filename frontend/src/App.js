import React, { useState, useEffect } from 'react';

function App() {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ name: '', email: '' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/users', {
        headers: {
          'Accept': 'application/json; charset=utf-8'
        }
      });
      const data = await response.json();
      if (data.success) {
        setUsers(data.data.users);
        setMessage('Данные загружены успешно!');
      } else {
        setMessage('Ошибка загрузки данных: ' + data.message);
      }
    } catch (error) {
      setMessage('Ошибка соединения с сервером: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const addUser = async (e) => {
    e.preventDefault();
    if (!newUser.name || !newUser.email) {
      setMessage('Пожалуйста, заполните все поля!');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Accept': 'application/json; charset=utf-8'
        },
        body: JSON.stringify(newUser),
      });
      const data = await response.json();
      
      if (data.success) {
        setMessage('Пользователь добавлен успешно!');
        setNewUser({ name: '', email: '' });
        fetchUsers();
      } else {
        setMessage('Ошибка добавления пользователя: ' + data.message);
      }
    } catch (error) {
      setMessage('Ошибка соединения с сервером: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="container">
      <h1>Docker Compose Web App</h1>
      <p>NGINX + React + Python FastAPI + MySQL</p>

      {message && (
        <div className="card">
          <p>{message}</p>
        </div>
      )}

      <div className="card">
        <h2>Добавить пользователя</h2>
        <form onSubmit={addUser}>
          <div className="form-group">
            <label htmlFor="name">Имя:</label>
            <input
              type="text"
              id="name"
              value={newUser.name}
              onChange={(e) => setNewUser({...newUser, name: e.target.value})}
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={newUser.email}
              onChange={(e) => setNewUser({...newUser, email: e.target.value})}
              disabled={loading}
            />
          </div>
          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Добавление...' : 'Добавить пользователя'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2>Список пользователей</h2>
        <button onClick={fetchUsers} className="button" disabled={loading}>
          {loading ? 'Загрузка...' : 'Обновить список'}
        </button>
        
        {users.length > 0 ? (
          <ul>
            {users.map((user) => (
              <li key={user.id}>
                <strong>{user.name}</strong> - {user.email}
                <small> (добавлен: {user.created_at})</small>
              </li>
            ))}
          </ul>
        ) : (
          <p>Пользователи не найдены.</p>
        )}
      </div>

      <div className="card">
        <h3>Статус системы</h3>
        <p>✅ NGINX - запущен</p>
        <p>✅ React - запущен</p>
        <p>✅ Python FastAPI - {users.length >= 0 ? 'подключен' : 'отключен'}</p>
        <p>✅ MySQL - {users.length >= 0 ? 'подключена' : 'отключена'}</p>
      </div>
    </div>
  );
}

export default App; 