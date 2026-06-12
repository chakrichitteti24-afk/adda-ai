"use client"
import { Suspense } from 'react';
import RoomClient from './RoomClient';

export default function RoomPage() {
  return (
    <Suspense fallback={<div className="flex h-screen items-center justify-center bg-background text-[#CBD5E1]">Loading Adda Room...</div>}>
      <RoomClient />
    </Suspense>
  );
}
