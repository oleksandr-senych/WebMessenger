import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

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
      const res = await fetch("http://localhost:8000/api/chats/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error(`Error ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
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
      const res = await fetch("http://localhost:8000/api/chats/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ other_username: otherUsername }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Failed to create chat");
      }

      await fetchChats();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Your Chats</h1>
      <button onClick={handleCreateChat}>Create Chat</button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {chats.map((chat) => (
          <li key={chat.id}>
            {chat.username1 === username ? chat.username2 : chat.username1}
          </li>
        ))}
      </ul>
    </div>
  );
}
