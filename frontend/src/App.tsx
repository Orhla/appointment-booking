import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { createService, fetchServices } from "@/api/services";
import type { ServiceCreate } from "@/api/services";

export default function App() {
  const qc = useQueryClient();

  const { data: services, isLoading } = useQuery({
    queryKey: ["services"],
    queryFn: fetchServices,
  });

  const mutation = useMutation({
    mutationFn: createService,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["services"] });
      setForm({ name: "", duration_min: 60, price: 0 });
    },
  });

  const [form, setForm] = useState<ServiceCreate>({
    name: "",
    duration_min: 60,
    price: 0,
  });

  function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    mutation.mutate(form);
  }

  if (isLoading) return <p className="p-6 text-gray-600">Загрузка...</p>;

  return (
    <div className="p-6 max-w-2xl mx-auto font-sans">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Услуги</h1>

      {services && services.length > 0 ? (
        <ul className="space-y-3 mb-8">
          {services.map((service) => (
            <li
              key={service.id}
              className="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm"
            >
              <span className="font-semibold text-lg text-gray-700">
                {service.name}
              </span>
              <div className="text-sm text-gray-500 mt-1">
                Длительность:{" "}
                {new Intl.NumberFormat("ru-RU", {
                  style: "unit",
                  unit: "minute",
                }).format(service.duration_min)}{" "}
                | Цена:{" "}
                <span className="text-blue-600 font-medium">
                  {new Intl.NumberFormat("ru-RU", {
                    style: "currency",
                    currency: "RUB",
                  }).format(service.price)}
                </span>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 mb-8">Список услуг пока пуст.</p>
      )}

      <h2>Добавить услугу</h2>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 max-w-xs bg-white p-6 rounded-lg shadow-md"
      >
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Название:
          </label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
            className="w-full border border-gray-300 rounded px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Длительность (мин):
          </label>
          <input
            type="number"
            value={form.duration_min}
            onChange={(e) =>
              setForm({ ...form, duration_min: Number(e.target.value) })
            }
            min={1}
            required
            className="w-full border border-gray-300 rounded px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Цена:{" "}
            {form.price ? `${form.price.toLocaleString("ru-RU")} руб.` : ""}
          </label>
          <input
            type="number"
            value={form.price || ""}
            onChange={(e) =>
              setForm({ ...form, price: e.target.valueAsNumber })
            }
            min={0}
            step="0.01"
            required
            className="w-full border border-gray-300 rounded px-3 py-1.5 focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={mutation.isPending}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded disabled:bg-gray-400 transition"
        >
          {mutation.isPending ? "Добавление..." : "Добавить"}
        </button>
      </form>
    </div>
  );
}
