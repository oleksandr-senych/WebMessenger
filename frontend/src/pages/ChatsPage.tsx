import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { createChat, getChats } from "../api/chats";

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
  const [error, setError] = useState<string | null>(null);
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
      const data = await getChats(token);
      setChats(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChat = async () => {
    const otherUsername = prompt("Enter username of the person to chat with:");
    if (!otherUsername) return;

    try {
      await createChat({ other_username: otherUsername }, token);
      await fetchChats(); // Refresh chats list
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1 className="bg-red-200">Your Chats</h1>
      <button onClick={handleCreateChat}>Create Chat</button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {chats.map((chat)  => (
          <Link key={chat.id}
            to={`/chats/${chat.id}`}
          >
            {chat.username1 === username ? chat.username2 : chat.username1}
          </Link>
        ))}
      </ul>
    </div>
  );
}
