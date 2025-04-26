let isChatOpen = false;

function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    isChatOpen = !isChatOpen;
    chatContainer.style.display = isChatOpen ? 'flex' : 'none';

    if(isChatOpen) {
        const chatIcon = document.querySelector('.chat-icon');
        chatIcon.classList.remove('notification');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Busca a mensagem de boas-vindas do backend
    fetch('/welcome')
        .then(response => response.json())
        .then(data => {
            addMessage(data.welcome, 'bot');
        })
        .catch(error => {
            console.error('Erro ao carregar mensagem inicial:', error);
        });
});

async function sendMessage() {
    const btn = document.querySelector('.btn-primary');
    btn.classList.add('sent'); 

    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if(message) {
        addMessage(message, 'user');
        userInput.value = '';
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            addMessage(data.response, 'bot');
            
            // Scroll automático garantido
            const messagesDiv = document.getElementById('chatMessages');
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        } catch (error) {
            console.error('Erro:', error);
            addMessage('Desculpe, ocorreu um erro.', 'bot');
        }
    }
    setTimeout(() => {
        btn.classList.remove('sent');
    }, 1000);
}

function addMessage(text, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const icon = document.createElement('img');
    icon.className = 'icon';
    icon.src = `static/${sender}-icon.png`;
    icon.alt = `${sender} icon`;

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = text;

    messageDiv.appendChild(icon);
    messageDiv.appendChild(content);
    messagesDiv.appendChild(messageDiv);
    messageDiv.scrollIntoView({ behavior: 'smooth' });

    if(sender === 'bot' && !isChatOpen) {
        const chatIcon = document.querySelector('.chat-icon');
        chatIcon.classList.add('notification');
    }
}

// Eventos melhorados
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('userInput').addEventListener('keypress', (e) => {
        if(e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});