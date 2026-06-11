import Link from 'next/link';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 lg:p-24 bg-gradient-to-br from-background via-background to-muted/20 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="z-10 text-center space-y-8 max-w-3xl mt-12">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/60">
          AddaAI
        </h1>
        <p className="text-xl md:text-2xl text-muted-foreground font-light leading-relaxed">
          Reviving Bengal&apos;s legendary intellectual Adda culture. Step into a virtual roundtable with Tagore, Ray, and Bose.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
          <Link href="/topic-submission" className={buttonVariants({ size: "lg", className: "rounded-full px-8 text-lg w-full sm:w-auto h-14" })}>
            Start a New Adda
          </Link>
          <Link href="/history" className={buttonVariants({ size: "lg", variant: "outline", className: "rounded-full px-8 text-lg w-full sm:w-auto h-14" })}>
            View Past Debates
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-24 z-10 w-full max-w-5xl">
        <Card className="bg-card/50 backdrop-blur-sm border-white/10 hover:bg-card/80 transition-colors">
          <CardHeader>
            <CardTitle>Rabindranath Tagore</CardTitle>
            <CardDescription>The Poet & Philosopher</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Provides a broad, universal perspective blending humanism with spirituality.
          </CardContent>
        </Card>
        <Card className="bg-card/50 backdrop-blur-sm border-white/10 hover:bg-card/80 transition-colors">
          <CardHeader>
            <CardTitle>Satyajit Ray</CardTitle>
            <CardDescription>The Maestro</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Brings sharp analytical insight, focusing on aesthetics, realism, and critique.
          </CardContent>
        </Card>
        <Card className="bg-card/50 backdrop-blur-sm border-white/10 hover:bg-card/80 transition-colors">
          <CardHeader>
            <CardTitle>Subhas Chandra Bose</CardTitle>
            <CardDescription>The Leader</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Offers pragmatic, action-oriented arguments driven by intense patriotic fervor.
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
