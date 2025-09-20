import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Upload calendar
async function handleUpload(file: File, userId: string) {
  const result = await api.tasks.calendar.upload(userId, file)
  console.log(result.message, result.events_count)
}

// Fetch events
async function fetchEvents(userId: string) {
  const events = await api.tasks.calendar.fetch(userId)
  console.log(events)
}

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
    },
    calendar: {
      upload: async (userId: string, file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const res = await axios.post(`${BACKEND_URL}/calendar/${userId}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        return res.data;
      },
      fetch: async (userId: string) => {
        const res = await axios.get(`${BACKEND_URL}/calendar/${userId}`);
        return res.data;
      }
    }
  }
}



