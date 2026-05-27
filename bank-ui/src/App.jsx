import { useEffect, useState } from "react";
import API from "./services/api";

export default function App() {

  // STATES
  const [balance, setBalance] = useState(0);

  const [query, setQuery] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Namaste 👋 I’m your AI Voice Banking Assistant.",
    },
  ]);
  const [isRecording, setIsRecording] = useState(false);

  // FETCH BALANCE
  useEffect(() => {

    async function fetchBalance() {

      try {

        console.log("Calling Backend...");

        const response = await API.get("/balance/Rahul");

        console.log("BACKEND RESPONSE:", response.data);

        setBalance(response.data.balance);

      } catch (error) {

        console.log("FULL ERROR:", error);

      }

    }

    fetchBalance();

  }, []);

  // SEND QUERY
  async function sendQuery() {

    if (!query.trim()) return;

    // USER MESSAGE
    const userMessage = {
      sender: "user",
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {

      console.log("Sending query...");

      const res = await API.post("/ask", {
        query: query,
      });

      console.log(res.data);

      // AI MESSAGE
      const aiMessage = {
        sender: "ai",
        text: res.data.response,
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {

      console.log("SEND ERROR:", error);

      const errorMessage = {
        sender: "ai",
        text: "Backend connection failed.",
      };

      setMessages((prev) => [...prev, errorMessage]);

    }

    // CLEAR INPUT
    setQuery("");

  }

  async function startRecording() {

  try {

    // Ask microphone permission
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });

    setIsRecording(true);

    const mediaRecorder = new MediaRecorder(stream);

    const audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {

      const audioBlob = new Blob(audioChunks, {
        type: "audio/webm",
      });

      const formData = new FormData();

      formData.append("file", audioBlob, "voice.webm");

      try {

        const response = await fetch(
          "http://127.0.0.1:8000/voice",
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        console.log(data);

        // USER MESSAGE
        setMessages((prev) => [
          ...prev,
          {
            sender: "user",
            text: data.transcript,
          },
        ]);

        // AI RESPONSE
        setMessages((prev) => [
          ...prev,
          {
            sender: "ai",
            text: data.response,
          },
        ]);

      } catch (error) {

        console.log(error);

      }

      setIsRecording(false);

    };

    mediaRecorder.start();

    // STOP AFTER 5 SECONDS
    setTimeout(() => {

      mediaRecorder.stop();

    }, 5000);

  } catch (error) {

    console.log(error);

  }

}

  // SUGGESTIONS
  const suggestions = [
    "What is my balance?",
    "Last 5 transactions",
    "Who did I send money to?",
    "Who sent me money?",
    "Details about Priya",
    "Monthly spending",
  ];

  return (

    <div className="min-h-screen bg-[#1e1e1e] text-white flex">

      {/* LEFT SIDEBAR */}
      <div className="w-[350px] border-r border-gray-700 p-6 flex flex-col gap-6">

        {/* LOGO */}
        <div className="flex items-center gap-3 text-2xl font-bold">

          <div className="w-8 h-8 border border-gray-400 rounded-md flex items-center justify-center">
            □
          </div>

          <h1>Voice Bank AI</h1>

        </div>

        {/* PROFILE CARD */}
        <div className="bg-[#2a2a2a] rounded-3xl border border-gray-700 p-6">

          <div className="w-20 h-20 rounded-full bg-white text-blue-700 flex items-center justify-center text-3xl mb-5">
            RK
          </div>

          <h2 className="text-3xl font-semibold">
            Rahul Kumar
          </h2>

          <p className="text-gray-400 mt-2">
            ACC: HDFC-XXXX-4521
          </p>

          <div className="mt-5 bg-green-100 text-green-700 inline-flex items-center gap-2 px-4 py-2 rounded-xl">
            ◉ Voice Verified
          </div>

        </div>

        {/* BALANCE CARD */}
        <div className="bg-[#1f5ea8] rounded-3xl p-6">

          <p className="text-gray-200">
            Current Balance
          </p>

          <h2 className="text-5xl font-bold mt-4">
            ₹{balance.toLocaleString("en-IN")}
          </h2>

          <p className="mt-4 text-gray-200">
            Savings Account · HDFC Bank
          </p>

        </div>

        {/* TRY SAYING */}
        <div>

          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            TRY SAYING...
          </h3>

          <div className="flex flex-col gap-3">

            {suggestions.map((item, index) => (

              <button
                key={index}
                onClick={() => setQuery(item)}
                className="text-left bg-[#2a2a2a] border border-gray-700 rounded-2xl px-5 py-4 hover:bg-[#343434] transition-all"
              >
                💬 {item}
              </button>

            ))}

          </div>

        </div>

      </div>

      {/* RIGHT SIDE */}
      <div className="flex-1 flex flex-col">

        {/* TOP BAR */}
        <div className="border-b border-gray-700 p-5 text-gray-300 flex items-center gap-3">

          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>

          Ready — click mic or type a command

        </div>

        {/* CHAT AREA */}
        <div className="flex-1 p-10 overflow-y-auto">

          <div className="flex flex-col gap-6">

            {messages.map((msg, index) => (

              <div
                key={index}
                className={`flex ${
                  msg.sender === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >

                <div
                  className={`max-w-3xl p-6 rounded-3xl border ${
                    msg.sender === "ai"
                      ? "bg-[#242424] border-gray-700"
                      : "bg-blue-600 border-blue-500"
                  }`}
                >

                  <p className="text-xl leading-relaxed">
                    {msg.text}
                  </p>

                </div>

              </div>

            ))}

          </div>

        </div>

        {/* INPUT AREA */}
        <div className="border-t border-gray-700 p-5 flex items-center gap-5">

          {/* MIC BUTTON */}
          <button onClick={startRecording}
          className={`w-20 h-20 rounded-3xl border border-gray-700 text-2xl transition-all ${
            isRecording
              ? "bg-red-500 animate-pulse"
              : "bg-[#2a2a2a] hover:bg-[#3a3a3a]"
            }`}
          >
            🎙️
          </button>

          {/* INPUT */}
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendQuery();
              }
            }}
            placeholder="Type your banking query..."
            className="flex-1 h-20 rounded-full bg-[#171717] border border-gray-700 px-8 outline-none"
          />

          {/* SEND BUTTON */}
          <button
            onClick={sendQuery}
            className="w-20 h-20 rounded-3xl bg-[#2a2a2a] border border-gray-700 text-2xl hover:bg-[#3a3a3a] transition-all"
          >
            ➤
          </button>

        </div>

      </div>

    </div>

  );

}