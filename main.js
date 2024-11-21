const { app, BrowserWindow, screen} = require('electron/main')

let mainWindow = null

app.whenReady().then(() => {
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize

  mainWindow = new BrowserWindow({ width, height })
  mainWindow.loadFile('popupScreen.html')
})
// const createWindow = () => {
//     const win = new BrowserWindow({
//       width: 800,
//       height: 600,
//       icon: "favicon.png"
//     })
  
//     win.loadFile('popupScreen.html')
//   }

//   app.whenReady().then(() => {
//     createWindow()
//   })