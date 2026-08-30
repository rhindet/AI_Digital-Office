import { api } from "../../../core/api/axios";


export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
}

export async function getUsers(): Promise<User[]> {
  const response = await api.get<User[]>("/users/");
  return response.data;
}



export async function assignTicket(
  ticketId: number,
  userId: number
): Promise<Ticket> {
  const response = await api.patch<Ticket>(
    `/tickets/${ticketId}/assign`,
    {
      user_id: userId,
    }
  );

  return response.data;
}


export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  created_by: number;
  assigned_to: number | null;
}

export interface CreateTicketRequest {
  title: string;
  description: string;
  priority: string;
}

export type TicketStatus =
  | "open"
  | "in_progress"
  | "resolved"
  | "closed";

export async function updateTicketStatus(
  ticketId: number,
  status: TicketStatus
): Promise<Ticket> {
  const response = await api.patch<Ticket>(
    `/tickets/${ticketId}/status`,
    {
      status,
    }
  );

  return response.data;
}

export interface UpdateTicketRequest {
  title?: string;
  description?: string;
  status?: "open" | "in_progress" | "resolved" | "closed";
  priority?: string;
}

export async function getTickets(): Promise<Ticket[]> {
  const response = await api.get<Ticket[]>("/tickets/");
  return response.data;
}

export async function getTicket(
  ticketId: number
): Promise<Ticket> {
  const response = await api.get<Ticket>(
    `/tickets/${ticketId}`
  );

  return response.data;
}

export async function createTicket(
  data: CreateTicketRequest
): Promise<Ticket> {
  const response = await api.post<Ticket>(
    "/tickets/",
    data
  );

  return response.data;
}

export async function updateTicket(
  ticketId: number,
  data: UpdateTicketRequest
): Promise<Ticket> {
  const response = await api.patch<Ticket>(
    `/tickets/${ticketId}`,
    data
  );

  return response.data;
}

export async function deleteTicket(
  ticketId: number
): Promise<void> {
  await api.delete(`/tickets/${ticketId}`);
}