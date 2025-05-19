import axios from 'axios';

// Create an axios instance with default config
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication if needed
apiClient.interceptors.request.use(
  (config) => {
    // You can add auth token here if needed
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors here
    if (error.response) {
      // Server responded with an error status
      console.error('API Error:', error.response.data);
      
      // Handle authentication errors
      if (error.response.status === 401) {
        // Redirect to login or refresh token
        console.error('Authentication error');
        // window.location.href = '/login';
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API functions for patients
export const patientsApi = {
  getAll: (params = {}) => apiClient.get('/patients/', { params }),
  getById: (id: number) => apiClient.get(`/patients/${id}`),
  create: (data: any) => apiClient.post('/patients/', data),
  update: (id: number, data: any) => apiClient.put(`/patients/${id}`, data),
  delete: (id: number) => apiClient.delete(`/patients/${id}`),
};

// API functions for scheduling
export const schedulingApi = {
  optimizeSchedule: (data: any) => apiClient.post('/scheduling/optimize/', data),
  getAppointments: (params = {}) => apiClient.get('/scheduling/appointments/', { params }),
  getAppointmentById: (id: number) => apiClient.get(`/scheduling/appointments/${id}`),
  cancelAppointment: (id: number) => apiClient.put(`/scheduling/appointments/${id}/cancel`),
};

// API functions for medical data
export const medicalApi = {
  getDiagnoses: (params = {}) => apiClient.get('/medical/diagnoses/', { params }),
  getProcedures: (params = {}) => apiClient.get('/medical/procedures/', { params }),
  getPatientDiagnoses: (patientId: number) => apiClient.get(`/medical/patients/${patientId}/diagnoses`),
  getPatientProcedures: (patientId: number) => apiClient.get(`/medical/patients/${patientId}/procedures`),
};

// API functions for resources
export const resourcesApi = {
  getAll: (params = {}) => apiClient.get('/resources/', { params }),
  getById: (id: number) => apiClient.get(`/resources/${id}`),
  getAvailability: (resourceId: number, params = {}) => 
    apiClient.get(`/resources/${resourceId}/availability`, { params }),
};

export default apiClient;