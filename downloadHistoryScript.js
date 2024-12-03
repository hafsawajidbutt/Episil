window.addEventListener('load', async function() {
    this.document.getElementById("loader").classList.add("loader")
    const request = new Request("http://127.0.0.1:5000/getUser", {
        method: "GET"})
    const response = await fetch(request)
    let data = await response.json()
    currentUser = data.userName
    const response2 = await fetch(`http://127.0.0.1:5000/getDownloadHistory?userName=${currentUser}`)
    let history = []
    history = await response2.json()
    console.log(history)
    storeElement = document.querySelector("#historyElement").inn
    parentDiv = document.querySelector(".Downloads")
    storeElement.innerHTML = history[0]
    for(let i = 1; i < history.length; i++)
    {
        cloneElement = storeElement.cloneNode(true)
        cloneElement.innerHTML = history[i]
        parentDiv.appendChild(cloneElement)
    }
    this.document.getElementById("loader").classList.remove("loader")
});