import { useQuery } from "@tanstack/react-query";
import { fetchServices } from "@/api/services";
import { CreateServiceForm } from "@/components/services/CreateServiceForm";
import { ServiceList } from "@/components/services/ServiceList";
import { ServiceListSkeleton } from "@/components/services/ServiceListSkeleton";

export default function App() {
  const { data: services, isLoading } = useQuery({
    queryKey: ["services"],
    queryFn: fetchServices,
  });

  return (
    <main className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold tracking-tight mb-6">Услуги</h1>

      {isLoading ? (
        <ServiceListSkeleton />
      ) : (
        <ServiceList services={services} />
      )}

      <CreateServiceForm />
    </main>
  );
}
