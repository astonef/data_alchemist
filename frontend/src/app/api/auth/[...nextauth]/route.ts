import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { MongoDBAdapter } from "@next-auth/mongodb-adapter";
import clientPromise from "@/lib/mongo";
import { compare } from "bcrypt";

const handler = NextAuth({
  adapter: MongoDBAdapter(clientPromise),
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: { username: {}, password: {} },
      async authorize(credentials) {
        const client = await clientPromise;
        const user = await client
          .db()
          .collection("users")
          .findOne({ username: credentials.username });

        if (!user) throw new Error("Utente non trovato");

        const isValid = await compare(credentials.password, user.password);
        if (!isValid) throw new Error("Password errata");

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
});

export { handler as GET, handler as POST };
