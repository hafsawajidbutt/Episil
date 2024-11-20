document.getElementById("loginButton").addEventListener("click", async function()
{
    console.log(document.getElementById("email").value)
    console.log(document.getElementById("password").value)
    const formData = new FormData();
    formData.append('userName', document.getElementById("email").value);
    formData.append('passWord', document.getElementById("password").value);
    const request = new Request("http://127.0.0.1:5000/verifyUser", {
        method: "POST",
        body: formData});
    const response = await fetch(request)
    console.log(response.message)
    console.log(response)
})