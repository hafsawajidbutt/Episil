import {getCookie} from './cookieGetter'
function showDropdown() {
    const searchBar = document.getElementById("search-bar");
    const dropdown = document.getElementById("dropdown");

    // Sample generic options for the dropdown
    const options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"];
    
    // Clear existing options
    dropdown.innerHTML = "";

    // Check if input is not empty
    if (searchBar.value.trim() !== "") {
        dropdown.classList.remove("hidden"); // Show the dropdown

        // Add each option to the dropdown
        options.forEach(option => {
            const dropdownItem = document.createElement("div");
            dropdownItem.classList.add("dropdown-item");
            
            // Create text for the dropdown option
            const optionText = document.createElement("span");
            optionText.textContent = option;

            // Create the like button
            const heartButton = document.createElement("button");
            heartButton.classList.add("heart-button");
            heartButton.innerHTML = "&#x2661;"; // Heart symbol
            heartButton.onclick = function () {
                this.classList.toggle("liked");
                this.innerHTML = this.classList.contains("liked") ? "&#x2764;" : "&#x2661;";
            };

            // Append option text and heart button to the dropdown item
            dropdownItem.appendChild(optionText);
            dropdownItem.appendChild(heartButton);

            // Append the dropdown item to the dropdown
            dropdown.appendChild(dropdownItem);
        });
    } else {
        dropdown.classList.add("hidden"); // Hide the dropdown if input is empty
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
window.addEventListener('load', setTimeout(async function() {
    // Your code to execute on page load goes here
    console.log("Page has loaded!")
    // const response = await fetch("http://127.0.0.1:5000/getCookie", {credentials: "same-origin"})
    // var data = await response.json()
    // console.log(response)
    // console.log(data.userName)
    // Query all cookies.
    cookie = getCookie()
    console.log(cookie)
    console.log("Potty")
  }), 2000);