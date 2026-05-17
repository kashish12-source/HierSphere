import Navbar from "../components/Navbar";

function Dashboard()
{
  return(
    <>
    <Navbar/>
      <div className="p-20">
        <h1>  Dashboard</h1>
        <div className="flex gap-20 mt-20">
          <div className="border-solid-gray-1 p-20 w-200">
            <h3>Applied job</h3>
            <p>12</p>


          </div>
          <div className="border-solid-gray-1 p-20 w-200 ">
            <h3>Resume Score</h3>
            <p>85%</p>

          </div>
        </div>
      </div>
    
    </>
  );
}
export default Dashboard;
