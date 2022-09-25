class Chatbox {
    constructor() {
        activate_button: document.query_selector('.chatbox__button'),   // the button that activates the chat
        chatbox: document.query_selector('.chatbox__support'),    // the main chat window
        send_button: document.query_selector('.send__button')    // the send button
    }

    this.state = false;
    this.messages = [];

    display() {
        const {activate_button, chatbox, send_button} = this.args;
        activate_button.addEventListener('click', () => this.toggleState(chatbox))   // when clicked, activate chat
        send_button.addEventListener('click', () => this.onSendButton(chatbox))  // when clicked, send the user input

        const chat_node = chatbox.query_selector('input');  // node that listens on the chatbox window
        chat_node.addEventListener('keyup', ({key}) => {  // instead of send button, user can also use <Enter>
            if (key ==="Enter") {
                this.onSendButton(chatbox)
            }
        })
    }

    toggleState (chatbox) {
        this.state = !this.state   // toggle state on/off
        alert("activating chat");
        if (this.state) {   // if state is on, then activate (show) the chat window
            chatbox.classList.add('chatbox--active')
        } else {  // else, hide the chat window
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {   // TODO: implement functionality for when the user sends a message

    }


}


const chat_window = new Chatbox();   // create a new Chatbox object that will represent the chat window
chat_window.display();   // adds functionality to the chat window, by activating the various event listeners