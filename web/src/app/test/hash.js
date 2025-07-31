import { hash } from "bcryptjs";

(async () => {
  const hashed = await hash("test", 10);
  console.log(hashed);
})();
