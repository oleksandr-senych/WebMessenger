import type { FormEvent } from "react";

interface Field {
  name: string;
  label: string;
  type: string;
  value: string;
  placeholder?: string;
}

interface AuthFormProps {
  fields: Field[];
  onChange: (name: string, value: string) => void;
  onSubmit: (e: FormEvent) => void;
  children?: React.ReactNode;
}

export default function AuthForm({
  fields,
  onChange,
  onSubmit,
  children,
}: AuthFormProps) {
  return (
    <form className="space-y-4" onSubmit={onSubmit}>
      {fields.map((field) => (
        <div key={field.name}>
          <label className="block text-sm font-medium mb-1">
            {field.label}
          </label>
          <input
            type={field.type}
            value={field.value}
            onChange={(e) => onChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      ))}
      {children}
    </form>
  );
}
