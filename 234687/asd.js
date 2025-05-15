const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

// Példa: http://localhost:3000/JohnDoe/150
app.get('/:jatekosnev/:pont', async (req, res) => {
  const { jatekosnev, pont } = req.params;

  try {
    // Külső oldalnak történő továbbítás
    const response = await axios.post('https://pelda-cel-oldal.hu/fogadas', {
      jatekosnev,
      pont: Number(pont),
    });

    res.send(`Adat elküldve: ${jatekosnev} - ${pont}, válasz: ${response.status}`);
  } catch (error) {
    console.error('Hiba a küldés közben:', error.message);
    res.status(500).send('Hiba történt az adatküldés során.');
  }
});

app.listen(PORT, () => {
  console.log(`Szerver fut: http://localhost:${PORT}`);
});
