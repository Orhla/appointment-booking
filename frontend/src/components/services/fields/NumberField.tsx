import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type NumberFieldProps = {
  id: string;
  label: string;
  hint?: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  step: string | number;
  required: boolean;
};

export function NumberField({
  id,
  label,
  hint,
  value,
  onChange,
  min = 0,
  step = 1,
  required = false,
}: NumberFieldProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id}>
        {label} {hint && <span className="text-muted-foreground">{hint}</span>}
      </Label>
      <Input
        id={id}
        type="number"
        min={min}
        step={step}
        value={value || ""}
        onChange={(e) => {
          const parsed = e.target.valueAsNumber;
          onChange(Number.isNaN(parsed) ? 0 : parsed);
        }}
        required={required}
      />
    </div>
  );
}
