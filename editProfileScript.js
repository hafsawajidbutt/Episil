console.log("Connected")
document.querySelector("#back").addEventListener('click', function()
{
    console.log("Clickie")
    window.location.href = "./homePage.html"
})
// document.getElementById("change").addEventListener("click", function()
// {
//     console.log("Click")
// })
document.querySelector("#change").addEventListener('click', async function()
{
    this.document.getElementById("loader").classList.add("loader")
    console.log("Clicked")
    var newUserName = document.querySelector("#username").value
    var profilePictureLink = document.querySelector("#pfp-link").value
    console.log(newUserName)
    console.log(profilePictureLink)
    if(newUserName != "" && profilePictureLink != "")
    {
        const request = new Request("http://127.0.0.1:5000/getUser", {
            method: "GET"})
        const response = await fetch(request)
        let data = await response.json()
        currentUser = data.userName
        console.log(currentUser)
        
        const formData2 = new FormData();
        formData2.append('userName', currentUser);
        formData2.append('profilePictureLink', profilePictureLink);
        const request3 = new Request("http://127.0.0.1:5000/changeProfilePicture", {
            method: "POST",
            body: formData2});
        const response3 = await fetch(request3)
        var data3 = await response3.json()
        console.log(data3)

        const formData = new FormData();
        formData.append('userName', currentUser);
        formData.append('newUserName', newUserName);
        const request2 = new Request("http://127.0.0.1:5000/changeUserName", {
            method: "POST",
            body: formData});
        const response2 = await fetch(request2)
        var data2 = await response2.json()
        console.log(data2)
        
        this.document.getElementById("loader").classList.remove("loader")
        console.log("Done")
        window.location.href = "./homePage.html"
    }
    else if(userName != "")
    {
        const request = new Request("http://127.0.0.1:5000/getUser", {
            method: "GET"})
        const response = await fetch(request)
        let data = await response.json()
        currentUser = data.userName
        console.log(currentUser)
        
        const formData2 = new FormData();
        formData2.append('userName', currentUser);
        formData2.append('profilePictureLink', profilePictureLink);
        const request3 = new Request("http://127.0.0.1:5000/changeProfilePicture", {
            method: "POST",
            body: formData2});
        const response3 = await fetch(request3)
        var data3 = await response3.json()
        console.log(data3)
        
        this.document.getElementById("loader").classList.remove("loader")
        window.location.href = "./homePage.html"
    }
    else if(profilePictureLink != "")
    {
        const request = new Request("http://127.0.0.1:5000/getUser", {
            method: "GET"})
        const response = await fetch(request)
        let data = await response.json()
        currentUser = data.userName
        console.log(currentUser)
        
        const formData2 = new FormData();
        formData2.append('userName', currentUser);
        formData2.append('profilePictureLink', profilePictureLink);
        const request3 = new Request("http://127.0.0.1:5000/changeProfilePicture", {
            method: "POST",
            body: formData2});
        const response3 = await fetch(request3)
        var data3 = await response3.json()
        console.log(data3)
        
        this.document.getElementById("loader").classList.remove("loader")
        window.location.href = "./homePage.html"
    }
})
