import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getMessages, createMessage, type Message } from "../api/messages";
import { useAuth } from "../context/AuthContext";
import toast from "react-hot-toast";
import MessageEntry from "../components/MessageEntry";

export default function MessagesPage() {
  const { chatId } = useParams<{ chatId: string }>();
  const {username, token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");

  const fetchMessages = async () => {
    try {
      if (!chatId) throw new Error("No chat ID provided");
      const data = await getMessages(Number(chatId), token);
      setMessages(data);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      await createMessage({ chat_id: Number(chatId), text: newMessage }, token);
      setNewMessage("");
      await fetchMessages();
    } catch (err: any) {
      toast.error(err.message);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, [chatId]);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">
        Chat Messages
      </h2>

      <div className="border border-gray-300 rounded-lg p-4 h-96 overflow-y-auto bg-white shadow-sm flex flex-col">
        {messages.length === 0 ? (
          <div className="text-gray-500 text-center">No messages yet</div>
        ) : (
          messages.map((msg) => (
            <MessageEntry
              key={msg.id}
              username={msg.username}
              text={msg.text}
              createdAt={msg.created_at}
              isOwn={msg.username === username}
            />
          ))
        )}
      </div>

      <div className="mt-4 flex gap-2">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Send
        </button>
      </div>
    </div>
  );
}
