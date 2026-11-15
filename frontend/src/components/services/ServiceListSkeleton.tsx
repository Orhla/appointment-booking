import { Skeleton } from "@/components/ui/skeleton";

export function ServiceListSkeleton() {
  return (
    <div className="space-y-3 mb-8">
      {Array.from({ length: 3 }).map((_, index) => (
        <Skeleton key={index} className="h-24 w-full rounded-xl" />
      ))}
    </div>
  );
}
