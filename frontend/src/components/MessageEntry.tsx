

interface MessageEntryProps {
  username: string|null;
  text: string;
  createdAt: string;
  isOwn: boolean; // whether message was sent by current user
}

export default function MessageEntry({ username, text, createdAt, isOwn }: MessageEntryProps) {
  return (
    <div
      className={`mb-3 p-2 rounded-lg border ${
        isOwn
          ? "bg-blue-100 border-blue-300 self-end text-right"
          : "bg-gray-50 border-gray-200 text-left"
      }`}
    >
      <div className="text-sm text-gray-700">
        <strong className="text-blue-600">{username}</strong>: {text}
      </div>
      <div className="text-xs text-gray-400">{createdAt}</div>
    </div>
  );
}