import { createFileRoute } from '@tanstack/react-router'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useEffect, useRef, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { getDetectionStateOptions, resetCountOptions, detectCards, type DetectedCardDTO } from '@/api'
import { toast } from 'sonner'
import { AxiosError } from 'axios'
import { getErrorMessage, type ServerError } from '@/services/apiClient'

export const Route = createFileRoute('/')({
  component: CardDetectionPage,
})

function CardDetectionPage() {
  const queryClient = useQueryClient()
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [detectedCards, setDetectedCards] = useState<DetectedCardDTO[]>([])
  const [sseState, setSSEState] = useState<{ running_count: number; total_cards_detected: number }>({
    running_count: 0,
    total_cards_detected: 0,
  })

  // Query for detection state
  const { data: stateData } = useQuery(getDetectionStateOptions())

  // Reset mutation
  const resetMutation = useMutation({
    ...resetCountOptions(queryClient),
    onMutate: () => {
      toast.dismiss()
      toast.loading('Resetting count...')
    },
    onSuccess: () => {
      toast.dismiss()
      toast.success('Count reset successfully!')
      setDetectedCards([])
      setSSEState({ running_count: 0, total_cards_detected: 0 })
    },
    onError: (error: AxiosError<ServerError>) => {
      toast.dismiss()
      const { message, description } = getErrorMessage(error)
      toast.error(message, { description })
    },
  })

  // Start webcam
  useEffect(() => {
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480 },
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          setIsStreaming(true)
        }
      } catch (error) {
        toast.error('Failed to access webcam', {
          description: 'Please ensure camera permissions are granted',
        })
      }
    }

    startWebcam()

    return () => {
      // Cleanup: stop all tracks
      if (videoRef.current?.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream
        stream.getTracks().forEach((track) => track.stop())
      }
    }
  }, [])

  // SSE connection for real-time updates
  useEffect(() => {
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const eventSource = new EventSource(`${API_BASE_URL}/api/stream`)

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'state_update') {
          setSSEState({
            running_count: data.running_count,
            total_cards_detected: data.total_cards_detected,
          })
        }
      } catch (error) {
        console.error('Error parsing SSE message:', error)
      }
    }

    eventSource.onerror = () => {
      console.error('SSE connection error')
      eventSource.close()
    }

    return () => {
      eventSource.close()
    }
  }, [])

  // Capture frame and detect
  const captureAndDetect = async () => {
    if (!videoRef.current || !canvasRef.current) return

    const video = videoRef.current
    const canvas = canvasRef.current

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    // Draw video frame to canvas
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      if (!blob) return

      try {
        const file = new File([blob], 'frame.jpg', { type: 'image/jpeg' })
        const result = await detectCards(file)
        setDetectedCards(result.cards)

        if (result.cards.length > 0) {
          toast.success(`Detected ${result.cards.length} card(s)`)
        }
      } catch (error) {
        const axiosError = error as AxiosError<ServerError>
        const { message } = getErrorMessage(axiosError)
        toast.error('Detection failed', { description: message })
      }
    }, 'image/jpeg')
  }

  return (
    <div className="container mx-auto p-4 max-w-7xl">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-2">Card Detection System</h1>
        <p className="text-muted-foreground">Real-time playing card detection with Hi-Lo counting</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Video Feed */}
        <Card>
          <CardHeader>
            <CardTitle>Live Camera Feed</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="relative aspect-video bg-muted rounded-lg overflow-hidden">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-full object-cover"
              />
              <canvas ref={canvasRef} className="hidden" />
              {!isStreaming && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <p className="text-muted-foreground">Starting camera...</p>
                </div>
              )}
            </div>
            <div className="flex gap-2">
              <Button onClick={captureAndDetect} disabled={!isStreaming} className="flex-1">
                Detect Cards
              </Button>
              <Button
                variant="outline"
                onClick={() => resetMutation.mutate()}
                disabled={resetMutation.isPending}
              >
                Reset Count
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Detection Results */}
        <Card>
          <CardHeader>
            <CardTitle>Detection Results</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Running Count */}
            <div className="text-center p-6 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Running Count</p>
              <p className="text-6xl font-bold">{sseState.running_count}</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 border rounded-lg">
                <p className="text-sm text-muted-foreground mb-1">Total Cards</p>
                <p className="text-2xl font-semibold">{sseState.total_cards_detected}</p>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <p className="text-sm text-muted-foreground mb-1">Current Frame</p>
                <p className="text-2xl font-semibold">{detectedCards.length}</p>
              </div>
            </div>

            {/* Detected Cards */}
            <div>
              <h3 className="text-sm font-medium mb-3">Detected Cards</h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {detectedCards.length > 0 ? (
                  detectedCards.map((card, i) => (
                    <div key={i} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">{card.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {card.rank} of {card.suit}
                        </p>
                      </div>
                      <Badge variant="outline">
                        {(card.confidence * 100).toFixed(1)}%
                      </Badge>
                    </div>
                  ))
                ) : (
                  <p className="text-center text-muted-foreground py-8">
                    No cards detected yet. Click "Detect Cards" to start.
                  </p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
