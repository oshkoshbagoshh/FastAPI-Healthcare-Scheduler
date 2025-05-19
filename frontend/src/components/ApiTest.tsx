import { useState, useEffect } from 'react';
import testApiConnectivity from '../api/testApi';
import Card from './Card';
import Button from './Button';
import './ApiTest.css';

interface TestResult {
  success: boolean;
  patients?: number;
  appointments?: number;
  error?: any;
}

const ApiTest = () => {
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const runTest = async () => {
    setIsLoading(true);
    setTestResult(null);

    try {
      const result = await testApiConnectivity();
      setTestResult(result);
    } catch (error) {
      setTestResult({
        success: false,
        error
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Run the test automatically when the component mounts
    runTest();
  }, []);

  return (
    <Card 
      title="API Connectivity Test" 
      subtitle="Tests the connection between the frontend and backend"
    >
      <div className="api-test">
        {isLoading ? (
          <p>Testing API connectivity...</p>
        ) : testResult ? (
          <div className="test-results">
            <div className={`test-status ${testResult.success ? 'success' : 'error'}`}>
              {testResult.success ? 'Connection Successful ✓' : 'Connection Failed ✗'}
            </div>

            {testResult.success ? (
              <div className="test-details">
                <p>Successfully connected to the backend API.</p>
                <ul>
                  <li>Fetched {testResult.patients} patients</li>
                  <li>Fetched {testResult.appointments} appointments</li>
                </ul>
              </div>
            ) : (
              <div className="test-details error">
                <p>Failed to connect to the backend API. Please check:</p>
                <ul>
                  <li>The backend server is running</li>
                  <li>CORS is properly configured</li>
                  <li>Network connectivity</li>
                </ul>
                <div className="error-message">
                  {testResult.error?.message || 'Unknown error'}
                </div>
              </div>
            )}
          </div>
        ) : null}

        <div className="test-actions">
          <Button 
            onClick={runTest} 
            isLoading={isLoading}
            variant="primary"
          >
            Run Test Again
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default ApiTest;
