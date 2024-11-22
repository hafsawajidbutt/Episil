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
