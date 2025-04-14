import { useState } from 'react';
import ChatUI from '../components/ChatUI';
import ProfileSetup from '../components/ProfileSetup';

export default function Home() {
  const [profileComplete, setProfileComplete] = useState(false);
  const [userProfile, setUserProfile] = useState(null);

  const handleProfileSubmit = (profile) => {
    setUserProfile(profile);
    setProfileComplete(true);
    // Store profile in localStorage
    localStorage.setItem('userProfile', JSON.stringify(profile));
  };

  if (!profileComplete) {
    return <ProfileSetup onSubmit={handleProfileSubmit} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-lg font-semibold text-gray-900">
            Job Market Assistant
          </h1>
          <p className="text-sm text-gray-500">
            Helping you navigate the job market based on your profile
          </p>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <ChatUI userProfile={userProfile} />
      </main>
    </div>
  );
}