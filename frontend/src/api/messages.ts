const API_BASE_URL = import.meta.env.VITE_API_URL;

export interface Message {
  id: number;
  chat_id: number;
  user_id: number;
  username: string | null;
  text: string;
  created_at: string;
}

export interface CreateMessagePayload {
  chat_id: number;
  text: string;
}

/**
 * Fetch all messages for a given chat
 */
export async function getMessages(
  chatId: number,
  token: string | null
): Promise<Message[]> {
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/messages/${chatId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch messages: ${response.status} - ${errorText}`
    );
  }

  return await response.json();
}

/**
 * Create a new message
 */
export async function createMessage(
  payload: CreateMessagePayload,
  token: string | null
): Promise<Message> {
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`${API_BASE_URL}/messages/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to create message: ${response.status} - ${errorText}`
    );
  }

  return await response.json();
}
