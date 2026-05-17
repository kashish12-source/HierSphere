import { Link,useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function Navbar()
{
    const {logout}=useContext(AuthContext);
    const navigate =useNavigate();
    const handlelogout=()=>{
        logout();
        navigate("/login");

    };
    return(
        <nav style={{
            display:"flex",
            justifyContent:"space-between",
            alignItems:"center",
            padding:"20px",
            backgroundColor:"#222",
            color:"white",

        }}>
             <h2>HireSphere</h2>
            <div  className='flex gap-20'>
                <Link to='/dashboard' className='white'>Dashboard</Link>
                <Link to='/jobs' className='white'>Jobs</Link>
                <button onClick={handlelogout}>
                    Logout
                </button>
            </div>
           
            
        </nav>
    );
}
export default Navbar;