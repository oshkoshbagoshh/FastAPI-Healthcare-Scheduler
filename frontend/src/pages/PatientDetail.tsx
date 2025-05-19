import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';

interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone_number: string;
  email: string;
  address: string;
  insurance_provider: string;
  insurance_id: string;
}

interface PatientUpdate {
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  email?: string;
  address?: string;
  insurance_provider?: string;
  insurance_id?: string;
}

const PatientDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<PatientUpdate>({});

  const fetchPatient = async () => {
    const response = await axios.get(`/api/patients/${id}`);
    return response.data;
  };

  const { data: patient, isLoading, isError } = useQuery<Patient>(
    ['patient', id],
    fetchPatient,
    {
      onSuccess: (data) => {
        setFormData({
          first_name: data.first_name,
          last_name: data.last_name,
          phone_number: data.phone_number,
          email: data.email,
          address: data.address,
          insurance_provider: data.insurance_provider,
          insurance_id: data.insurance_id,
        });
      },
    }
  );

  const updatePatient = useMutation(
    (updatedPatient: PatientUpdate) => 
      axios.put(`/api/patients/${id}`, updatedPatient),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['patient', id]);
        setIsEditing(false);
      },
    }
  );

  const deletePatient = useMutation(
    () => axios.delete(`/api/patients/${id}`),
    {
      onSuccess: () => {
        navigate('/patients');
      },
    }
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updatePatient.mutate(formData);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this patient?')) {
      deletePatient.mutate();
    }
  };

  if (isLoading) return <p>Loading patient details...</p>;
  if (isError) return <p className="error">Error loading patient details. Please try again.</p>;
  if (!patient) return <p>Patient not found.</p>;

  return (
    <div className="patient-detail-page">
      <div className="page-header">
        <h1>
          {isEditing ? 'Edit Patient' : `${patient.first_name} ${patient.last_name}`}
        </h1>
        <div className="actions">
          {isEditing ? (
            <>
              <button 
                className="btn btn-secondary" 
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </button>
              <button 
                className="btn btn-primary" 
                onClick={handleSubmit}
                disabled={updatePatient.isLoading}
              >
                Save Changes
              </button>
            </>
          ) : (
            <>
              <button 
                className="btn btn-primary" 
                onClick={() => setIsEditing(true)}
              >
                Edit
              </button>
              <button 
                className="btn btn-danger" 
                onClick={handleDelete}
                disabled={deletePatient.isLoading}
              >
                Delete
              </button>
            </>
          )}
        </div>
      </div>

      {isEditing ? (
        <form className="patient-form">
          <div className="form-group">
            <label htmlFor="first_name">First Name</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name || ''}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="last_name">Last Name</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name || ''}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="phone_number">Phone Number</label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number || ''}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email || ''}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="address">Address</label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address || ''}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="insurance_provider">Insurance Provider</label>
            <input
              type="text"
              id="insurance_provider"
              name="insurance_provider"
              value={formData.insurance_provider || ''}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="insurance_id">Insurance ID</label>
            <input
              type="text"
              id="insurance_id"
              name="insurance_id"
              value={formData.insurance_id || ''}
              onChange={handleInputChange}
            />
          </div>
        </form>
      ) : (
        <div className="patient-info">
          <div className="info-section">
            <h2>Personal Information</h2>
            <div className="info-grid">
              <div className="info-item">
                <span className="label">Date of Birth:</span>
                <span className="value">{new Date(patient.date_of_birth).toLocaleDateString()}</span>
              </div>
              <div className="info-item">
                <span className="label">Gender:</span>
                <span className="value">{patient.gender}</span>
              </div>
              <div className="info-item">
                <span className="label">Phone:</span>
                <span className="value">{patient.phone_number}</span>
              </div>
              <div className="info-item">
                <span className="label">Email:</span>
                <span className="value">{patient.email}</span>
              </div>
              <div className="info-item">
                <span className="label">Address:</span>
                <span className="value">{patient.address}</span>
              </div>
            </div>
          </div>
          
          <div className="info-section">
            <h2>Insurance Information</h2>
            <div className="info-grid">
              <div className="info-item">
                <span className="label">Provider:</span>
                <span className="value">{patient.insurance_provider}</span>
              </div>
              <div className="info-item">
                <span className="label">ID:</span>
                <span className="value">{patient.insurance_id}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientDetail;