import axios from "axios";
import type { Service } from "@/lib/types";

const api = axios.create({ baseURL: "http://localhost:8000" });

export type ServiceCreate = Omit<Service, "id">;

export async function fetchServices(): Promise<Service[]> {
  const response = await api.get<Service[]>(`/services/`);
  return response.data;
}

export async function createService(data: ServiceCreate): Promise<Service> {
  const response = await api.post<Service>("/services/", data);
  return response.data;
}
