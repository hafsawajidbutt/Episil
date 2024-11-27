const { app, BrowserWindow, screen} = require('electron/main')
const {session} = require('electron')

let mainWindow = null

app.whenReady().then(async () => {
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize
  mainWindow = new BrowserWindow({ width, height })
  const request = new Request("http://127.0.0.1:5000/getUser", {
    method: "GET"});
  const response = await fetch(request)
  var data = await response.json()
  if(data.userName == "No username")
    mainWindow.loadFile('popupScreen.html')
  else
    mainWindow.loadFile('homePage.html')
})