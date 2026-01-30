import type { AnalyzeResponse } from '../types'

const API_BASE = import.meta.env.VITE_API_URL ?? ''

export async function analyzeTranscription(transcription: string): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transcription }),
  })
  if (!res.ok) {
    const body = (await res.json().catch(() => ({}))) as { detail?: string | unknown[] }
    const d = body.detail
    const msg = Array.isArray(d)
      ? d.map((x) => (typeof x === 'object' && x && 'msg' in x ? String((x as { msg: unknown }).msg) : String(x))).join(' ; ')
      : (d != null ? String(d) : res.statusText)
    throw new Error(msg || res.statusText)
  }
  return res.json() as Promise<AnalyzeResponse>
}
