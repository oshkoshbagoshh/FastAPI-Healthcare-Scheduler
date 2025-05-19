import { patientsApi, schedulingApi } from './apiClient';

/**
 * Test function to verify API connectivity
 * This function makes simple requests to the backend API to verify connectivity
 */
export const testApiConnectivity = async () => {
  try {
    console.log('Testing API connectivity...');
    
    // Test patients API
    console.log('Testing patients API...');
    const patientsResponse = await patientsApi.getAll();
    console.log(`Successfully fetched ${patientsResponse.data.length} patients`);
    
    // Test scheduling API
    console.log('Testing scheduling API...');
    const appointmentsResponse = await schedulingApi.getAppointments();
    console.log(`Successfully fetched ${appointmentsResponse.data.length} appointments`);
    
    console.log('API connectivity test completed successfully!');
    return {
      success: true,
      patients: patientsResponse.data.length,
      appointments: appointmentsResponse.data.length
    };
  } catch (error) {
    console.error('API connectivity test failed:', error);
    return {
      success: false,
      error
    };
  }
};

export default testApiConnectivity;