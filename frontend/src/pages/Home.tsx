import { Link } from 'react-router-dom';
import ApiTest from '../components/ApiTest';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <h1>Healthcare Scheduling System</h1>
        <p>An AI-powered healthcare scheduling system for outpatient procedures</p>
        <div className="cta-buttons">
          <Link to="/scheduling" className="btn btn-primary">Schedule Appointment</Link>
          <Link to="/patients" className="btn btn-secondary">Manage Patients</Link>
        </div>
      </section>

      <section className="features">
        <h2>Key Features</h2>
        <div className="feature-grid">
          <div className="feature-card">
            <h3>Patient Management</h3>
            <p>Create, retrieve, update, and delete patient records</p>
          </div>
          <div className="feature-card">
            <h3>Medical Data Management</h3>
            <p>Manage diagnoses (ICD-10 codes), procedures (CPT codes), and patient-specific medical data</p>
          </div>
          <div className="feature-card">
            <h3>Resource Management</h3>
            <p>Manage resources like rooms and equipment, along with their availability</p>
          </div>
          <div className="feature-card">
            <h3>AI-Powered Scheduling</h3>
            <p>Optimize scheduling of procedures based on various factors</p>
          </div>
        </div>
      </section>

      <section className="api-test-section">
        <h2>System Status</h2>
        <ApiTest />
      </section>
    </div>
  );
};

export default Home;
