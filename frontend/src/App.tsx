import ChatComponent from "./chat/ChatComponent"
import "./App.css"

function App() {
  return (
    <div className="page-root">
      <header className="page-header">
        <h1 className="title">
          Book Recommender <span role="img" aria-label="books">📚</span>
        </h1>
        <p className="subtitle">
          Ask for a book by themes, e.g. “I want a book about magic and friendship” or
          “What do you recommend for someone who loves war stories?”.
        </p>
      </header>

      <ChatComponent />
    </div>
  );
}

export default App
