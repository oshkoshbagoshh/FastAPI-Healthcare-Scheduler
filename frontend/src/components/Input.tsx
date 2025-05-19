import React, { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  className?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ error, className = '', ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={`form-input ${error ? 'input-error' : ''} ${className}`}
        {...props}
      />
    );
  }
);

Input.displayName = 'Input';

export default Input;