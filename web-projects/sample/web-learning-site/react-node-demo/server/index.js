const express = require('express');
const app = express();
const port = 4000;

app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Express API!' });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
