import { Link } from "react-router-dom";

interface NavButtonProps {
  label: string;
  to: string;
  disabled?: boolean;
}

export default function NavButton({ label, to, disabled }: NavButtonProps) {
  return (
    <Link
      to={disabled ? "#" : to}
      className={`px-4 py-2 rounded-md text-white font-medium transition
        ${
          disabled
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-400"
        }`}
    >
      {label}
    </Link>
  );
}
