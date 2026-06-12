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
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    console.log("[handleSubmit] Starting topic submission flow");
    console.log("[handleSubmit] process.env.NEXT_PUBLIC_API_URL:", process.env.NEXT_PUBLIC_API_URL);
    console.log("[handleSubmit] Selected apiBaseUrl:", apiBaseUrl);

    try {
      const topicUrl = `${apiBaseUrl}/api/v1/topics/`;
      console.log("[handleSubmit] POST Request to:", topicUrl);
      console.log("[handleSubmit] Payload:", { title, description: '' });

      const res = await fetch(topicUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description: '' })
      });
      
      console.log("[handleSubmit] POST /topics/ Response Status:", res.status, res.statusText);
      const data = await res.json();
      console.log("[handleSubmit] POST /topics/ Response Data:", data);
      
      const startUrl = `${apiBaseUrl}/api/v1/debate/start?topic_id=${data.id}`;
      console.log("[handleSubmit] POST Request to:", startUrl);

      const startRes = await fetch(startUrl, { method: 'POST' });
      console.log("[handleSubmit] POST /debate/start Response Status:", startRes.status, startRes.statusText);
      const startData = await startRes.json();
      console.log("[handleSubmit] POST /debate/start Response Data:", startData);
      
      console.log("[handleSubmit] Redirecting to room:", startData.session_id);
      router.push(`/room/${startData.session_id}`);
    } catch (error) {
      console.error("[handleSubmit] Error occurred during fetch flow:", error);
      if (error instanceof TypeError) {
        console.error("[handleSubmit] TypeError Details: Check CORS configuration on backend or ensure NEXT_PUBLIC_API_URL is configured and built correctly in Cloudflare Pages dashboard.");
      }
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
