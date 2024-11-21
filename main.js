const { app, BrowserWindow} = require('electron')
const createWindow = () => {
    const win = new BrowserWindow({
      width: 800,
      height: 600,
      icon: "favicon.png"
    })
  
    win.loadFile('popupScreen.html')
  }

  app.whenReady().then(() => {
    createWindow()
  })