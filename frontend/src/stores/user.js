import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isLoggedIn = ref(!!token.value)

  function setLoginState(userData, userToken) {
    currentUser.value = userData
    token.value = userToken
    isLoggedIn.value = true
    localStorage.setItem('token', userToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  function logout() {
    currentUser.value = null
    token.value = null
    isLoggedIn.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  function initFromStorage() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    if (savedToken && savedUser) {
      token.value = savedToken
      currentUser.value = JSON.parse(savedUser)
      isLoggedIn.value = true
    }
  }

  return {
    currentUser,
    token,
    isLoggedIn,
    setLoginState,
    logout,
    initFromStorage
  }
})
