import { useState } from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import axios from 'axios';

interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone_number: string;
  email: string;
}

const Patients = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const fetchPatients = async () => {
    const params = searchTerm ? { name: searchTerm } : {};
    const response = await axios.get('/api/patients/', { params });
    return response.data;
  };

  const { data: patients, isLoading, isError, refetch } = useQuery<Patient[]>(
    ['patients', searchTerm],
    fetchPatients,
    {
      keepPreviousData: true,
      staleTime: 5000,
    }
  );

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    refetch();
  };

  return (
    <div className="patients-page">
      <div className="page-header">
        <h1>Patients</h1>
        <Link to="/patients/new" className="btn btn-primary">Add New Patient</Link>
      </div>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit" className="btn">Search</button>
      </form>

      {isLoading ? (
        <p>Loading patients...</p>
      ) : isError ? (
        <p className="error">Error loading patients. Please try again.</p>
      ) : patients && patients.length > 0 ? (
        <div className="patients-list">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Date of Birth</th>
                <th>Gender</th>
                <th>Contact</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {patients.map((patient) => (
                <tr key={patient.id}>
                  <td>{patient.id}</td>
                  <td>{patient.first_name} {patient.last_name}</td>
                  <td>{new Date(patient.date_of_birth).toLocaleDateString()}</td>
                  <td>{patient.gender}</td>
                  <td>
                    <div>{patient.phone_number}</div>
                    <div>{patient.email}</div>
                  </td>
                  <td>
                    <Link to={`/patients/${patient.id}`} className="btn btn-small">View</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No patients found. Try a different search or add a new patient.</p>
      )}
    </div>
  );
};

export default Patients;