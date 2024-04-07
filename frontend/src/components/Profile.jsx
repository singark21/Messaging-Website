import { useEffect, useState } from "react";
import { useAuth, useUser } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [readOnly, setReadOnly] = useState(true);



  const formatDate = (isoDateTimeString) => {
    const date = new Date(isoDateTimeString);
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    return date.toDateString();
  };

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
    }
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    console.log("username: " + username);
    console.log("email: " + email);
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2">
        details
      </h2>
      <form className="border rounded px-4 py-2" onSubmit={onSubmit}>
      <div className="flex items-center mb-4">
          <label htmlFor="username" className="text-gray-400 mr-2">
            Username:
          </label>
          <span className="text-gray-200">
          {username}
          </span>
        </div>    

        <div className="flex items-center mb-4">
          <label htmlFor="email" className="text-gray-400 mr-2">
            Email:
          </label>
          <span className="text-gray-200">
          {email}
          </span>
        </div>    

        <div className="flex items-center mb-4">
          <label htmlFor="memberSince" className="text-gray-400 mr-2">
            Member Since:
          </label>
          <span className="text-gray-200">
          {user && formatDate(user.created_at)}
          </span>
        </div>    
      </form>
      <Button onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;