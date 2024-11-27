const { app, BrowserWindow, screen} = require('electron/main')
const {session} = require('electron')

let mainWindow = null

app.whenReady().then(() => {
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize
  
  mainWindow = new BrowserWindow({ width, height })
  mainWindow.loadFile('popupScreen.html')
})