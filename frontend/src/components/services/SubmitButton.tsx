import { Button } from "@/components/ui/button";

type SubmitButtonProps = {
  isPending: boolean;
  idleText: string;
  pendingText: string;
};

export function SubmitButton({
  isPending,
  idleText = "Добавить",
  pendingText = "Добавление...",
}: SubmitButtonProps) {
  return (
    <Button type="submit" disabled={isPending} className="w-full">
      {isPending ? pendingText : idleText}
    </Button>
  );
}
