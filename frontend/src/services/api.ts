import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export const api = {
  users: {
    getXp: async (username: string) => {
      const res = await axios.get(`${BACKEND_URL}/users/${username}/xp`)
      return res.data
    },
    purchaseUpgrade: async (username: string, upgrade: string) => {
      const res = await axios.post(`${BACKEND_URL}/users/${username}/upgrades/${upgrade}`)
      return res.data
    },
    rebirth: async (username: string) => {
      const res = await axios.post(`${BACKEND_URL}/users/${username}/rebirth`)
      return res.data
    }
  },
  tasks: {
    create: async (username: string, title: string, duration: number) => {
      const res = await axios.post(`${BACKEND_URL}/tasks`, {
        username,
        title,
        durationMin: duration
      })
      return res.data
    },
    complete: async (taskId: string, username: string) => {
      const res = await axios.post(`${BACKEND_URL}/tasks/${taskId}/complete`, {
        username
      })
      return res.data
    },
    autofit: async (username: string) => {
      const res = await axios.post(`${BACKEND_URL}/tasks/autofit`, {
        username
      })
      return res.data
    }
  }
}
