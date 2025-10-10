import { Link } from "react-router-dom";

interface ChatEntryProps {
  chatId: number;
  name: string;
}

export default function ChatEntry({ chatId, name }: ChatEntryProps) {
  return (
    <li className="border border-gray-300 rounded px-3 py-2 hover:bg-gray-100 focus-within:ring-2 focus-within:ring-blue-500 transition-all">
      <Link
        to={`/chats/${chatId}`}
        className="block w-full text-gray-800 font-medium hover:text-blue-600"
      >
        {name}
      </Link>
    </li>
  );
}
