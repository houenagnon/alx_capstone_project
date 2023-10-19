const data = {
    username: 'example_username',
    email: 'example@email.com',
    password: 'example_password'
  };
  
  fetch('http://127.0.0.1:5000/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Utilisateur enregistré avec succès : ', data);
  })
  .catch((error) => {
    console.error('Une erreur s\'est produite lors de l\'enregistrement de l\'utilisateur : ', error);
  });
  