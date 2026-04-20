import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm flex flex-col gap-8">
        <h1 className="text-4xl font-bold text-center">
          🗳️ Pool Élections Québec 2026
        </h1>
        <p className="text-xl text-center max-w-2xl">
          Bienvenue sur la plateforme de prédiction interactive. Networking, compétition amicale et analyses en temps réel.
        </p>
        <div className="flex gap-4">
          <Link
            href="/login"
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          >
            Se connecter
          </Link>
          <Link
            href="/predictions"
            className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
          >
            Voir les prédictions
          </Link>
        </div>
      </div>
    </main>
  )
}
