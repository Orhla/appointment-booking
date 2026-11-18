import type { Service } from "@/lib/types";
import { ServiceCard } from "@/components/services/ServiceCard";

type ServiceListProps = {
  services?: Service[];
};

export function ServiceList({ services }: ServiceListProps) {
  if (!services || services.length === 0) {
    return (
      <p className="text-muted-foreground mb-8">Список услуг пока пуст.</p>
    );
  }

  return (
    <ul className="space-y-3 mb-8">
      {services.map((service) => (
        <li key={service.id}>
          <ServiceCard service={service} />
        </li>
      ))}
    </ul>
  );
}
