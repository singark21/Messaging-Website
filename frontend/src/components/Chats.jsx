import { useQuery,useQueryClient } from "react-query"
import { useState } from "react";
import { Link,useParams } from "react-router-dom";
import "./Chats.css";
import { getToken } from "../context/auth";
import ScrollContainer from "./ScrollContainer";


function ChatListItem({ chat }) {
    return (
      <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
        <div className="chat-list-item-name">
          {chat.name}
        </div>
      </Link>
    )
  }


function ChatList({ chats }){
    return (
        <div className="chat-list overflow-y-scroll">
          {chats.map((chat) => (
            <ChatListItem key={chat.id} chat={chat} />
          ))}
        </div>
      )
}

function ChatCard({ messages,chatId }) {
  const { data } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/chats")
        .then((response) => response.json())
    ),
  });
  const [message, setMessage] = useState("");
  const queryClient = useQueryClient();
  const handleMessageSubmit = async (e) => {
  e.preventDefault();

  try {
    const messageData = {
      text: message.trim(),
    };

    // Send a POST request to create a new message in the chat
    const response = await fetch(`http://localhost:8000/chats/${chatId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': `application/json`,
        'Authorization': `Bearer `+ getToken(),

      },
      body: JSON.stringify(messageData),
    });

    if (!response.ok) {
      throw new Error('Failed to create message');
    }

    queryClient.invalidateQueries({
      queryKey: ["chats", chatId, "messages"]
    })

    setMessage("");
  } catch (error) {
    console.error('Error creating message:', error);
  }
};
    return (
        <div className="flex flex-col max-h-main">
           <h2>Messages</h2>
          
          <ScrollContainer>
          {messages.map((message, index) => {
            const createdAtDate = new Date(message["created_at"]);
            const formattedCreatedAt = createdAtDate.toDateString();
            const formattedTime = createdAtDate.toLocaleTimeString();
            return (
              <div key={index} className="message-list-item">
                <div className="message-list-item-header">
                  <div className="message-list-item-user">
                    {message["user"]["username"].toString()}
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
          </ScrollContainer>
        
         <form onSubmit={handleMessageSubmit} className="mt-4 flex">
          <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="New message"
          className="flex-grow p-2 rounded-l bg-gray-600 text-white"
        />
           <button
          type="submit"
          className="px-4 py-2 rounded-r bg-blue-500 text-white font-semibold hover:bg-blue-600"
        >
          Send
        </button>
          </form>

      </div>
    );
  }

function ChatCardContainer({ messages, chatId }) {

    return (
      <div className="chat-card-container">
        <ChatCard messages={messages} chatId = {chatId}/>
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
        <div className="chat-list-container max-h-main">
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
      queryKey: ["chats", chatId, "messages"],
      queryFn: () => (
        fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
          .then((response) => response.json())
      ),
    });

    if (data && data.messages) {
      
      return( 
        <div>       
         
          <ChatCardContainer messages={data.messages} chatId = {chatId} />
         
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
          {chatId ? <ChatCardQueryContainer chatId={chatId} /> : 
            <h2 >Select a chat</h2>
          }
        </div>
      );
}
export default Chats;