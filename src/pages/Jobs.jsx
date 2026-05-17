import { useEffect, useState } from "react";

import API from "../api/axios";

import Navbar from "../components/Navbar";

function Jobs() {

  const [jobs, setJobs] = useState([]);

  useEffect(() => {

    fetchJobs();

  }, []);

  const fetchJobs = async () => {

    try {

      const response = await API.get("/jobs");

      console.log(response.data);

      setJobs(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  return (

    <>
      <Navbar />

      <div style={{ padding: "20px" }}>

        <h1>Jobs Page</h1>

        {
          jobs.length === 0 ? (

            <p>No Jobs Found</p>

          ) : (

            jobs.map((job) => (

              <div
                key={job.id}
                style={{
                  border: "1px solid gray",
                  padding: "15px",
                  marginBottom: "10px",
                }}
              >

                <h3>{job.title}</h3>

                <p>{job.description}</p>

                <p>{job.location}</p>

              </div>

            ))
          )
        }

      </div>
    </>
  );
}

export default Jobs;