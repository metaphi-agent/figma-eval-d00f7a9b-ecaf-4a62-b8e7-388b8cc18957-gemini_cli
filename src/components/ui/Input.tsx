import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  icon?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ 
  icon, 
  error, 
  className = '', 
  ...props 
}) => {
  return (
    <div className="w-full relative group">
      <div className="relative flex items-center">
        {icon && (
          <div className="absolute left-3 z-10 flex items-center justify-center w-5 h-5 pointer-events-none">
            <img src={icon} alt="" className="w-full h-full object-contain" />
          </div>
        )}
        <input
          className={`
            w-full h-[45px] bg-transparent
            border border-white rounded-[4px]
            text-white font-light text-sm uppercase placeholder-white
            focus:outline-none focus:ring-1 focus:ring-white/50
            transition-all duration-200
            ${icon ? 'pl-12 pr-4' : 'px-4'}
            ${error ? 'border-red-400' : 'border-white'}
            ${className}
          `}
          {...props}
        />
      </div>
      {error && (
        <span className="text-red-300 text-xs mt-1 absolute -bottom-5 left-0">
          {error}
        </span>
      )}
    </div>
  );
};
