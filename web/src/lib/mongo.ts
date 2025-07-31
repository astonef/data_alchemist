// src/lib/mongo.ts

import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI!;
const options = {};

declare global {
  // Garantisce che il client sia singleton anche in sviluppo
  var _mongoClientPromise: Promise<MongoClient> | undefined;
}

let client: MongoClient;
const clientPromise: Promise<MongoClient> =
  global._mongoClientPromise ??
  (() => {
    client = new MongoClient(uri, options);
    global._mongoClientPromise = client.connect();
    return global._mongoClientPromise;
  })();

export default clientPromise;
