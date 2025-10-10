interface CreateChatButtonProps {
  onClick: () => void;
  loading?: boolean;
}

export default function CreateChatButton({
  onClick,
  loading,
}: CreateChatButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500
                 bg-blue-500 text-white hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {loading ? "Creating..." : "Create Chat"}
    </button>
  );
}
