import { useId } from "react";
import { cn } from "../../lib/utils";

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
}

export default function Select({
  label,
  error,
  className,
  children,
  ...props
}: SelectProps) {
  const generatedId = useId();
  const id = props.id || generatedId;
  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={id}
          className="block text-sm font-medium text-gray-300 mb-1"
        >
          {label}
        </label>
      )}
      <select
        id={id}
        aria-label={
          props["aria-label"] ||
          label ||
          ("placeholder" in props ? String(props.placeholder || "") : undefined)
        }
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        className={cn(
          "w-full px-3 py-2 bg-surfaceLight border border-gray-600 rounded-lg text-gray-100",
          "focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          error && "border-danger",
          className,
        )}
        {...props}
      >
        {children}
      </select>
      {error && (
        <p id={`${id}-error`} role="alert" className="mt-1 text-sm text-danger">
          {error}
        </p>
      )}
    </div>
  );
}
