import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat API
export const sendMessage = async (data: { user_id: number; message: string; conversation_id?: number }) => {
  const response = await api.post('/chat', data)
  return response.data
}

export const getChatHistory = async (userId: number) => {
  const response = await api.get(`/chat/history/${userId}`)
  return response.data
}

// Documents API
export const uploadDocument = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/documents/ingest', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const listDocuments = async () => {
  const response = await api.get('/documents')
  return response.data
}

export const deleteDocument = async (documentId: number) => {
  const response = await api.delete(`/documents/${documentId}`)
  return response.data
}

// Conversations API
export const getUserConversations = async (userId: number) => {
  const response = await api.get(`/conversations/${userId}`)
  return response.data
}

export const getConversationMessages = async (conversationId: number) => {
  const response = await api.get(`/conversations/${conversationId}/messages`)
  return response.data
}

export const deleteConversation = async (conversationId: number) => {
  const response = await api.delete(`/conversations/${conversationId}`)
  return response.data
}

export const updateConversationTitle = async (conversationId: number, title: string) => {
  const response = await api.put(`/conversations/${conversationId}/title`, { title })
  return response.data
}

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api
