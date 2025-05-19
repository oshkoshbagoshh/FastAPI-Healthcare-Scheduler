import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { format, parseISO } from 'date-fns';

interface Appointment {
  id: number;
  patient_id: number;
  procedure_id: number;
  resource_id: number;
  scheduled_date: string;
  start_time: string;
  end_time: string;
  status: string;
  notes: string;
  patient?: {
    first_name: string;
    last_name: string;
  };
  procedure?: {
    name: string;
  };
  resource?: {
    name: string;
  };
}

const Appointments = () => {
  const queryClient = useQueryClient();
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [status, setStatus] = useState<string>('');

  const fetchAppointments = async () => {
    const params: Record<string, string> = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    if (status) params.status = status;

    const response = await axios.get('/api/scheduling/appointments/', { params });
    return response.data;
  };

  const { data: appointments, isLoading, isError, refetch } = useQuery<Appointment[]>(
    ['appointments', startDate, endDate, status],
    fetchAppointments,
    {
      keepPreviousData: true,
    }
  );

  const cancelAppointment = useMutation(
    (appointmentId: number) => 
      axios.put(`/api/scheduling/appointments/${appointmentId}/cancel`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('appointments');
      },
    }
  );

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    refetch();
  };

  const handleCancel = (appointmentId: number) => {
    if (window.confirm('Are you sure you want to cancel this appointment?')) {
      cancelAppointment.mutate(appointmentId);
    }
  };

  const formatDateTime = (date: string, time: string) => {
    try {
      const dateTime = parseISO(`${date}T${time}`);
      return format(dateTime, 'MMM d, yyyy h:mm a');
    } catch (error) {
      return `${date} ${time}`;
    }
  };

  return (
    <div className="appointments-page">
      <div className="page-header">
        <h1>Appointments</h1>
      </div>

      <div className="filter-section">
        <form className="filter-form" onSubmit={handleFilter}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_date">Start Date</label>
              <input
                type="date"
                id="start_date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="end_date">End Date</label>
              <input
                type="date"
                id="end_date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="">All</option>
                <option value="scheduled">Scheduled</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div className="form-group">
              <button type="submit" className="btn">Filter</button>
            </div>
          </div>
        </form>
      </div>

      {isLoading ? (
        <p>Loading appointments...</p>
      ) : isError ? (
        <p className="error">Error loading appointments. Please try again.</p>
      ) : appointments && appointments.length > 0 ? (
        <div className="appointments-list">
          <table>
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Patient</th>
                <th>Procedure</th>
                <th>Resource</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((appointment) => (
                <tr key={appointment.id} className={`status-${appointment.status}`}>
                  <td>
                    {formatDateTime(appointment.scheduled_date, appointment.start_time)}
                    <div className="text-small">
                      to {format(parseISO(`${appointment.scheduled_date}T${appointment.end_time}`), 'h:mm a')}
                    </div>
                  </td>
                  <td>
                    {appointment.patient ? 
                      `${appointment.patient.first_name} ${appointment.patient.last_name}` : 
                      `Patient #${appointment.patient_id}`}
                  </td>
                  <td>
                    {appointment.procedure ? 
                      appointment.procedure.name : 
                      `Procedure #${appointment.procedure_id}`}
                  </td>
                  <td>
                    {appointment.resource ? 
                      appointment.resource.name : 
                      `Resource #${appointment.resource_id}`}
                  </td>
                  <td>
                    <span className={`status-badge ${appointment.status}`}>
                      {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                    </span>
                  </td>
                  <td>
                    {appointment.status === 'scheduled' && (
                      <button
                        className="btn btn-small btn-danger"
                        onClick={() => handleCancel(appointment.id)}
                        disabled={cancelAppointment.isLoading}
                      >
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No appointments found. Try different filter criteria or schedule new appointments.</p>
      )}
    </div>
  );
};

export default Appointments;