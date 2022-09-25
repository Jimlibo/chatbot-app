class Chatbox {
    constructor() {
        this.args = {
            activate_button: document.querySelector('.chatbox__button'),   // the button that activates the chat
            chatbox: document.querySelector('.chatbox__support'),   // the main chat window
            send_button: document.querySelector('.send__button'),   // the send button
            cancel_button: document.querySelector('.close__button')  // the 'x' button to close the window
        }
    
        this.state = false;
        this.messages = [];
    }

    
    display() {
        const {activate_button, chatbox, send_button, cancel_button} = this.args;
        activate_button.addEventListener('click', () => this.toggleState(chatbox))   // when clicked, activate chat
        send_button.addEventListener('click', () => this.onSendButton(chatbox))  // when clicked, send the user input
        cancel_button.addEventListener('click', () => this.toggleState(chatbox))  // when clicked, close the window

        const chat_node = chatbox.querySelector('input');  // node that listens on the chatbox window
        chat_node.addEventListener("keyup", ({key}) => {  // instead of send button, user can also use <Enter>
            if (key === "Enter") {
                this.onSendButton(chatbox)
            }
        })
    }


    toggleState (chatbox) {
        this.state = !this.state   // toggle state on/off
        if (this.state) {   // if state is on, then activate (show) the chat window
            chatbox.classList.add('chatbox--active')
        } else {  // else, hide the chat window
            chatbox.classList.remove('chatbox--active')
        }
    }


    onSendButton(chatbox) {
        var text_input = chatbox.querySelector('input');   // get the text field component from the chat window
        let text = text_input.value;
        if (text === "") {   // if text field is empty, do nothing
            return;
        }

        let msg = {name: "User", message: text}    // create object with message and sender
        this.messages.push(msg)  // add the new message to the list of messages

        fetch($SCRIPT_ROOT + '/predict', {    // create a post request with the data, and get the answer 
            method: 'POST',
            body: JSON.stringify({message: text}),
            mode: 'cors',
            headers: {'Content-Type': 'application/json'} 
        }).then(
            res => res.json()   // get the response in a json format
            ).then(res => {
                let bot_msg = {name: "Nio", message: res.response};  // create the message object with the response
                this.messages.push(bot_msg)   // add it to the list of messages
                this.updateChat(chatbox)   // update the chat with the new messages
                text_input.value = ''   // clear the text input field from the previous message
        }).catch((error) =>{   // if error occured, handle it and update the chat window
            alert("Error:" + error);
            console.error('Error occured:', error);   // print it to the console for debugging
            this.updateChat(chatbox)
            text_input.value = ''
        });
    }


    updateChat(chatbox) {  // function that updates the message environment based on the messages that have been sent
        var html_content = '';   

        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Nio") {   // message from the chatbot
                html_content += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            } 
            else {   // message from the user
                html_content += '<div class="message__item messages__item--operator">' + item.message + '</div>'
            }
        });
        const chat_env = chatbox.querySelector('.chatbox__messages');   // get the chat window space were the messages are shown
        chat_env.innerHTML = html_content;   // update the contents of that space based on the new messages
    }


}

const chat_window = new Chatbox();   // create a new Chatbox object that will represent the chat window
chat_window.display();   // adds functionality to the chat window, by activating the various event listeners