import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  isLoading, 
  className = '', 
  ...props 
}) => {
  return (
    <button
      className={`
        w-full h-[53px] bg-brand-blue text-white rounded-[4px]
        font-semibold text-base uppercase tracking-normal
        shadow-[0px_4px_4px_rgba(0,0,0,0.3)]
        hover:bg-opacity-90 transition-all duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        flex items-center justify-center
        cursor-pointer
        ${className}
      `}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading ? (
        <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
      ) : (
        children
      )}
    </button>
  );
};
