let showName = ""
let showData = []
let currentUser = ""
async function showDropdown() {
    this.document.getElementById("loader").classList.add("loader")
    console.log("In show dropdown")
    const searchBar = document.getElementById("search-bar")
    showName = searchBar.value
    console.log(showName)
    const dropdown = document.getElementById("dropdown")
    const response = await fetch(`http://127.0.0.1:5000/getDownloadOptions?userName=${currentUser}&show=${showName}`)
    showData = await response.json()
    console.log(showData)
    const options = showData//["option 1", "option 2", "option 3"]
    
    // Clear existing options
    dropdown.innerHTML = ""

    // Check if input is not empty
    if (searchBar.value.trim() !== "") {
        dropdown.classList.remove("hidden") // Show the dropdown
        console.log("In correct if")
        // Add each option to the dropdown
        let index = 0
        options.forEach(option => {
            const dropdownItem = document.createElement("div")
            dropdownItem.classList.add("dropdown-item")
            // Create text for the dropdown option
            const optionText = document.createElement("span")
            optionText.textContent = option;

            // Create the like button
            const heartButton = document.createElement("button")
            heartButton.classList.add("heart-button")
            heartButton.id = option
            heartButton.innerHTML = "&#x2661;" // Heart symbol
            heartButton.onclick = async function (event) {
                this.document.getElementById("loader").classList.add("loader")
                this.classList.toggle("liked")
                this.innerHTML = this.classList.contains("liked") ? "&#x2764;" : "&#x2661;"
                let show = event.target.id
                console.log("Show clicked: "+ show)
                console.log("By: " + currentUser)
                const formData = new FormData();
                formData.append('userName', currentUser);
                formData.append('show', show);
                const request = new Request("http://127.0.0.1:5000/insertShow", {
                    method: "POST",
                    body: formData});
                const response2 = await fetch(request)
                var data = await response2.json()
                console.log(response2)
                console.log(data.message)
                this.document.getElementById("loader").classList.add("loader")
                loadPage()
                const request2 = new Request("http://127.0.0.1:5000/download", {
                    method: "POST",
                    body: formData});
                const response3 = await fetch(request2)
                var data2 = await response3.json()
                console.log()
            };
            // Append option text and heart button to the dropdown item
            dropdownItem.appendChild(optionText)
            dropdownItem.appendChild(heartButton)
            // Append the dropdown item to the dropdown
            dropdown.appendChild(dropdownItem)
            index++
        })
        this.document.getElementById("loader").classList.remove("loader")  
        console.log("Options appended")
    } else {
        dropdown.classList.add("hidden") // Hide the dropdown if input is empty
    }
}
document.querySelector("#logOut").addEventListener("click", async function()
{
    document.getElementById("loader").classList.add("loader")
    const request = new Request("http://127.0.0.1:5000/logOut", {
        method: "POST"});
    const response = await fetch(request)
    var data = await response.json()
    console.log(data)
    document.getElementById("loader").classList.remove("loader")
    window.location.href = "./login.html"
})
async function loadPage()
{
    classList = document.querySelector(".movie-card").classList
    if(!("hidden" in classList))
        document.querySelector(".movie-card").classList.add("hidden")
    document.querySelector(".movie-card").classList.add("hidden")
    this.document.getElementById("loader").classList.add("loader")
    console.log("Added class")
    console.log("Page about to load")
    const request = new Request("http://127.0.0.1:5000/getUser", {
        method: "GET"})
    const response = await fetch(request)
    let data = await response.json()
    currentUser = data.userName
    console.log(currentUser)
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
    parentDiv.innerHTML = '<div class="movie-card"><div class="movie-image"></div><div class="movie-title"></div></div>'
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
    this.document.getElementById("loader").classList.remove("loader")
    //document.querySelectorAll(".movie-card").classList.remove("hidden")
    console.log("Removed class")
    console.log("Page loaded")
}
window.addEventListener('load', function() {
    loadPage()
});
document.querySelector("#editProfile").addEventListener('click', function()
{
    window.location.href = "./editProfile.html"
})
document.querySelector("#history").addEventListener('click', function()
{
    window.location.href = "./downloadHistory.html"
})