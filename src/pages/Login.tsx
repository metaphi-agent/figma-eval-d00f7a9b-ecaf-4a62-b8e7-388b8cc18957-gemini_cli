import React, { useState } from 'react';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsSubmitting(false);
    console.log('Login:', { username, password });
  };

  return (
    <div className="min-h-screen w-full bg-brand-blue relative overflow-hidden flex items-center justify-center">
      {/* Background Image */}
      <img 
        src="./assets/images/background.png" 
        alt="" 
        className="absolute inset-0 w-full h-full object-cover z-0 pointer-events-none"
      />
      
      {/* Content Container */}
      <div className="relative z-10 w-[300px] flex flex-col items-center">
         {/* Logo */}
         <div className="mb-[71px]">
            <img 
              src="./assets/logo.svg" 
              alt="Logo" 
              className="w-[120px] h-auto" 
            />
         </div>

         {/* Login Form */}
         <form className="w-full flex flex-col gap-5" onSubmit={handleSubmit}>
            <Input 
               placeholder="USERNAME" 
               icon="./assets/icons/user.svg" 
               value={username}
               onChange={(e) => setUsername(e.target.value)}
               required
            />
            <Input 
               type="password"
               placeholder="PASSWORD" 
               icon="./assets/icons/lock.svg" 
               value={password}
               onChange={(e) => setPassword(e.target.value)}
               required
            />
            
            <Button type="submit" className="mt-[43px]" isLoading={isSubmitting}>
               LOGIN
            </Button>
         </form>

         <a 
           href="#" 
           className="mt-[11px] text-white font-medium text-base hover:underline transition-all"
           onClick={(e) => e.preventDefault()}
         >
            Forgot password?
         </a>
      </div>
    </div>
  );
}
