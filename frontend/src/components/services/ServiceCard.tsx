import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Service } from "@/lib/types";

type ServiceCardProps = {
  service: Service;
};

export function ServiceCard({ service }: ServiceCardProps) {
  const formattedDuration = new Intl.NumberFormat("ru-RU", {
    style: "unit",
    unit: "minute",
  }).format(service.duration_min);

  const formattedPrice = new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
  }).format(service.price);

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between gap-2">
          <CardTitle className="text-lg">{service.name}</CardTitle>
          <Badge variant="secondary" className="text-sm font-medium">
            {formattedPrice}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">
          Длительность: {formattedDuration}
        </p>
      </CardContent>
    </Card>
  );
}
