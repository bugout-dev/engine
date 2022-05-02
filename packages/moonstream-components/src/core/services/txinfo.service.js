import { http } from "../utils";

const API = process.env.NEXT_PUBLIC_ENGINE_API_URL;

export const getTxInfo = (tx) =>
  http({
    method: "POST",
    url: `${API}/txinfo/ethereum_blockchain`,
    data: tx,
  });
