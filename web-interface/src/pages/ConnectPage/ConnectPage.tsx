import { useNavigate } from "react-router-dom";

import "./ConnectPage.scss";
import { connectToDatabase } from "../../API/API.ts";

export default function ConnectPage() {
    const navigate = useNavigate();
    // const [databaseType, set]

    const sendForm = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const formData = new FormData(event.currentTarget);

        const copy = formData.get('copy') ? true : false;

        const response = await connectToDatabase({
            database: "postgresql",
            url: formData.get('url')?.toString() || '',
            port: formData.get('port')?.toString() || '',
            user: formData.get('user')?.toString() || '',
            password: formData.get('password')?.toString() || '',
            copyDatabase: copy,
        });

        if (response === 200) {
            navigate('/test');
        }
    }

    return (
        <div className='connection-setup-container'>
            <h1>
                Подключение
                <br/>
                <span className="datbase-name">PostgreSQL</span>
            </h1>
            <div className='user-input-container'>
                <div className='form-continer'>
                    <form onSubmit={sendForm} className='database-connection-form'>
                        <h3>Сервер</h3>

                        <label htmlFor="url">
                            <span>Хост: </span>
                            <input type="text" placeholder='localhost' name='url'/>
                        </label>
                        <label htmlFor="port">
                            <span>Порт: </span>
                            <input type="number" placeholder='5432' name='port'/>
                        </label>
                        <h3>Аутентификация</h3>
                        <label htmlFor="user">
                            <span>Пользователь: </span>
                            <input type="text" placeholder='postgres' name='user'/>
                        </label>
                        <label htmlFor="password">
                            <span>Пароль: </span>
                            <input type="password" placeholder='******' name='password'/>
                        </label>
                        <label htmlFor="copy" id="copyLabel">
                            <span>Коприровать БД: </span>
                            <input type="checkbox" name='copy' defaultChecked/>
                        </label>

                        <button type="submit">Connect</button>
                    </form>
                </div>
            </div>
      </div>
    )
}