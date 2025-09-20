import { useMemo } from 'react'

export function useSfx(){
  const kaching = useMemo(()=>{
    const audio = new Audio('/sfx/kaching.mp3')
    audio.preload = 'auto'
    return audio
  },[])

  function playKaching(){
    try{ kaching.currentTime = 0; kaching.play() }catch{}
  }

  return { playKaching }
}



