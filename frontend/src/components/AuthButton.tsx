export default function AuthButton({ label }: { label: string }) {
  return (
    <button
      type="submit"
      className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
    >
      {label}
    </button>
  );
}
