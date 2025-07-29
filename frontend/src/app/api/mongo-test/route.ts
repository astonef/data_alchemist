import { NextResponse } from "next/server"
import clientPromise from "@/lib/mongo"

export async function GET() {
  try {
    const client = await clientPromise
    const db = client.db("users") // se vuoi specifico: client.db("nome-db")
    const users = await db.collection("users").find({}).limit(5).toArray()

    return NextResponse.json({ ok: true, users })
  } catch (err) {
    console.error("Errore connessione Mongo:", err)
    return NextResponse.json({ ok: false, error: err }, { status: 500 })
  }
}
