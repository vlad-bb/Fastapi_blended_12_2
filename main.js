console.log('Hello world!')

const ws = new WebSocket('ws://localhost:8080')

formChat.addEventListener('submit', (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})

ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}

ws.onmessage = (e) => {
    console.log(e.data)
    text = e.data.split('\n')
    for (let i = 0; i < text.length; i++) {
        const elMsg = document.createElement('div')
        elMsg.textContent = text[i]
        subscribe.appendChild(elMsg)
    }
}
