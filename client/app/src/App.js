import React, {useState} from 'react';

const HOST = "localhost"
const PORT = 5000
const ENDPOINT = `http://` + HOST + ":" + PORT


function App() {
    let users = [
        {
            user: "semirat216@gmail.com",
            fonction: "Alt DA",
            departement: "DS2P",
            pays: "France",
            langue: "fra_Latn",
        }
    ]

    const [connectedUser, setConnectedUser] = useState({
        user: "test@test.com",
        fonction: "SPM",
        departement: "Log",
        pays: "USA",
        langue: "eng_Latn",
    })

    const [selectedUser, setSelectedUser] = useState(users[0])
    
    const [message, setMessage] = useState('');

    const [currentMessageStack, setCurrentMessageStack] = useState([]);

    const handleClick = (event) => {
        // Suppression du comportement par défaut de l'élément DOM
        event.preventDefault();
        
        // Envoi du message via l'API
        sendMessage()
            .then(() => {
                setMessage("")
                loadMessageStack()
            })
            .catch(e =>{
                console.error(e.message);
                alert("Message cannot be sent !")
            })
    }

    function displayMessages() {        
        return currentMessageStack.map(message => 
            connectedUser.user == message.expediteur
            ? SenderMessageBox(message.texte)
            : ReceiverMessageBox(message.texte)
        )
    }

    async function sendMessage(){
        try {
            const res = await fetch(ENDPOINT + "/envoyer", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    texte: message,
                    expediteur: connectedUser.user,
                    destinataire: selectedUser.user
                }),
            });
      
            if (!res.ok) {
              throw new Error('Network response was not ok');
            }
      
            const data = await res.json();
            
            return data
        } catch (error) {
           console.error(error.message);
        }

        return false        
    }

    async function loadMessageStack(){
        try {
            const res = await fetch(ENDPOINT + "/charger-conversation", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    expediteur: connectedUser.user,
                    destinataire: selectedUser.user
                }),
            });
      
            if (!res.ok) {
              throw new Error('Network response was not ok');
            }
      
            const data = await res.json();

            console.log(data);
            
            
            setCurrentMessageStack(data)
        
        } catch (error) {
           console.error(error.message);
           alert("Les messages ne peuvent pas être chargés.")
        }
    }

    function UserSideView(infos) {
        return (
          <li onClick={() => setSelectedUser(infos)}>
              <img src={ENDPOINT + "/images/" + infos.user} alt={infos.user}/>
              <div>
                  <h2>{infos.user}</h2>
                  <h3>
                      {infos.fonction} - {infos.departement}
                  </h3>
              </div>
          </li>
        )
    }

    function ReceiverMessageBox(texte){
        return (
            <li class="you">
                <div class="entete">
                    <h3>10:12AM, Today</h3>
                </div>
                <div class="triangle"></div>
                <div class="message">
                    {texte}
                </div>
            </li>
        )
    }

    function SenderMessageBox(texte){
        return (
            <li class="me">
                <div class="entete">
                    <h3>10:12AM, Today</h3>
                </div>
                <div class="triangle"></div>
                <div class="message">
                    {texte}
                </div>
            </li>
        )
    }
    
    return (
        <div id="container">
            <aside>
                <header>
                    <input type="text" placeholder="search"/>
                </header>
                
                <ul>                
                    {users.map(userInfo => 
                        UserSideView(userInfo)
                    )}
                </ul>
            </aside>
            
            <main>
                <header>
                    <img src={ENDPOINT + "/images/" + selectedUser.user} alt=""/>
                    <div>
                        <h2>{selectedUser.user}</h2>
                        <h3>{selectedUser.fonction} - {selectedUser.departement}</h3>
                    </div>
                </header>
                
                <ul id="chat">
                    {displayMessages()}
                </ul>
                
                <footer>
                    <textarea
                        id="writtenText"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type your message here"
                    />
                    <a href="#" onClick={handleClick}>Send</a>
                </footer>
            
            </main>
        </div>
    );
}

export default App;
