import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createService } from "@/api/services";
import type { ServiceCreate } from "@/api/services";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { NumberField } from "./fields/NumberField";
import { TextField } from "./fields/TextField";
import { SubmitButton } from "./SubmitButton";

const INITIAL_FORM_STATE: ServiceCreate = {
  name: "",
  duration_min: 60,
  price: 0,
};

export function CreateServiceForm() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState<ServiceCreate>(INITIAL_FORM_STATE);

  const mutation = useMutation({
    mutationFn: createService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["services"] });
      setForm(INITIAL_FORM_STATE);
    },
  });

  function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    mutation.mutate(form);
  }

  const priceHint = form.price
    ? `(${form.price.toLocaleString("ru-RU")} руб.)`
    : undefined;

  return (
    <Card className="max-w-sm">
      <CardHeader>
        <CardTitle className="text-xl">Добавить услугу</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <TextField
            id="service-name"
            label="Название"
            placeholder="Например, стрижка"
            value={form.name}
            onChange={(name) => setForm({ ...form, name })}
            required
          />

          <NumberField
            id="service-duration"
            label="Длительность (мин)"
            min={1}
            step={1}
            value={form.duration_min}
            onChange={(duration_min) => setForm({ ...form, duration_min })}
            required
          />

          <NumberField
            id="service-price"
            label="Цена"
            hint={priceHint}
            min={0}
            step="0.01"
            value={form.price}
            onChange={(price) => setForm({ ...form, price })}
            required
          />

          <SubmitButton
            isPending={mutation.isPending}
            idleText="Добавить"
            pendingText="Добавление..."
          />
        </form>
      </CardContent>
    </Card>
  );
}
