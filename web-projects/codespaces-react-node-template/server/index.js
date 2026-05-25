const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.json());

app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Express API' });
});

// 如果你想要用后端提供前端打包文件，取消下面注释
// const clientBuildPath = path.join(__dirname, '..', 'client', 'dist');
// app.use(express.static(clientBuildPath));
// app.get('*', (req, res) => res.sendFile(path.join(clientBuildPath, 'index.html')));

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
