import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { getMessages, createMessage, type Message } from "../api/messages";
import { useAuth } from "../context/AuthContext";

export default function MessagesPage() {
  const { chatId } = useParams<{ chatId: string }>();
  const { username, token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMessages = async () => {
    setLoading(true);
    try {
      if (!chatId) throw new Error("No chat ID provided");
      const data = await getMessages(Number(chatId), token);
      setMessages(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      await createMessage({ chat_id: Number(chatId), text: newMessage }, token);
      setNewMessage("");
      await fetchMessages();
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, [chatId]);

  if (loading) return <div>Loading messages...</div>;
  if (error) return <div>Error: {error}</div>;

  
  return (
    <div>
      <h2>Chat Messages</h2>
      <div>
        {messages.length === 0 ? (
          <div>No messages yet</div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id}>
              <strong>{msg.username}:</strong>{" "}
              {msg.text}
              <div>{msg.created_at}</div>
            </div>
          ))
        )}
      </div>

      <div>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}
