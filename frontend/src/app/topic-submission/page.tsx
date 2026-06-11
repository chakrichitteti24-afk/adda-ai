"use client"
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function TopicSubmission() {
  const [title, setTitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiBaseUrl}/api/v1/topics/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description: '' })
      });
      const data = await res.json();
      
      const startRes = await fetch(`${apiBaseUrl}/api/v1/debate/start?topic_id=${data.id}`, { method: 'POST' });
      const startData = await startRes.json();
      
      router.push(`/room/${startData.session_id}`);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gradient-to-br from-background to-muted/20">
      <Card className="w-full max-w-lg bg-card/50 backdrop-blur-sm border-white/10">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl">Propose a Topic</CardTitle>
          <CardDescription>What shall the Adda discuss today?</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <Input 
              placeholder="e.g., Should Artificial Intelligence replace teachers?" 
              value={title} 
              onChange={e => setTitle(e.target.value)} 
              required 
              className="h-12 text-lg"
            />
            <Button type="submit" size="lg" disabled={isLoading} className="w-full">
              {isLoading ? "Preparing the Adda Room..." : "Begin the Adda"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
