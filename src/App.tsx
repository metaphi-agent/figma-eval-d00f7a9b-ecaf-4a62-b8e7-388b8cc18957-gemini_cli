import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

// Lazy load pages
const Login = React.lazy(() => import('./pages/Login'));

function App() {
  return (
    <Suspense fallback={
      <div className="min-h-screen w-full bg-brand-blue flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
      </div>
    }>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="*" element={<Login />} />
      </Routes>
    </Suspense>
  );
}

export default App;
