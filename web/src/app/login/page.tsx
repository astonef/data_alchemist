'use client'

import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

import { signIn } from "next-auth/react"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const res = await signIn("credentials", {
      redirect: false,
      username,
      password,
    })

    if (res?.ok) {
      router.push("/dashboard")
    } else {
      alert("Login fallito 😬")
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-background text-foreground">
  <div className="w-[360px] rounded-xl border-[3px] border-[#8BE9FD] bg-[#44475a] shadow-lg">
    <Card className="bg-transparent border-none">
      <CardContent className="p-6 space-y-4">
        <div className="flex justify-center">
          <Avatar className="w-16 h-16 border-2 border-[#F1FA8C] shadow-md">
            <AvatarImage
              src="https://cdn.jsdelivr.net/gh/astonef/fstfd-cdn@core/images/20250729_140527.jpg"
              alt="Avatar"
            />
            <AvatarFallback>U</AvatarFallback>
          </Avatar>
        </div>
        <h2 className="text-xl font-bold text-center text-[#8BE9FD]">
          Data Alchemist
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="bg-[#282a36] text-[#8BE9FD] placeholder:text-[#ff79c6]"
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-[#282a36] text-[#8BE9FD] placeholder:text-[#ff79c6]"
          />
          <Button
            className="w-full bg-[#F1FA8C] text-black hover:bg-[#50FA7B] transition-colors"
            type="submit"
          >
            Entra
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</div>

  )
}
