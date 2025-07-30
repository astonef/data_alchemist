import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { MongoDBAdapter } from "@next-auth/mongodb-adapter";
import clientPromise from "@/lib/mongo";
import { compare } from "bcryptjs";

const handler = NextAuth({
  adapter: MongoDBAdapter(clientPromise),
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials) {
          console.warn("❌ Credenziali mancanti");
          throw new Error("Credenziali mancanti");
        }

        console.log("🧪 Tentativo login:", credentials);

        const client = await clientPromise;
        const user = await client
          .db("users")
          .collection("users")
          .findOne({ username: credentials.username });

        console.log("🧪 Utente trovato:", user);

        if (!user) {
          console.warn("❌ Utente non trovato");
          throw new Error("Credenziali errate"); // ❗ messaggio generico
        }

        const isValid = await compare(credentials.password, user.password);

        console.log("🧪 Password valida?", isValid);

        if (!isValid) {
          console.warn("❌ Password errata");
          throw new Error("Credenziali errate"); // ❗ messaggio generico
        }

        console.log("✅ Login riuscito");
        return {
          id: user._id.toString(),
          name: user.name,
          email: user.email,
        };
      },
    }),
  ],
  session: { strategy: "jwt" },
  pages: { signIn: "/login" },
  secret: process.env.NEXTAUTH_SECRET,
});

export { handler as GET, handler as POST };
