import { useQuery,useQueryClient } from "react-query"
import { useEffect, useState } from "react";
import { Link,useParams } from "react-router-dom";
import "./Chats.css";
import { useApi } from "../hooks";
import { useUser } from "../hooks";

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


function ChatCard({ messages, chatId }) {
  const api = useApi();
  const queryClient = useQueryClient();
  const [message, setMessage] = useState("");
  const [editedMessage, setEditedMessage] = useState("");
  const [editingIndex, setEditingIndex] = useState(null);
  const currentUser = useUser();

  const handleMessageSubmit = async (e) => {
    e.preventDefault();
    try {
      const messageData = {
        text: message.trim(),
      };
      
      // Send a POST request to create a new message in the chat
      const response = await api.post(`/chats/${chatId}/messages`, messageData);

      if (!response.ok) {
        throw new Error('Failed to create message');
      }

      queryClient.invalidateQueries({
        queryKey: ["chats", chatId, "messages"]
      });

      setMessage("");
    } catch (error) {
      console.error('Error creating message:', error);
    }
  };

  const handleEdit = (index) => {
    setEditingIndex(index);
    setEditedMessage(messages[index].text);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      const updatedMessageData = {
        text: editedMessage.trim(),
      };

      const messageId = messages[editingIndex].id;
      // Send a PUT request to update the message
      const response = await api.put(`/chats/${chatId}/messages/${messageId}`, updatedMessageData);

      if (!response.ok) {
        throw new Error('Failed to update message');
      }

      queryClient.invalidateQueries({
        queryKey: ["chats", chatId, "messages"]
      });

      setEditingIndex(null);
    } catch (error) {
      console.error('Error updating message:', error);
    }
  };

  const handleCancel = () => {
    setEditingIndex(null);
  };

  const handleDelete = async (index) => {
    try {
      const messageId = messages[index].id;
      // Send a DELETE request to delete the message
      const response = await api.del(`/chats/${chatId}/messages/${messageId}`);

      if (!response.ok) {
        throw new Error('Failed to delete message');
      }

      queryClient.invalidateQueries({
        queryKey: ["chats", chatId, "messages"]
      });
    } catch (error) {
      console.error('Error deleting message:', error);
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
          const isCurrentUserMessage = message["user"]["id"] === currentUser.id;

          return (
            <div key={index} className="message-list-item">
              <div className="message-list-item-header">
                <div className="message-list-item-user">
                  {message["user"]["username"].toString()}
                </div>
                <div className="message-list-item-date">
                  {formattedCreatedAt} - {formattedTime}
                </div>  
                {isCurrentUserMessage && (
                  <div className="message-list-item-buttons">
                    {editingIndex === index ? (
                      <>
                        <button
                          onClick={handleSave}
                          className="px-2 py-1 rounded bg-green-500 text-white font-semibold mr-2"
                        >
                          Save
                        </button>
                        <button
                          onClick={handleCancel}
                          className="px-2 py-1 rounded bg-gray-500 text-white font-semibold"
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => handleEdit(index)}
                          className="px-2 py-1 rounded bg-yellow-500 text-white font-semibold mr-2"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(index)}
                          className="px-2 py-1 rounded bg-red-500 text-white font-semibold"
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                )}
              </div>
              
              <div className="message-list-item-text">
                {editingIndex === index ? (
                  <input
                    type="text"
                    value={editedMessage}
                    onChange={(e) => setEditedMessage(e.target.value)}
                    placeholder="Edit message"
                    className="p-2 rounded bg-gray-200 text-gray-800"
                  />
                ) : (
                  <div>{message["text"].toString()}</div>
                )}
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
  const currentUser = useUser();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Set loading to false once currentUser is available
    if (currentUser) {
      setLoading(false);
    }
  }, [currentUser]);

  // Render loading state while currentUser is being fetched
  if (loading) {
    return <h2>Loading...</h2>;
  }
    return (
      <div className="chat-card-container">
        <ChatCard messages={messages} chatId = {chatId}/>
      </div>
    );
  }

function ChatListContainer() {
  const api = useApi();
    const { data } = useQuery({
      queryKey: ["chats"],
      queryFn: () => (
        api.get("/chats").then((response) => response.json())
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

  }


  function ChatCardQueryContainer({ chatId }) {
    const api = useApi();
    const { data } = useQuery({
      queryKey: ["chats", chatId, "messages"],
      queryFn: () => (
        api.get(`/chats/${chatId}/messages`).then((response) => response.json())
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