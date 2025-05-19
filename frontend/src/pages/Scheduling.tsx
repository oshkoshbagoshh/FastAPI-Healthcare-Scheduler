import { useState } from 'react';
import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { format } from 'date-fns';

interface ScheduleRequest {
  start_date: string;
  end_date: string;
  patient_ids?: number[];
  procedure_ids?: number[];
  priority_weight?: number;
  duration_weight?: number;
  resource_utilization_weight?: number;
  patient_preference_weight?: number;
}

const Scheduling = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<ScheduleRequest>({
    start_date: format(new Date(), 'yyyy-MM-dd'),
    end_date: format(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd'),
    priority_weight: 1.0,
    duration_weight: 1.0,
    resource_utilization_weight: 1.0,
    patient_preference_weight: 1.0,
  });

  const optimizeSchedule = useMutation(
    (scheduleRequest: ScheduleRequest) => 
      axios.post('/api/scheduling/optimize/', scheduleRequest),
    {
      onSuccess: () => {
        navigate('/appointments');
      },
    }
  );

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    if (type === 'number') {
      setFormData({ ...formData, [name]: parseFloat(value) });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    optimizeSchedule.mutate(formData);
  };

  return (
    <div className="scheduling-page">
      <div className="page-header">
        <h1>Schedule Optimization</h1>
      </div>

      <div className="card">
        <div className="card-body">
          <p>
            This tool uses AI to create an optimal schedule for patient procedures based on various factors
            including procedure priority, duration, resource availability, and patient preferences.
          </p>
        </div>
      </div>

      <form className="schedule-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h2>Date Range</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_date">Start Date</label>
              <input
                type="date"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="end_date">End Date</label>
              <input
                type="date"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Optimization Weights</h2>
          <p className="form-help">
            Adjust these values to prioritize different factors in the scheduling algorithm.
            Higher values give more importance to that factor.
          </p>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="priority_weight">Procedure Priority</label>
              <input
                type="number"
                id="priority_weight"
                name="priority_weight"
                min="0"
                max="2"
                step="0.1"
                value={formData.priority_weight}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="duration_weight">Procedure Duration</label>
              <input
                type="number"
                id="duration_weight"
                name="duration_weight"
                min="0"
                max="2"
                step="0.1"
                value={formData.duration_weight}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="resource_utilization_weight">Resource Utilization</label>
              <input
                type="number"
                id="resource_utilization_weight"
                name="resource_utilization_weight"
                min="0"
                max="2"
                step="0.1"
                value={formData.resource_utilization_weight}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="patient_preference_weight">Patient Preference</label>
              <input
                type="number"
                id="patient_preference_weight"
                name="patient_preference_weight"
                min="0"
                max="2"
                step="0.1"
                value={formData.patient_preference_weight}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={optimizeSchedule.isLoading}
          >
            {optimizeSchedule.isLoading ? 'Optimizing...' : 'Optimize Schedule'}
          </button>
        </div>

        {optimizeSchedule.isError && (
          <div className="error-message">
            An error occurred while optimizing the schedule. Please try again.
          </div>
        )}
      </form>
    </div>
  );
};

export default Scheduling;