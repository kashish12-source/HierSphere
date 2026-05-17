import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";

import API from "../api/axios";
import { AuthContext } from "../context/AuthContext";


function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const { login } = useContext(AuthContext);

    const navigate = useNavigate();
const handleSubmit = async (e) => {

    e.preventDefault();

    try {

        const formData = new FormData();

        formData.append(
            "username",
            email
        );

        formData.append(
            "password",
            password
        );

        const response = await API.post(
            "/login",
            formData
        );

        login(response.data.access_token);

        navigate("/dashboard");

    }

    catch (error) {

        console.log(error);

        alert("Invalid Credential");

    }
};
    return (
        <div className='flex justify-center items-center h-100'>
            <form onSubmit={handleSubmit} className="flex column w-300 gap-15">
                <h1>Login</h1>
                <input type='email' placeholder='email' value={email} onChange={(e) =>
                    setEmail(e.target.value)
                }>

                </input>
                <input type='password'autoComplete="current-password" placeholder='123@-' value={password} onChange={(e) => { setPassword(e.target.value) }}></input>
                <button type='submit'>
                    Login

                </button>
                <p>Don't have an account?
                    <Link to='/register'>Register</Link>
                </p>


            </form>
        </div>
    );
}
export default Login;