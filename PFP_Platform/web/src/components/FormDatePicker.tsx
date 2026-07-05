import React from 'react';
import { UseFormRegister, FieldError } from 'react-hook-form';

interface FormDatePickerProps {
  label: string;
  name: string;
  register: UseFormRegister<any>;
  error?: FieldError;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  helpText?: string;
  includeTime?: boolean;
}

const FormDatePicker: React.FC<FormDatePickerProps> = ({
  label,
  name,
  register,
  error,
  required = false,
  disabled = false,
  className = '',
  helpText,
  includeTime = false,
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        id={name}
        type={includeTime ? 'datetime-local' : 'date'}
        disabled={disabled}
        {...register(name, { required: required && `${label} is required` })}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
          ${error ? 'border-red-300' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      />
      {helpText && !error && (
        <p className="mt-1 text-sm text-gray-500">{helpText}</p>
      )}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error.message}</p>
      )}
    </div>
  );
};

export default FormDatePicker;