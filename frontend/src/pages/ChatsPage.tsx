import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { createChat, getChats } from "../api/chats";
import toast from "react-hot-toast";
import CreateChatButton from "../components/CreateChatButton";
import ChatEntry from "../components/ChatEntry";

interface Chat {
  id: number;
  username1: string;
  username2: string;
  user_id1: number;
  user_id2: number;
}

export default function ChatsPage() {
  const { token, username } = useAuth();
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token || !username) {
      navigate("/login");
      return;
    }

    fetchChats();
  }, [token, username]);

  const fetchChats = async () => {
    setLoading(true);
    try {
      await toast.promise(getChats(token).then(setChats), {
        loading: "Loading your chats...",
        success: "Chats loaded!",
        error: "Failed to fetch chats",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChat = async () => {
    const otherUsername = prompt("Enter username of the person to chat with:");
    if (!otherUsername) return;

    await toast.promise(
      createChat({ other_username: otherUsername }, token).then(() =>
        fetchChats()
      ),
      {
        loading: "Creating chat...",
        success: `Chat with ${otherUsername} created!`,
        error: (err) =>
          typeof err === "string"
            ? err
            : err?.message || "Failed to create chat",
      }
    );
  };

  return (
    <div className="max-w-lg mx-auto mt-10 space-y-4">
      <h1 className="text-2xl font-bold text-center mb-4">Your Chats</h1>
      <CreateChatButton onClick={handleCreateChat} loading={loading} />

      <ul className="space-y-2">
        {chats.map((chat) => (
          <ChatEntry
            key={chat.id}
            chatId={chat.id}
            name={chat.username1 === username ? chat.username2 : chat.username1}
          />
        ))}
      </ul>
    </div>
  );
}
