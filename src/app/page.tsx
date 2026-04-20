import Link from 'next/link'
import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'

export default async function Home() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  async function signOut() {
    'use server'
    const supabase = await createClient()
    await supabase.auth.signOut()
    redirect('/login')
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm flex flex-col gap-8">
        <h1 className="text-4xl font-bold text-center">
          🗳️ Pool Élections Québec 2026
        </h1>
        
        {user ? (
          <div className="flex flex-col items-center gap-4">
            <p className="text-xl text-center">
              Bonjour, <span className="font-bold text-blue-600">{user.email}</span> !
            </p>
            <div className="flex gap-4">
              <Link
                href="/predictions"
                className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-blue-600 text-white gap-2 hover:bg-blue-700 text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
              >
                Mes Prédictions
              </Link>
              <form action={signOut}>
                <button className="rounded-full border border-solid border-gray-300 transition-colors flex items-center justify-center hover:bg-gray-100 text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5">
                  Déconnexion
                </button>
              </form>
            </div>
          </div>
        ) : (
          <>
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
            </div>
          </>
        )}
      </div>
    </main>
  )
}
