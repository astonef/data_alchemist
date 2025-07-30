export default function TestPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center space-y-4 bg-dracula-background text-dracula-foreground">
      <div className="text-2xl font-bold">Test Dracula Colors</div>
      <div className="w-40 h-10 bg-dracula-purple text-center">Purple</div>
      <div className="w-40 h-10 bg-dracula-pink text-center">Pink</div>
      <div className="w-40 h-10 bg-dracula-comment text-center">Comment</div>
      <div className="w-40 h-10 bg-dracula-yellow text-center text-black">Yellow</div>
    </div>
  )
}
