async function showDropdown() {
    console.log("In show dropdown")
    const searchBar = document.getElementById("search-bar")
    let showName = searchBar.value
    console.log(showName)
    const dropdown = document.getElementById("dropdown")
    const response = await fetch(`http://127.0.0.1:5000/getDownloadOptions?userName=${currentUser}&show=${showName}`)
    let showData = []
    showData = await response.json()
    console.log(showData)
    // Sample generic options for the dropdown
    const options = showData//["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    
    // Clear existing options
    dropdown.innerHTML = ""

    // Check if input is not empty
    if (searchBar.value.trim() !== "") {
        dropdown.classList.remove("hidden") // Show the dropdown
        console.log("In correct if")
        // Add each option to the dropdown
        options.forEach(option => {
            const dropdownItem = document.createElement("div")
            dropdownItem.classList.add("dropdown-item")
            
            // Create text for the dropdown option
            const optionText = document.createElement("span")
            optionText.textContent = option;

            // Create the like button
            const heartButton = document.createElement("button")
            heartButton.classList.add("heart-button")
            heartButton.innerHTML = "&#x2661;" // Heart symbol
            heartButton.onclick = function () {
                this.classList.toggle("liked")
                this.innerHTML = this.classList.contains("liked") ? "&#x2764;" : "&#x2661;"
            };

            // Append option text and heart button to the dropdown item
            dropdownItem.appendChild(optionText)
            dropdownItem.appendChild(heartButton)

            // Append the dropdown item to the dropdown
            dropdown.appendChild(dropdownItem)
        })
        console.log("Options appended")
    } else {
        dropdown.classList.add("hidden") // Hide the dropdown if input is empty
    }
}
// document.onload = async function()
// {
//     const response = await fetch("http://127.0.0.1:5000/getCookie")
//     var data = await response.json()
//     console.log(response)
//     console.log(data)
//     console.log("Code has run!")
// }
let currentUser = ""
window.addEventListener('load', async function() {
    console.log("Page about to load")
    const request = new Request("http://127.0.0.1:5000/getUser", {
        method: "GET"})
    const response = await fetch(request)
    let data = await response.json()
    currentUser = data.userName
    console.log(currentUser)
    const formData = new FormData()
    formData.append('userName', data.userName)
    const response2 = await fetch(`http://127.0.0.1:5000/getUserShows?userName=${currentUser}`)
    let showData = []
    showData = await response2.json()
    console.log(showData)
    animeNames = []
    banners = []
    for(let i = 0; i < showData.length; i++)
    {
        if(i % 2 == 0)
            animeNames.push(showData[i])
        else
            banners.push(showData[i])
    }
    console.log("Animes: " + animeNames)
    console.log("Banners: " + banners)
    parentDiv = this.document.querySelector(".grid")
    storeDiv = this.document.querySelector(".movie-card")
    storeDiv.querySelector(".movie-image").innerHTML = `<img src = ${banners[0]}>`
    storeDiv.querySelector(".movie-title").innerHTML = `<p> ${animeNames[0]} </p>`
    if(animeNames.length > 1)
    {
        for(let i = 1; i < animeNames.length; i++)
        {
            cloneDiv = storeDiv.cloneNode(true)
            storeDiv.querySelector(".movie-image").innerHTML = `<img src = ${banners[i]}>`
            storeDiv.querySelector(".movie-title").innerHTML = `<p> ${animeNames[i]} </p>`
            parentDiv.appendChild(cloneDiv)
        }
    }
    console.log("Page loaded")
});