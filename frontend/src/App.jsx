import { useState } from "react"

const API = "http://127.0.0.1:8000"

function App() {

  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState([])
  const [permission, setPermission] = useState(null)
  const [activity, setActivity] = useState([])

  async function sendMessage() {

    if (!message.trim()) return

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        text: message
      }
    ])

    const response = await fetch(`${API}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message,
        user_id: "demo_user"
      })
    })

    const data = await response.json()

    setMessages(prev => [
      ...prev,
      {
        role: "agent",
        text: data.message
      }
    ])

    setActivity(data.activity || [])

    if (data.permission_required) {
      setPermission({
        id: data.permission_id
      })
    }

    setMessage("")
  }

  async function handlePermission(allowed) {

  // Tell backend whether user allowed or denied
  await fetch(`${API}/permission`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      permission_id: permission.id,
      allowed: allowed
    })
  })

  setPermission(null)

  // If user denied, stop here
  if (!allowed) {

    setMessages(prev => [
      ...prev,
      {
        role: "agent",
        text: "Permission denied. I did not access your information."
      }
    ])

    setActivity(prev => [
      ...prev,
      "Permission denied",
      "Tool execution skipped"
    ])

    return
  }

  // If user allowed, continue the ORIGINAL request
  const response = await fetch(`${API}/continue`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: "",
      user_id: "demo_user"
    })
  })

  const data = await response.json()

  setMessages(prev => [
    ...prev,
    {
      role: "agent",
      text: data.message
    }
  ])

  setActivity(data.activity || [])
}
  return (
    <div className="min-h-screen bg-slate-100">

      <header className="bg-white border-b p-4">

        <div className="max-w-5xl mx-auto flex justify-between">

          <div>
            <h1 className="text-xl font-bold">
              🇮🇳 Bharat Personal Agent
            </h1>

            <p className="text-sm text-gray-500">
              Privacy-first personal AI assistant
            </p>
          </div>

          <div className="text-xs text-green-600">
            ● Demo Mode
          </div>

        </div>

      </header>


      <main className="max-w-5xl mx-auto p-4 grid md:grid-cols-3 gap-4">

        {/* CHAT */}

        <section className="md:col-span-2 bg-white rounded-xl shadow-sm">

          <div className="h-[500px] overflow-y-auto p-4">

            {messages.length === 0 && (

              <div className="text-center text-gray-500 mt-20">

                <div className="text-4xl mb-3">
                  🤖
                </div>

                <h2 className="font-semibold">
                  How can I help?
                </h2>

                <p className="text-sm mt-2">
                  Try: "Check my healthcare status"
                </p>

              </div>

            )}

            {messages.map((msg, index) => (

              <div
                key={index}
                className={`mb-4 ${
                  msg.role === "user"
                    ? "text-right"
                    : "text-left"
                }`}
              >

                <div
                  className={`inline-block p-3 rounded-xl max-w-[80%] ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {msg.text}
                </div>

              </div>

            ))}

          </div>


          <div className="border-t p-3 flex gap-2">

            <input
              value={message}
              onChange={e => setMessage(e.target.value)}
              onKeyDown={e => {
                if (e.key === "Enter") sendMessage()
              }}
              placeholder="Ask your personal agent..."
              className="flex-1 border rounded-lg px-3 py-2"
            />

            <button
              onClick={sendMessage}
              className="bg-blue-600 text-white px-5 rounded-lg"
            >
              Send
            </button>

          </div>

        </section>


        {/* SIDEBAR */}

        <aside className="space-y-4">

          <div className="bg-white rounded-xl p-4 shadow-sm">

            <h2 className="font-semibold mb-3">
              🔐 Privacy
            </h2>

            <div className="text-sm space-y-2">

              <p>✓ Local memory enabled</p>
              <p>✓ Permission required</p>
              <p>✓ Mock APIs only</p>
              <p>✓ No real transactions</p>
              <p>✓ No government database access</p>

            </div>

          </div>


          <div className="bg-white rounded-xl p-4 shadow-sm">

            <h2 className="font-semibold mb-3">
              🧠 Agent Activity
            </h2>

            <div className="text-xs space-y-2">

              {activity.length === 0 && (
                <p className="text-gray-400">
                  No activity yet
                </p>
              )}

              {activity.map((item, index) => (
                <div key={index}>
                  • {item}
                </div>
              ))}

            </div>

          </div>

        </aside>

      </main>


      {/* PERMISSION MODAL */}

      {permission && (

        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">

          <div className="bg-white rounded-xl p-6 max-w-sm w-full">

            <div className="text-3xl mb-3">
              🔐
            </div>

            <h2 className="text-lg font-bold">
              Permission Required
            </h2>

            <p className="text-gray-600 text-sm mt-2">
              This request requires access to sensitive
              information. Do you want to allow it?
            </p>

            <div className="flex gap-3 mt-6">

              <button
                onClick={() => handlePermission(false)}
                className="flex-1 border rounded-lg py-2"
              >
                Deny
              </button>

              <button
                onClick={() => handlePermission(true)}
                className="flex-1 bg-blue-600 text-white rounded-lg py-2"
              >
                Allow
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  )
}

export default App