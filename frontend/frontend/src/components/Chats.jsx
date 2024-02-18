import { useQuery } from "react-query"
import { Link,useParams } from "react-router-dom";
import "./Chats.css";

function ChatListItem({ chat }) {
  const formattedDate = new Date(chat.created_at);
    return (
      <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
        <div className="chat-list-item-name">
          {chat.name}
        </div>
        <div className="chat-list-item-detail">
          {chat.user_ids.join(", ")}
        </div>
        <div className="chat-list-item-detail">
          created at: {formattedDate.toDateString()}
        </div>
      </Link>
    )
  }


function ChatList({ chats }){
    return (
        <div className="chat-list">
          {chats.map((chat) => (
            <ChatListItem key={chat.id} chat={chat} />
          ))}
        </div>
      )
}

function ChatCard({ messages }) {
    const attributes = [
      "user_id",
      "text",
      "created_at",
    ];
  
    return (
        <div className="message-list">
        {messages.map((message, index) => {
          const createdAtDate = new Date(message["created_at"]);
          const formattedCreatedAt = createdAtDate.toDateString();
          const formattedTime = createdAtDate.toLocaleTimeString();
          return (
            <div key={index} className="message-list-item">
              <div className="message-list-item-header">
                <div className="message-list-item-user">
                  {message["user_id"].toString()}
                </div>
                <div className="message-list-item-date">
                {formattedCreatedAt} - {formattedTime}
              </div>  
              </div>
              
              <div className="message-list-item-text">
                  {message["text"].toString()}
                </div>
            </div>
          );
        })}
      </div>
    );
  }

function ChatCardContainer({ messages }) {
    return (
      <div className="chat-card-container">
        <ChatCard messages={messages} />
      </div>
    );
  }

function ChatListContainer() {
    const { data } = useQuery({
      queryKey: ["chats"],
      queryFn: () => (
        fetch("http://127.0.0.1:8000/chats")
          .then((response) => response.json())
      ),
    });
  
    if (data?.chats) {
      return (
        <div className="chat-list-container">
          <h2>Chats</h2>
          <ChatList chats={data.chats} />
        </div>
      )
    }
  
    return (
      <h2>Chat list</h2>
    );
  }


  function ChatCardQueryContainer({ chatId }) {
    const { data } = useQuery({
      queryKey: ["chats", chatId],
      queryFn: () => (
        fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
          .then((response) => response.json())
      ),
    });
  
    if (data && data.messages) {

      return( 
        <div>       
          <h2>Messages</h2>
          <ChatCardContainer messages={data.messages} />
        </div>

      )
    }
  
    return <h2>loading...</h2>
  }

function Chats(){
    const { chatId } = useParams();
    return (
        <div className="chats-page">
          <ChatListContainer />
          {chatId ? <ChatCardQueryContainer chatId={chatId} /> : <h2>Select a chat</h2>}
        </div>
      );
}

export default Chats;