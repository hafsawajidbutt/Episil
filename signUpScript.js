document.getElementById("signUp").addEventListener("click", async function()
{
    username = document.getElementById("username").value
    email = document.getElementById("email").value
    password = document.getElementById("password").value
    cpassword = document.getElementById("Cpassword").value
    profilePhoto = document.getElementById("ProfilePhoto").value
    console.log("Values collected")
    if(password.value == cpassword.value)
    {
        const formData = new FormData()
        formData.append('userName', username)
        formData.append('passWord', password)
        formData.append('email', email)
        formData.append('profilePictureLink', profilePhoto)
        const request = new Request("http://127.0.0.1:5000/addUser", {
            method: "POST",
            body: formData});
        const response = await fetch(request)
        var data = await response.json()
        console.log(response)
        console.log(data)
        if(data.message == "Success")
            window.location.href = "./login.html"
    }
})
