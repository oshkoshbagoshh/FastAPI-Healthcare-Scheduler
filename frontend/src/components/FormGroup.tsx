import React from 'react';

interface FormGroupProps {
  label?: string;
  htmlFor?: string;
  error?: string;
  children: React.ReactNode;
  className?: string;
  required?: boolean;
  helpText?: string;
}

const FormGroup: React.FC<FormGroupProps> = ({
  label,
  htmlFor,
  error,
  children,
  className = '',
  required = false,
  helpText,
}) => {
  return (
    <div className={`form-group ${className} ${error ? 'has-error' : ''}`}>
      {label && (
        <label htmlFor={htmlFor} className="form-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      )}
      {children}
      {helpText && <div className="form-help-text">{helpText}</div>}
      {error && <div className="form-error">{error}</div>}
    </div>
  );
};

export default FormGroup;