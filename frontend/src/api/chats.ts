const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export interface Chat {
  id: number;
  user_id1: number;
  user_id2: number;
  username1: string;
  username2: string;
}

export interface CreateChatPayload {
  username2: string; // the user to start chat with
}

/**
 * Fetch all chats for the current logged-in user
 */
export async function getChats(): Promise<Chat[]> {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/chats/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to fetch chats: ${response.status} - ${errorText}`);
  }

  return await response.json();
}

/**
 * Create a new chat with another user
 */
export async function createChat(payload: CreateChatPayload): Promise<Chat> {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/chats/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to create chat: ${response.status} - ${errorText}`);
  }

  return await response.json();
}