document.getElementById("loginButton").addEventListener("click", async function()
{
    console.log(document.getElementById("email").value)
    console.log(document.getElementById("password").value)
    const formData = new FormData();
    formData.append('userName', document.getElementById("email").value);
    formData.append('passWord', document.getElementById("password").value);
    const request = new Request("http://127.0.0.1:5000/verifyUser", {
        method: "POST",
        credentials: "include",
        body: formData});
    const response = await fetch(request)
    var data = await response.json()
    if(data.message === "Success")
    {
        console.log("Success")
        window.location.href = "./homePage.html"
    }    
    else if(data.message === "Failure")
    {
        console.log("Failure")
        document.getElementById("email").value = ""
        document.getElementById("password").value = ""
        document.getElementById("error").innerHTML = "Invalid credentials"
    }
})