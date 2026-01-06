"use client"
import { useState, useEffect } from "react"

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    // ตั้งเวลาหน่วง (Timer)
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    // ล้างเวลาเก่าทิ้ง (Cleanup) เมื่อ value เปลี่ยนก่อนที่จะครบเวลา
    // นี่คือหัวใจของ Debounce: ถ้าพิมพ์รัวๆ timer เก่าจะถูกยกเลิกตลอดเวลา
    return () => {
      clearTimeout(timer)
    }
  }, [value, delay])

  return debouncedValue
}